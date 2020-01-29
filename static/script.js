const MAX_SELECTED = 4;

function select_image (e) {
    let selectedList = load("selectedList", []);
    console.log(selectedList);
    let element = e.toElement;

    // if element is already selected
    if (element.classList.contains("selected")) {
        // deselect it
        element.classList.remove("selected");
        // and remove it from the list
        remove(selectedList, element.parentElement.id);
    } else {
        if (selectedList.length < MAX_SELECTED) {
            // select it
            element.classList.add("selected");
            // and add it to the list
            selectedList.push(element.parentElement.id);
        } else {
            alert("Too many selected"); //TODO
        }
    }

    // store updated counter and list
    store("selectedList", selectedList);
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

// execute the following code only after the page has loaded
document.addEventListener("DOMContentLoaded", () => {

    // make images selectable
    document.querySelectorAll("#gallery img").forEach(e => {
        e.onclick = select_image;
    });


});
