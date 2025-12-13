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
    if (street === "") {
        hideNewAppMarker();
        return
    }
    if (house_number === "") {
        house_number = 0;
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
function scrollToAppointment(id) {
    document.getElementById(id).scrollIntoView({behavior:'smooth'});
    document.getElementById(id).classList.remove("bg-secondary");
    document.getElementById(id).classList.add("bg-warning");
    setTimeout(() => {
        document.getElementById(id).classList.remove("bg-warning");
        document.getElementById(id).classList.add("bg-secondary");
    }, 1500)
}

/*****************
 Valid values for usecases are: "generic", "appointment", "dispo"
******************/
function createMarker(appointment, usecase) {
    const popupOption = {
        "closeButton":false
    }

    var marker = new L.Marker([appointment.lat,appointment.lon])
    .bindPopup('<div>'
        + '<a href="/appointment/list?id='+ appointment.id +'">' + appointment.contact_name + '</a>'
        +'<br>'+ appointment.street.name + ' ' + appointment.house_number
        +'<br>' + getTimeslotName(appointment.timeslot) +
        '</div>',popupOption).openPopup();
    if (usecase !== "generic") {
        if (usecase === "appointment") {
            var color = stringToColor(getTimeslotName(appointment.timeslot));
        }
        if (usecase === "dispo") {
            var name = "dispo";
            areaList.forEach(area => {
                try {
                    if (area.id === appointment.area || (area.id === appointment.street.area.parent && appointment.area === null)) {
                        name = area.name;
                    }
                } catch (e){}
            });
            var color = stringToColor(name);
            marker.addEventListener("click", () => {
                scrollToAppointment("ap_" + appointment.id);
            });
        }
        var markerIcon = L.ExtraMarkers.icon({
                icon: "true",
                svg: true,
                markerColor: color
        });
        marker.setIcon(markerIcon);
    }
    return marker;
}

function loadMapBasics() {
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
    return map;
}

function loadGenericMap() {
    var map = loadMapBasics();
    Promise.all([getTimeslots(), getAppointments()]).then(results =>{
        var bounds = [];
        var timeslotList = results[0];
        var appointmentList = results[1];
        var layerControl = L.control.layers(null, null, {collapsed:false}).addTo(map);
        timeslotList.forEach(timeslot => {
            var markers = new L.markerClusterGroup({disableClusteringAtZoom: 1,});
            appointmentList.forEach(appointment => {
                if (appointment.timeslot.id === timeslot.id) {
                    var marker = createMarker(appointment, "generic");
                    bounds.push([appointment.lat, appointment.lon]);
                    markers.addLayer(marker);
                }
            });
            layerControl.addOverlay(markers, getTimeslotName(timeslot));
            map.addLayer(markers);
        });
        map.fitBounds(new L.LatLngBounds(bounds));
    });
}

function loadAppointmentMap() {
    globalThis.map = loadMapBasics();

    Promise.all([getTimeslots(), getAppointments()]).then(results => {
        var bounds = [];
        var timeslotList = results[0];
        var appointmentList = results[1];
        var layerControl = L.control.layers(null, null, {collapsed: false}).addTo(map);
        timeslotList.forEach(timeslot => {
            var markers = new L.markerClusterGroup({disableClusteringAtZoom: 1,});
            appointmentList.forEach(appointment => {
                if (appointment.timeslot.id === timeslot.id) {
                    var marker = createMarker(appointment, "appointment");
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

    globalThis.newAppMarker = new L.Marker(["0", "0"], {icon: newMarkerIcon}).addTo(map);
    globalThis.typingTimer = null;

    document.addEventListener('DOMContentLoaded', () => {
        var house_number = document.getElementById("house_number");
        house_number.addEventListener("focusout", function (e) {
            clearTimeout(typingTimer);
            globalThis.typingTimer = setTimeout(updateMarker, 500);
        });
        house_number.addEventListener("focus", function (e) {
            clearTimeout(typingTimer);
        });
    });
}

function loadDispoMap() {
    var map = loadMapBasics();
    Promise.all([getTimeslots(), getAppointments(), getAreas()]).then(results => {
        var bounds = [];
        globalThis.allMarkers = {};
        globalThis.timeslotList = results[0];
        globalThis.appointmentList = results[1];
        globalThis.areaList = results[2];
        var layerControl = L.control.layers(null, null, {collapsed: false}).addTo(map);

        timeslotList.forEach(timeslot => {
            var markers = new L.markerClusterGroup({disableClusteringAtZoom: 1,});
            appointmentList.forEach(appointment => {
                if (appointment.timeslot.id === timeslot.id) {
                    var marker = createMarker(appointment, "dispo");
                    allMarkers["ap_" + String(appointment.id)] = marker;
                    bounds.push([appointment.lat, appointment.lon]);
                    markers.addLayer(marker);
                }
            });
            layerControl.addOverlay(markers, getTimeslotName(timeslot));
            map.addLayer(markers);
        });
        map.fitBounds(new L.LatLngBounds(bounds));
        fillTimeslotBars(timeslotList);
    });
}