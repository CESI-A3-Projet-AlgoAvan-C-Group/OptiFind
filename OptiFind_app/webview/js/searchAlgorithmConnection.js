var socket = io.connect('http://' + document.domain + ':' + location.port); // creation de la connexion

socket.on('newLayerPoints', function (pointsJSON) {
    showPackages(pointsJSON);
});

socket.on('newLayerLine', function (linesJSON) {
    showPaths(linesJSON);
});

async function searchRequest() {
    changeToResults();
    let truckGroups = await getGroups('truckGroups');
    let packageGroups = await getGroups('packageGroups');

    // send request to flask search algorithm
    dispatcher(truckGroups, packageGroups);
}

function dispatcher(truckGroups, packageGroups) {
    let mapData = null;
    if (map.getSource('file-source')) {
        console.log("map.getSource found")
        mapData = map.getSource('file-source')._data;
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
        })
    }
}

function getPaths(truckGroups, packageGroups, mapData) {
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
    })
}

function backToSearch() {
    console.log("map layers", map.getStyle().layers)
    if (map.getSource('file-source')) {
        map.removeLayer('file-points');
        map.removeSource('file-source');
        document.getElementById('delete-file').style.color = '#DDE6ED';
        document.getElementById('package-container').style.display = 'flex';
    }
    document.getElementById('file').value = '';
    for (let i = 0; i < layerPointList.length; i++) {
        map.removeLayer(layerPointList[i]);
        map.removeSource(layerPointList[i]);
    }
    for (let i = 0; i < layerLineList.length; i++) {
        map.removeLayer(layerLineList[i]);
        map.removeSource(layerLineList[i]);
    }
    layerPointList = [];
    layerLineList = [];
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
