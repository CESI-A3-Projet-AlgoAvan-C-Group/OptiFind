function searchRequest() {
    changeToResults();
    if (document.cookie.includes('mode=manual')) {
        let truckGroups = getGroups('truckGroups');
        let packageGroups = getGroups('packageGroups');

        // send request to flask search algorithm
        getPaths('manual',truckGroups, packageGroups);
    } else {
        // send request to flask search algorithm
        getPaths('assisted');
    }
}

function getPaths(searchMode,truckGroups, packageGroups) {
    fetch('/get_paths', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            truckGroups,
            packageGroups,
            mapData: map.getSource('uploaded-source')._data
        })
    }).then(response => response.json())
        .then(data => {
            showPaths(data);
        }
        );
}

function backToSearch() {
    map.removeLayer('uploaded-paths');
    map.removeSource('python-source');
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