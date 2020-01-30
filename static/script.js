const MAX_SELECTED = 4;

function select_image (e) {
    let selectedList = load("selectedList", []);
    let element = e.currentTarget.parentElement.parentElement;
    let nextButton = document.querySelector("#nextButton");

    // if element is already selected
    if (element.classList.contains("selected")) {
        // deselect it
        element.classList.remove("selected");
        // and remove it from the list
        remove(selectedList, element.id);

        // disable button when last image has been deselected
        if (selectedList.length < 1) {
            nextButton.classList.add("disabled");
        }
    } else {
        if (selectedList.length < MAX_SELECTED) {
            // select it
            element.classList.add("selected");
            // and add it to the list
            selectedList.push(element.id);

            // enable button if it isn't
            if (nextButton.classList.contains("disabled")) {
                nextButton.classList.remove("disabled");
            }
        } else {
            alert("Too many selected"); //TODO
        }
    }

    // store updated counter and list
    store("selectedList", selectedList);
}

function next (e) {
    // assert that button is clickable
    if (load("selectedList",[]).length < 1) {
        return null;
    }

    // construct hidden form
    let form = document.createElement("form");
    form.action = "/thank-you";
    form.method = "POST";
    let input = document.createElement("input");
    input.type = "hidden";
    input.name = "selected_list";
    input.value = JSON.stringify(load("selectedList"));
    form.appendChild(input);
    document.querySelector("#hiddenForm").appendChild(form);
    form.submit();
}

// remove element from array (removes inplace, due to pass by reference)
function remove (array, el) {
    i = array.indexOf(el);
    array.splice(i, 1);
    return array;
}

// load from localStorage with default and as JSON
function load (key, _default) {
    let value = window.localStorage.getItem(key);
    if (value !== null) {
        return JSON.parse(value);
    }
    return _default;
}

// alias for localStorage.setItem with array support
function store (key, value) {
    value = JSON.stringify(value);
    return window.localStorage.setItem(key, value);
}

function create_indicator(n) {
    let indicator = document.createElement("div");
    indicator.textContent = n.toString();
    indicator.id = "progress-indicator-"+n.toString();
    indicator.classList.add("indicator");
    return indicator;
}

// execute the following code only after the page has loaded
document.addEventListener("DOMContentLoaded", () => {

    // make images selectable
    document.querySelectorAll("#gallery .main-image").forEach(e => {
        e.onclick = select_image;
    });

    // make next button clickable
    document.querySelector("#nextButton").onclick = next;

    // load image status
    let selectedList = load("selectedList",[]);
    for (img_id of selectedList) {
        document.getElementById(img_id).classList.add("selected");
    }

    // determine button status
    if (selectedList.length > 0) {
        nextButton.classList.remove("disabled");
    }

    // add progress indicators
    let progress_bar = document.querySelector("#progress");
    for (let i = 0; i < MAX_SELECTED; i++) {
        progress_bar.appendChild(create_indicator(i+1));
    }
});
