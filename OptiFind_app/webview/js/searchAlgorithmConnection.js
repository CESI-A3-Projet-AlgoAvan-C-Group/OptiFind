async function searchRequest() {
    changeToResults();
    if (document.cookie.includes('mode=manual')) {
        let truckGroups = await getGroups('truckGroups');
        let packageGroups = await getGroups('packageGroups');

        // send request to flask search algorithm
        getPaths('manual', truckGroups, packageGroups);
    } else {
        // send request to flask search algorithm
        getPaths('assisted');
    }
}

function getPaths(searchMode, truckGroups, packageGroups) {
    console.log(truckGroups);
    console.log(packageGroups);
    fetch('/get_paths', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            searchMode: searchMode,
            truckGroups: truckGroups,
            packageGroups: packageGroups
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