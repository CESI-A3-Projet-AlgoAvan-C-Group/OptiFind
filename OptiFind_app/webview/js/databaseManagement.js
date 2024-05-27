let db = '';
let dbVersion = 1;
let dbName = 'OptiFind';

var selectedGroup = {
    dbName: '',
    type: '',
    id: '',
    name: '',
    quantity: '',
    volume: '',
    weight: '',
}

let openRequest = indexedDB.open(dbName, dbVersion);

openRequest.onupgradeneeded = function (event) {
    db = event.target.result;

    if (!db.objectStoreNames.contains('packageGroups')) {
        db.createObjectStore('packageGroups', {keyPath: 'id', autoIncrement: true});
    }
    if (!db.objectStoreNames.contains('truckGroups')) {
        db.createObjectStore('truckGroups', {keyPath: 'id', autoIncrement: true});
    }
}

openRequest.onsuccess = function (event) {
    db = event.target.result;
    loadGroups();
}

openRequest.onerror = function () {
    alert('Error loading database');
}