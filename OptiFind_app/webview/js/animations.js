document.getElementById("ico-panel-hide").addEventListener("click", hidePanel)
document.getElementById("popup").style.display = "none";
changeMode('manual');
document.cookie = "etape=search";

function hidePanel() {
    let leftPanel = document.getElementById("left-panel")
    let containerSearch = document.getElementById("container-"+getCookie("etape"))
    let icoHide = document.getElementById("ico-panel-hide")
    if (containerSearch.style.display === "none") {
        containerSearch.style.display = "flex";
        leftPanel.style.width = "332px";
        icoHide.style.rotate = "0deg";
    } else {
        containerSearch.style.display = "none";
        leftPanel.style.width = "auto";
        icoHide.style.rotate = "180deg";
    }
}

function addGroup() {
    document.getElementById("btn-cancel-group").style.display = "flex";
    document.getElementById("btn-update-group").style.display = "none";
    document.getElementById("btn-create-group").style.display = "flex";
    document.getElementById("btn-delete-group").style.display = "none";
}

function changeGroup() {
    document.getElementById("btn-cancel-group").style.display = "none";
    document.getElementById("btn-update-group").style.display = "flex";
    document.getElementById("btn-create-group").style.display = "none";
    document.getElementById("btn-delete-group").style.display = "flex";
}

function showHidePopup() {
    let popup = document.getElementById("popup");
    document.getElementById("popup-text").innerText = selectedGroup.type + " group";
    document.getElementById("group-name").value = selectedGroup.name;
    document.getElementById("group-quantity").value = selectedGroup.quantity;
    document.getElementById("group-volume").value = selectedGroup.volume;
    document.getElementById("group-weight").value = selectedGroup.weight;
    if (popup.style.display === "none") {
        popup.style.display = "block";
    } else {
        popup.style.display = "none";
    }
}

function changeMode(mode) {
    changeCookieMode(mode);
    if (mode === 'manual') {
        document.getElementById("btn-type-selection-right").style.background = "#9DB2BF";
        document.getElementById("btn-type-selection-left").style.background = "#526D82";
        document.getElementById("manual-mode").style.display = "block";
        document.getElementById("assisted-mode").style.display = "none";
    } else {
        document.getElementById("btn-type-selection-right").style.background = "#526D82";
        document.getElementById("btn-type-selection-left").style.background = "#9DB2BF";
        document.getElementById("manual-mode").style.display = "none";
        document.getElementById("assisted-mode").style.display = "flex";
    }
}

function changeCookieMode(mode) {
    document.cookie = "mode=" + mode;
}

function getCookie(name) {
    // Add the = sign to the name and decode the cookie string
    let cookieArr = decodeURIComponent(document.cookie).split(';');

    // Loop through the array to find the cookie with the specified name
    for(let i = 0; i < cookieArr.length; i++) {
        let c = cookieArr[i];

        // Remove any leading whitespace
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }

        // If the cookie's name matches the specified name, return the value of the cookie
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }

    // If the cookie wasn't found, return an empty string
    return "";
}

function changeToResults() {
    document.getElementById("container-search").style.display = "none";
    document.getElementById("container-results").style.display = "flex";
    document.getElementById("mode-text").innerText = "Results";
}

function changeToSearch() {
    document.getElementById("container-search").style.display = "flex";
    document.getElementById("container-results").style.display = "none";
    document.getElementById("mode-text").innerText = "Search";
}