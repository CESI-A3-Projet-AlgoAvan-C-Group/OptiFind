const MAPTILER_KEY = 'get_your_own_OpIi9ZULNHzrESv6T2vL';
document
    .getElementById('file')
    .addEventListener('change', handleFileSelect, false);

document.getElementById('delete-file').addEventListener('click', () => {
    if (map.getSource('file-source')) {
        map.removeLayer('file-points');
        map.removeSource('file-source');
        document.getElementById('delete-file').style.color = '#DDE6ED';
        document.getElementById('package-container').style.display = 'flex';
    }
    // reset the input
    document.getElementById('file').value = '';
});

const map = new maplibregl.Map({
    container: 'map',
    style: '../assets/mapstyle2.json',
    center: [-2, 47],
    orientation: 0,
    zoom: 5.4,
    antialias: true
})

let layerPointList = [];
let layerLineList = [];

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
                'fill-extrusion-color': ['case', ['==', ['get', 'type'], 'building:part'], '#d3d3d3', '#d3d3d3'],
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
                ],
                'fill-extrusion-opacity': 1
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

        if (map.getSource('file-source')) {
            map.removeLayer('file-points');
            map.removeSource('file-source');
        }
        // Add as source to the map
        map.addSource('file-source', {
            'type': 'geojson',
            'data': geoJSONcontent
        });

        map.addLayer({
            'id': 'file-points',
            'type': 'circle',
            'source': 'file-source',
            'paint': {
                'circle-radius': 2,
                'circle-color': '#FFD580'
            },
            // or points add more layers with different filters
            'filter': ['==', '$type', 'Point']
        });

        map.on('click', 'file-points', (e) => {
            const coordinates = e.features[0].geometry.coordinates.slice();
            const city = e.features[0].properties.city;
            const id = e.features[0].properties.package_id;
            const weight = e.features[0].properties.weight;
            const volume = e.features[0].properties.volume;

            // Ensure that if the map is zoomed out such that multiple
            // copies of the feature are visible, the popup appears
            // over the copy being pointed to.
            while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
            }

            new maplibregl.Popup()
                .setLngLat(coordinates)
                .setHTML(`<h3>Package ${id}</h3><p>City: ${city}</p><p>Weight: ${weight} kg</p><p>Volume: ${volume} m³</p>`)
                .addTo(map);
        });

        // Change the cursor to a pointer when the mouse is over the places layer.
        map.on('mouseenter', 'places', () => {
            map.getCanvas().style.cursor = 'pointer';
        });

        // Change it back to a pointer when it leaves.
        map.on('mouseleave', 'places', () => {
            map.getCanvas().style.cursor = '';
        });
        document.getElementById('package-container').style.display = 'none';
    };

    // Read the GeoJSON as text
    reader.readAsText(file, 'UTF-8');
    document.getElementById('delete-file').style.color = '#27374D';
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
        speed: 7, // make the flying slow
        curve: 2, // change the speed at which it zooms out

        // This can be any easing function: it takes a number between
        // 0 and 1 and returns another number between 0 and 1.
        easing(t) {
            return t;
        },

        // this animation is considered essential with respect to prefers-reduced-motion
        essential: true
    });
}

function showPackages(jsonData) {
    const geoJSONcontent = typeof jsonData === 'string' ? JSON.parse(jsonData) : jsonData;
    map.addLayer({
        'id': 'python-points-'+layerPointList.length,
        'type': 'circle',
        'source': {
            'type': 'geojson',
            'data': geoJSONcontent
        },
        'paint': {
            'circle-radius': 2,
            'circle-color': '#FFD580'
        },
        // or points add more layers with different filters
        'filter': ['==', '$type', 'Point']
    });
    layerLineList.push('python-points-'+layerPointList.length);
    map.on('click', 'python-points-'+layerPointList.length, (e) => {
            const coordinates = e.features[0].geometry.coordinates.slice();
            const city = e.features[0].properties.city;
            const id = e.features[0].properties.package_id;
            const weight = e.features[0].properties.weight;
            const volume = e.features[0].properties.volume;

            // Ensure that if the map is zoomed out such that multiple
            // copies of the feature are visible, the popup appears
            // over the copy being pointed to.
            while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
            }

            new maplibregl.Popup()
                .setLngLat(coordinates)
                .setHTML(`<h3>Package ${id}</h3><p>City: ${city}</p><p>Weight: ${weight} kg</p><p>Volume: ${volume} m³</p>`)
                .addTo(map);
        });
}

function showPaths(jsonData) {
    const geoJSONcontent = typeof jsonData === 'string' ? JSON.parse(jsonData) : jsonData;

    // Add as source to the map

    map.addLayer({
        'id': 'python-paths-'+layerLineList.length,
        'type': 'line',
        'source': {
            'type': 'geojson',
            'data': geoJSONcontent
        },
        'paint': {
            'line-color': '#ff0000',
            'line-width': 2
        },
        // or points add more layers with different filters
        'filter': ['==', '$type', 'LineString']
    });
    layerLineList.push('python-paths-'+layerLineList.length);
}

