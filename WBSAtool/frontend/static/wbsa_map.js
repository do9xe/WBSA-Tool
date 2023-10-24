async function getAreas() {
    var response = await fetch("/api/area?is_parent=True");
    return response.json();
}

async function getAppointments() {
    var response = await fetch("/api/appointment");
    return response.json();
}

function createMarker(appointment) {
    var marker = new L.Marker([appointment.lat,appointment.lon])
    .on("mouseover",event =>{
        event.target.bindPopup('<div>'+ appointment.title +'<br>'+ appointment.address+'<br>Abholdatum:'+ appointment.date+'</div>',popupOption).openPopup();
    })
    .on("mouseout", event => {
        event.target.closePopup();
    })
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

Promise.all([getAreas(), getAppointments()]).then(results =>{
    var bounds = [];
    var areaList = results[0];
    var appointmentList = results[1];
    var layerControl = L.control.layers(null, null, {collapsed:false}).addTo(map);

    areaList.forEach(area => {
        var markers = new L.markerClusterGroup();
        appointmentList.filter(appointment => appointment.street.area != null)
            .forEach(appointment => {
            if (appointment.street.area.parent === area.id) {
                var marker = createMarker(appointment);
                bounds.push([appointment.lat, appointment.lon]);
                markers.addLayer(marker);
            }
        });
        layerControl.addOverlay(markers, area.name);
        map.addLayer(markers);
    });
    map.fitBounds(new L.LatLngBounds(bounds));
});
