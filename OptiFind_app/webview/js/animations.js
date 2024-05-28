document.getElementById("ico-panel-hide").addEventListener("click", hidePanel)
document.getElementById("popup").style.display = "none";
let stepView = "search";
let nameUpper = {truck: "Truck", package: "Package"};

function hidePanel() {
    let leftPanel = document.getElementById("left-panel")
    let containerSearch = document.getElementById("container-"+stepView)
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
    document.getElementById("popup-text").innerText = nameUpper[selectedGroup.type] + " group";
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

function changeToResults() {
    stepView = "results";
    document.getElementById("container-search").style.display = "none";
    document.getElementById("container-results").style.display = "flex";
    document.getElementById("mode-text").innerText = "Results";
}

function changeToSearch() {
    stepView = "search";
    document.getElementById("container-search").style.display = "flex";
    document.getElementById("container-results").style.display = "none";
    document.getElementById("mode-text").innerText = "Search";
}