// Funktionen für das Autocomplete in den Textfeldern
/*
Usage:
Innerhalb des HTML ein <script> Element setzen und darin folgendes definieren:
var countries = ["Afghanistan","Albania"];
autocomplete(document.getElementById("myInput"), countries);

*/
function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item includes the same letters as the text field value:*/
        if (String(arr[i]).toUpperCase().includes(val.toUpperCase())) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          var strPosition = String(arr[i]).toUpperCase().indexOf(val.toUpperCase());

          b.innerHTML += arr[i].substr(0, strPosition);
          b.innerHTML += "<strong>" + arr[i].substr(strPosition, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(strPosition+val.length);

          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
          b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              const selection = this.getElementsByTagName("input")[0].value;
              inp.value = selection;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
              updateMarker();
              loadTimeslotsForStreet(selection);
              getTimeslotSuggestions(selection);
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}

// Einblenden eines Fensters mit den Details einer Abholung
async function showAppointmentDetails(appointmentID) {
    const modalContentDIV = document.getElementById("appointment_detail");
    const response = await fetch(`/appointment/${appointmentID}?format=modal`);
    modalContentDIV.innerHTML = await response.text();
    const myModal = new bootstrap.Modal(document.getElementById("appointment_modal"));
    myModal.show();
}

// eine Abholung als abgeholt markieren oder umgekehrt
async function markCollected(button, appointment_id){
    const csrftoken = document.getElementsByName('csrfmiddlewaretoken').item(0).value
    var options = {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            credentials: 'same-origin',
            'X-CSRFToken': csrftoken
        },
        body: "is_collected=True"
    }
    if (button.value === "false") {
        options.body = "is_collected=False";
    }
    const url = "/appointment/"+ appointment_id + "/collected";
    await fetch(url, options);
    document.getElementById("ModalCloseButton").click();
    changeAppointmentPresentation(appointment_id, button.value);
}

// die Abholung nehmen und die Tabelle oder Liste anpassen
function changeAppointmentPresentation(appointment_id, new_status) {
    const type = document.getElementsByName("appointment_view_type")[0].id;
    const container = "status_" + appointment_id;
    const icon_collected = '<i class="bi bi-check-circle-fill text-success"></i>';
    const icon_not_collected = '<i class="bi bi-x-circle-fill text-danger"></i>';
    if (type === "collect") {
        if (new_status === "true") {
            document.getElementById(container).classList.remove("bg-warning");
            document.getElementById(container).classList.add("bg-success");
        } else {
            document.getElementById(container).classList.remove("bg-success");
            document.getElementById(container).classList.add("bg-warning");
        }
    }
    if (type === "list") {
        if (new_status === "true") {
            document.getElementById(container).innerHTML = icon_collected;
        } else {
            document.getElementById(container).innerHTML = icon_not_collected;
        }
    }
}

// Einblenden eines Fensters mit den Details eines Gebietes
async function showAreaDetails(areaID) {
    const modalContentDIV = document.getElementById("area_detail");
    const response = await fetch(`/area/${areaID}?format=modal`);
    modalContentDIV.innerHTML = await response.text();
    const myModal = new bootstrap.Modal(document.getElementById("area_modal"));
    myModal.show();
}

function getTimeslotName(timeslot) {
    var splitdate = timeslot.date.split("-");
    var date = splitdate[2]+'.'+splitdate[1]+'.'+splitdate[0].slice(2,4)
    return date +', '+ timeslot.time_from.slice(0,-3) + '-' + timeslot.time_to.slice(0,-3) + ' Uhr'
}

// Abrufen aller Zeitslots und ihrer Auslastungen für das Fahrzeug, das die Straße anfährt
async function loadTimeslotsForStreet(street) {
    const response = await fetch('/api/street');
    const streetList = await response.json();
    var streetObj = streetList.filter(obj => {return obj.name === street})[0];
    try {
        var area = streetObj.area.parent;
    } catch (error) {
        var area_list = await ((await fetch('/api/area?is_parent=true')).json());
        var area = area_list[0].id;
        alert(`Warnung! Straße ${streetObj.name} hat keine Gebietszuordnung. Es werden die Zeiträume & Auslastungen für ${area_list[0].name} angezeigt!`)
    }

    var timeslotList = await (await fetch(`/api/area/${area}/timeslots`)).json();
    var tsSelect = document.getElementById('timeslot');
    var innerHTML = '<option value="None">-----</option>'
    timeslotList.forEach(ts => {
        var attr = ""
        var fillcount = `Auslastung: ${ts.count}/${ts.appointment_max}`
        if (ts.count === ts.appointment_max) {
            attr = "disabled"
            fillcount = "AUSGEBUCHT!"
        }
        innerHTML += `<option value="${ts.timeslot.id}" ${attr}>${getTimeslotName(ts.timeslot)} - ${fillcount}</option>`;
    })
    tsSelect.innerHTML = innerHTML;
}

// Abrufen einer Liste mit Zeitraum-Vorschlägen auf Basis der Straße
async function getTimeslotSuggestions(street_name) {
    const suggestionDIV = document.getElementById("suggestion_list");
    const response = await fetch(`/timeslot/suggestion?street=${street_name}`)
    suggestionDIV.innerHTML = await response.text();
}

// Zeitslot anhand des Vorschlages auswählen
function acceptSuggestion(timeslot_id) {
    const dropDown = document.getElementById("timeslot")
    for (let i = 0; i < dropDown.options.length; i++) {
        if (dropDown.options[i].value == timeslot_id) {
            dropDown.options[i].selected = true;
            return;
        }
    }
}
