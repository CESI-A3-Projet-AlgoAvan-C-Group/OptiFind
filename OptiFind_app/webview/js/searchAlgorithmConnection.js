function searchRequest() {
    changeToResults();
    if (document.cookie.includes('mode=manual')) {
        let truckGroups = getGroups('truckGroups');
        let packageGroups = getGroups('packageGroups');

        // send request to flask search algorithm
        getPaths(truckGroups, packageGroups);

    }
}

function backToSearch() {
    changeToSearch();
}

function getGroups(groupType) {
    let transaction = db.transaction(groupType, 'readonly');
    let groups = transaction.objectStore(groupType);
    let request = groups.getAll();
    request.onsuccess = function () {
        return request.result;
    }
}