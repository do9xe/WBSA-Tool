function stringToColor(str) {
  let hash = 0;
  str.split('').forEach(char => {
    hash = char.charCodeAt(0) + ((hash << 6) - hash)
  })
  let colour = '#'
  for (let i = 0; i < 3; i++) {
    const value = (hash >> (i * 8)) & 0xff
    colour += value.toString(16).padStart(2, '0')
  }
  return colour
}

function getTimeslotName(timeslot) {
    var splitdate = timeslot.date.split("-");
    var date = splitdate[2]+'.'+splitdate[1]+'.'+splitdate[0].slice(2,4)
    return date +', '+ timeslot.time_from.slice(0,-3) + '-' + timeslot.time_to.slice(0,-3) + ' Uhr'
}

function setNewAppMarker(lat, long) {
    newAppMarker.setLatLng([lat, long]);
    map.flyTo([lat, long], 16);
}
function hideNewAppMarker() {
    newAppMarker.setLatLng(["0", "0"]);
}

async function updateMarker() {
    var street = document.getElementById("street").value;
    var house_number = document.getElementById("house_number").value;
    if (street === "" || house_number === "") {
        hideNewAppMarker();
        return
    }
    params = {
        "street": street +" "+house_number,
        "city": "Karlsruhe",
        "postalcode": "76227",
        "format": "jsonv2"
    }
    var response = await fetch(nominatim_url +'?'+ new URLSearchParams(params));
    var coordinates = await response.json();
    setNewAppMarker(coordinates[0].lat, coordinates[0].lon);
}

async function getAreas() {
    var response = await fetch("/api/area?is_parent=True");
    return response.json();
}

async function getTimeslots() {
    var response = await fetch("/api/timeslot");
    return response.json();
}

async function getAppointments() {
    var response = await fetch("/api/appointment");
    return response.json();
}

function createMarker(appointment) {
    var color = stringToColor(getTimeslotName(appointment.timeslot))
    var marker = new L.Marker([appointment.lat,appointment.lon])
    .bindPopup('<div>'
        + appointment.contact_name
        +'<br>'+ appointment.street.name + ' ' + appointment.house_number
        +'<br>' + getTimeslotName(appointment.timeslot) +
        '</div>',popupOption).openPopup();
    if (L.ExtraMarkers !== undefined) {
        var markerIcon = L.ExtraMarkers.icon({
                icon: "true",
                svg: true,
                markerColor: color
        });
        marker.setIcon(markerIcon);
    }
    return marker;
}
/***********************************************************
* Section where we create the actual Map and center it     *
***********************************************************/
// Creating map options
var mapOptions = {
    center: [48.99707935, 8.47255828438081],
    zoom: 15
}
// Creating a map object
var map = new L.map('map', mapOptions);

// Creating a Layer object
var backgroundMap = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
// Adding layer to the map
map.addLayer(backgroundMap);

/***********************************************************
* Section where we add all the markers to layer-groups     *
***********************************************************/

const popupOption = {
    "closeButton":false
}

Promise.all([getAreas(), getTimeslots(), getAppointments()]).then(results =>{
    var bounds = [];
    var timeslotList = results[1];
    var appointmentList = results[2];
    var layerControl = L.control.layers(null, null, {collapsed:false}).addTo(map);

    timeslotList.forEach(timeslot => {
        var markers = new L.markerClusterGroup({disableClusteringAtZoom: 1,});
        appointmentList.forEach(appointment => {
            if (appointment.timeslot.id === timeslot.id) {
                var marker = createMarker(appointment);
                bounds.push([appointment.lat, appointment.lon]);
                markers.addLayer(marker);
            }
        });
        layerControl.addOverlay(markers, getTimeslotName(timeslot));
        map.addLayer(markers);
    });
    map.fitBounds(new L.LatLngBounds(bounds));
});

var newMarkerIcon = L.ExtraMarkers.icon({
    icon: "true",
    svg: true,
    markerColor: "#ffeb00"
})

var newAppMarker = new L.Marker(["0","0"], {icon: newMarkerIcon}).addTo(map);
var typingTimer;
document.addEventListener('DOMContentLoaded', () => {
    var house_number = document.getElementById("house_number");
    house_number.addEventListener("keyup", function(e) {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(updateMarker, 1000);
    });
    house_number.addEventListener("keydown", function(e) {
        clearTimeout(typingTimer);
    });
});