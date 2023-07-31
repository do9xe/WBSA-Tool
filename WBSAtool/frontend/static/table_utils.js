/*
========================================================================================================
Table Utils - a collection of functions in order to do some stuff with tables.

1) a "select all" checkbox in the table header
In order to use this functionality just add an <input type="checkbox" name="select_all"> to your
table header and an <input type="checkbox" name="select_row"> into every line of your table.
if the table is part of a form you can set values for each row and collect the data on submit.

========================================================================================================
 */


// returns all checkboxes with a specific name within the given HTML element
function getCheckboxesByName(html_element, box_name) {
    const input_ele_list = html_element.getElementsByTagName("input");
    var box_list = [];
    for (let i=0; i<input_ele_list.length; i++) {
        if (input_ele_list[i].type === "checkbox" && input_ele_list[i].name === box_name) {
            box_list.push(input_ele_list[i]);
        }
    }
    return box_list;
}

function getParentTableElement(html_element) {
    var current_parent = html_element.parentElement;
    while (true) {
        if (current_parent.tagName === "TABLE") {
            console.log("table found");
            return current_parent;
        }
        if (current_parent.tagName === "BODY"){
            console.log("reached body, aborting")
            return;
        }
        current_parent = current_parent.parentElement;
    }
}

function getParentTableCell(html_element) {
    var current_parent = html_element.parentElement;
    while (true) {
        if (current_parent.tagName === ("TH"||"TD")) {
            console.log("tablecell found");
            return current_parent;
        }
        if (current_parent.tagName === "BODY"){
            console.log("reached body, aborting")
            return;
        }
        current_parent = current_parent.parentElement;
    }
}

function selectAll(current_table){
    var ele= getCheckboxesByName(current_table, 'select_row');
    for(var i=0; i<ele.length; i++){
        ele[i].checked=true;
    }
}
function deSelectAll(current_table){
    var ele= getCheckboxesByName(current_table, 'select_row');
    for(var i=0; i<ele.length; i++){
        ele[i].checked=false;
    }
}
function countAndCheck(current_table){
    var ele = getCheckboxesByName(current_table, 'select_row');
    var count = 0;
    for(var i=0; i<ele.length; i++){
        if(ele[i].checked === true) {
            count++;
        }
    }
    if (ele.length === count){
        const select_all_list = getCheckboxesByName(current_table, 'select_all');
        for(var i=0; i<ele.length; i++){
            select_all_list[i].checked = true;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // get all the tables that are within the page
    const all_tables = document.getElementsByTagName("table");
    // loop through all the tables to set individual event-listener
    for (let i=0; i<all_tables.length; i++) {
        const table = all_tables[i];
        // get all the inputs and loop through them
        const input_ele_list = table.getElementsByTagName("input");
        for (let j=0; j<input_ele_list.length; j++) {
            const input_ele = input_ele_list[j];
            // if the name of the input is select_all, add an EventListener, that (un)checks all the boxes
            if (input_ele.name === "select_all") {
                input_ele.addEventListener('change', function (event) {
                    if (input_ele.checked === true) {
                        selectAll(table);
                        const string = "select all inputes" + " " + input_ele.value;
                        console.log(string);
                    }
                    else {
                        deSelectAll(table);
                        const string = "deSelect all inputes" + " " + input_ele.value;
                        console.log(string);
                    }
                });
            }
            // if the name of the input is select_row, add an EventListener that counts & checks boxes
            if (input_ele.name === "select_row" && input_ele.type === "checkbox") {
                input_ele.addEventListener('change', function(event) {
                    const parent_table = getParentTableElement(this);
                    if (this.checked === true) {
                        console.log("count and check boxes");
                        countAndCheck(parent_table);
                    }
                    if (this.checked === false) {
                        console.log("uncheck the select_all box");
                        const table_input_list = parent_table.getElementsByTagName("input");
                        for (let k=0; k<table_input_list.length; k++) {
                            if (table_input_list[k].type === "checkbox" && table_input_list[k].name === "select_all") {
                                table_input_list[k].checked = false;
                            }
                        }
                    }
                });
            }
        }
    }
});


// Utils for searching & filtering a table
document.addEventListener('DOMContentLoaded', () => {
    // first, find all divs with the name "filter-column"
    let filter_col_list = document.getElementsByName("filter-col");
    for (let i=0; i<filter_col_list.length; i++) {
        //now we place a search Icon into every div with the name "filter-column"
        const searchIcon = '<i class="bi bi-search text-secondary ms-1" onclick="displaySearch(this)"></i>';
        filter_col_list[i].innerHTML = searchIcon;
        filter_col_list[i].style = "display:inline;";
    }
});

function displaySearch(sourceElement) {
    let searchBar = '<i class="bi ms-1 bi-x-circle-fill" onclick="removeFilter(this)"></i>' +
        '<div class="bg-light shadow-sm rounded-1" style="z-index:9;position:absolute;">' +
        '<div class="input-group input-group-sm px-1 py-1">' +
        '<input class="form-control" type="text" id="currentSearchInput">' +
        '<button class="btn btn-outline-success" type="button" id="currentSearchButton" onclick="searchCol(this)"><i class="bi bi-search"></i></button>' +
        '</div></div>';
    sourceElement.parentElement.id = "currentSearchWindow";
    sourceElement.outerHTML = searchBar;
    document.getElementById("currentSearchInput").addEventListener('keydown',(e) => {
        if (e.key === "Enter") {
            document.getElementById("currentSearchButton").click();
        }
    });
}

function searchCol(sourceElement) {
    // get the search term from the Element
    let searchTerm = sourceElement.parentElement.getElementsByTagName("input")[0].value;
    if (searchTerm.length === 0) {
        return;
    }
    // actually filter the table
    filterTable(sourceElement, searchTerm);
    // after filtering, place a small pill badge with the search term in out table header
    let searchTermIcon = '<span class="badge rounded-pill text-bg-secondary">'+ searchTerm + '<i class="bi ms-1 bi-x-circle-fill" onclick="removeFilter(this)"></i></span>';
    let x = document.getElementById("currentSearchWindow");
    x.innerHTML = searchTermIcon;
    x.id = "";
}

function removeFilter(sourceElement) {
    //show the full table
    showFullTable(sourceElement);
    // now re-place the search icon
    const searchIcon = '<i class="bi bi-search text-secondary ms-1" onclick="displaySearch(this)"></i>';
    if (sourceElement.parentElement.nodeName === "DIV") {
        sourceElement.parentElement.innerHTML = searchIcon;
    }
    else {
        sourceElement.parentElement.outerHTML = searchIcon;
    }
}

function filterTable(sourceElement, searchTerm) {
    // find out which table we are in before we cut the roots
    let table = getParentTableElement(sourceElement);
    let colIndex = getParentTableCell(sourceElement).cellIndex;
    let rows = table.getElementsByTagName("tr");
    for (let i=0; i<rows.length;i++) {
        let this_td = rows[i].getElementsByTagName("td")[colIndex];
        if (this_td) {
            let txtValue = this_td.textContent || this_td.innerText;
            if (txtValue.toUpperCase().indexOf(searchTerm.toUpperCase()) > -1) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
    }
}

function showFullTable(sourceElement) {
    let table = getParentTableElement(sourceElement);
    let rows = table.getElementsByTagName("tr");
    for (let i=0; i<rows.length;i++) {
        rows[i].style.display = "";
    }
}