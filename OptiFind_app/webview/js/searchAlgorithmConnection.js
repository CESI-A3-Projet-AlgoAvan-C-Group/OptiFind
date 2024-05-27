function searchRequest() {
    changeToResults();
    if (document.cookie.includes('mode=manual')) {
        let trucks = getGroups('truckGroups');
        let packages = getGroups('packageGroups');

        // send request to flask search algorithm

        // display results

        showPaths();

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