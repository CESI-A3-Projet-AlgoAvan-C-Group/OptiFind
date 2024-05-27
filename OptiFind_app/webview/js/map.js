const MAPTILER_KEY = 'get_your_own_OpIi9ZULNHzrESv6T2vL';
document
    .getElementById('file')
    .addEventListener('change', handleFileSelect, false);

const map = new maplibregl.Map({
    container: 'map',
    style: '../assets/mapstyle2.json',
    center: [-2, 47],
    orientation: 0,
    zoom: 5.4,
    antialias: true
})

function getPaths(truckGroups, packageGroups) {
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

map.on('load', () => {
    // Insert the layer beneath any symbol layer.
    const layers = map.getStyle().layers;

    let labelLayerId;
    for (let i = 0; i < layers.length; i++) {
        if (layers[i].type === 'symbol' && layers[i].layout['text-field']) {
            labelLayerId = layers[i].id;
            break;
        }
    }

    map.addSource('openmaptiles', {
        url: `https://api.maptiler.com/tiles/v3/tiles.json?key=${MAPTILER_KEY}`,
        type: 'vector',
    });

    map.addLayer(
        {
            'id': '3d-buildings',
            'source': 'openmaptiles',
            'source-layer': 'building',
            'type': 'fill-extrusion',
            'minzoom': 15,
            'paint': {
                'fill-extrusion-color': [
                    'case',
                    ['==', ['get', 'type'], 'building'],
                    'rgb(200, 200, 200)',
                    'rgb(200, 200, 200)'
                ],
                'fill-extrusion-height': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    15,
                    0,
                    16,
                    ['get', 'render_height']
                ],
                'fill-extrusion-base': ['case',
                    ['>=', ['get', 'zoom'], 16],
                    ['get', 'render_min_height'], 0
                ]
            }
        },
        labelLayerId
    );
});

function handleFileSelect(evt) {
    const file = evt.target.files[0]; // Read first selected file

    const reader = new FileReader();

    reader.onload = function (theFile) {
        // Parse as (geo)JSON
        const geoJSONcontent = JSON.parse(theFile.target.result);

        // Add as source to the map
        map.addSource('uploaded-source', {
            'type': 'geojson',
            'data': geoJSONcontent
        });

        map.addLayer({
            'id': 'uploaded-points',
            'type': 'circle',
            'source': 'uploaded-source',
            'layout': {},
            'paint': {
                'circle-radius': 5,
                'circle-color': '#007cbf'
            },
            // or points add more layers with different filters
            'filter': ['==', '$type', 'Point']
        });

    };

    // Read the GeoJSON as text
    reader.readAsText(file, 'UTF-8');
}

function resetView() {
    map.flyTo({
        // These options control the ending camera position: centered at
        // the target, at zoom level 9, and north up.
        center: [-2, 47],
        zoom: 5.4,
        bearing: 0,
        // reset the pitch to 0
        pitch: 0,
        // These options control the flight curve, making it move
        // slowly and zoom out almost completely before starting
        // to pan.
        speed: 10, // make the flying slow
        curve: 1, // change the speed at which it zooms out

        // This can be any easing function: it takes a number between
        // 0 and 1 and returns another number between 0 and 1.
        easing(t) {
            return t;
        },

        // this animation is considered essential with respect to prefers-reduced-motion
        essential: true
    });
}

function showPaths(jsonData) {
    const geoJSONcontent = typeof jsonData === 'string' ? JSON.parse(jsonData) : jsonData;

    // Add as source to the map
    map.addSource('python-source', {
        'type': 'geojson',
        'data': geoJSONcontent
    });

    map.addLayer({
        'id': 'uploaded-paths',
        'type': 'line',
        'source': 'python-source',
        'paint': {
            'line-color': '#ff0000',
            'line-width': 2
        },
        // or points add more layers with different filters
        'filter': ['==', '$type', 'LineString']
    });
}