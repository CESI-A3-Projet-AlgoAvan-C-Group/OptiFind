async function searchRequest() {
    changeToResults();
    let truckGroups = await getGroups('truckGroups');
    let packageGroups = await getGroups('packageGroups');

    // send request to flask search algorithm
    getPaths(truckGroups, packageGroups);
}

function getPaths( truckGroups, packageGroups) {
    let mapData = null;
    if ( map.getSource('uploaded-source') ) {
        mapData = map.getSource('uploaded-source')._data;
    }
    fetch('/get_paths', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            startCity: document.getElementById('start-city').value,
            truckGroups: truckGroups,
            packageGroups: packageGroups,
            mapData: mapData
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
    // get the data from index db and return it as an array
    let transaction = db.transaction(groupType, 'readonly');
    let Groups = transaction.objectStore(groupType);
    let request = Groups.getAll();
    // wait request to finish and return the result
    return new Promise(resolve => {
        request.onsuccess = function () {
            resolve(request.result);
        }
    });
}
