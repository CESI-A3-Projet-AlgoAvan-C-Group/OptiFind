async function searchRequest() {
    changeToResults();
    let truckGroups = await getGroups('truckGroups');
    let packageGroups = await getGroups('packageGroups');

    // send request to flask search algorithm
    dispatcher(truckGroups, packageGroups);
}

function dispatcher(truckGroups, packageGroups) {
    let mapData = null;
    if (map.getSource('uploaded-source')) {
        console.log("map.getSource found")
        mapData = map.getSource('uploaded-source')._data;
        console.log(mapData)
        getPaths(truckGroups, packageGroups, mapData);
    } else {
        console.log("map.getSource not found")
        fetch('/get_packages', {
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
            showPackages(data);
            getPaths(truckGroups, packageGroups ,data);
        })
    }
}

function getPaths( truckGroups, packageGroups, mapData) {
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
    map.removeLayer('uploaded-points')
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
