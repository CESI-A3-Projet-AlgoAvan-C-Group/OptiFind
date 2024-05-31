document.getElementById("ico-add-package-group").addEventListener("click", addPackageGroup)
document.getElementById("ico-add-truck-group").addEventListener("click", addTruckGroup)

var selectedGroup = {
    dbName: '',
    type: '',
    id: '',
    name: '',
    quantity: '',
    volume: '',
    weight: '',
}

function loadGroups() {
    let packageContainer = document.getElementById("package-container");
    while (packageContainer.firstChild) {
        packageContainer.removeChild(packageContainer.firstChild);
    }
    let truckContainer = document.getElementById("truck-container");
    while (truckContainer.firstChild) {
        truckContainer.removeChild(truckContainer.firstChild);
    }
    let transaction = db.transaction('packageGroups', 'readonly');
    let packageGroups = transaction.objectStore('packageGroups');
    let packageRequest = packageGroups.getAll();
    packageRequest.onsuccess = function () {
        let groups = packageRequest.result;
        for (let i = 0; i < groups.length; i++) {
            selectedGroup = {
                dbName: 'packageGroups',
                type: 'package',
                id: groups[i].id,
                name: groups[i].name,
                quantity: groups[i].quantity,
                volume: groups[i].volume,
                weight: groups[i].weight,
            }
            addGroupToHtml();
        }
    }
    transaction = db.transaction('truckGroups', 'readonly');
    let truckGroups = transaction.objectStore('truckGroups');
    let truckRequest = truckGroups.getAll();
    truckRequest.onsuccess = function () {
        let groups = truckRequest.result;
        for (let i = 0; i < groups.length; i++) {
            selectedGroup = {
                dbName: 'truckGroups',
                type: 'truck',
                id: groups[i].id,
                name: groups[i].name,
                quantity: groups[i].quantity,
                volume: groups[i].volume,
                weight: groups[i].weight,
            }
            addGroupToHtml();
        }
    }
}

function addTruckGroup() {
    selectedGroup = {
        dbName: 'truckGroups',
        type: 'truck',
        id: '',
        name: '',
        quantity: '',
        volume: '',
        weight: ''
    };
    addGroup();
    showHidePopup();
}

function addPackageGroup() {
    selectedGroup = {
        dbName: 'packageGroups',
        type: 'package',
        id: '',
        name: '',
        quantity: '',
        volume: '',
        weight: ''
    };
    addGroup();
    showHidePopup();
}

function editGroup(idName) {
    let type = idName.split("-")[0];
    let id = parseInt(idName.split("-")[1]);
    let dbName = type + 'Groups';
    let transaction = db.transaction(dbName, 'readonly');
    let groups = transaction.objectStore(dbName);
    let request = groups.get(parseInt(id));
    request.onsuccess = function () {
        selectedGroup.dbName = dbName;
        selectedGroup.type = type;
        selectedGroup.id = request.result.id;
        selectedGroup.name = request.result.name;
        selectedGroup.quantity = request.result.quantity;
        selectedGroup.volume = request.result.volume;
        selectedGroup.weight = request.result.weight;
        changeGroup();
        showHidePopup();
    }
}

function updateGroup() {
    getDbConnection().put({
        id: selectedGroup.id,
        name: selectedGroup.name,
        quantity: selectedGroup.quantity,
        volume: selectedGroup.volume,
        weight: selectedGroup.weight
    }).onsuccess = function () {
        loadGroups();
        showHidePopup();
    }
}

function cancelGroup() {
    showHidePopup();
}

function deleteGroup() {
    let transaction = db.transaction(selectedGroup.dbName, 'readwrite');
    let groups = transaction.objectStore(selectedGroup.dbName);
    groups.delete(selectedGroup.id).onsuccess = function () {
        loadGroups();
        showHidePopup();
    }
}

function createGroup() {
    getDbConnection().add({
        name: selectedGroup.name,
        quantity: selectedGroup.quantity,
        volume: selectedGroup.volume,
        weight: selectedGroup.weight
    }).onsuccess = function (event) {
        selectedGroup.id = event.target.result;
        loadGroups();
        showHidePopup();
    }
}

function addGroupToHtml() {
    let type = selectedGroup.type;
    let groupContainer = document.getElementById(type + "-container");
    let groupDiv = document.createElement("div");
    groupDiv.classList.add("experiment");
    groupDiv.id = type + "-" + selectedGroup.id;
    let name = document.createElement("h4");
    name.innerText = selectedGroup.name;
    name.classList.add("experiment-txt");
    groupDiv.appendChild(name);
    let quantity = document.createElement("p");
    quantity.innerText = selectedGroup.quantity;
    quantity.classList.add("experiment-txt");
    groupDiv.appendChild(quantity);
    let volume = document.createElement("p");
    volume.innerText = selectedGroup.volume;
    volume.classList.add("experiment-txt");
    groupDiv.appendChild(volume);
    let weight = document.createElement("p");
    weight.innerText = selectedGroup.weight;
    weight.classList.add("experiment-txt");
    groupDiv.appendChild(weight);
    groupContainer.appendChild(groupDiv);
    groupDiv.addEventListener("click", function () {
        editGroup(this.id)
    });
}

function getDbConnection() {
    let transaction = db.transaction(selectedGroup.dbName, 'readwrite');
    let groups = transaction.objectStore(selectedGroup.dbName);
    selectedGroup.name = document.getElementById('group-name').value;
    selectedGroup.quantity = document.getElementById('group-quantity').value;
    selectedGroup.volume = document.getElementById('group-volume').value;
    selectedGroup.weight = document.getElementById('group-weight').value;
    return groups;
}