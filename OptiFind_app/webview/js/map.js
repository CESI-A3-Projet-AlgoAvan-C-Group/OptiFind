const map = new maplibregl.Map({
    container: 'map',
    style: '../assets/mapstyle2.json',
    center: [-2, 47],
    zoom: 5.4
});

function resetView() {
    map.flyTo({
            // These options control the ending camera position: centered at
            // the target, at zoom level 9, and north up.
            center: [-2, 47],
            zoom: 5.4,
            bearing: 0,

            // These options control the flight curve, making it move
            // slowly and zoom out almost completely before starting
            // to pan.
            speed: 10, // make the flying slow
            curve: 1, // change the speed at which it zooms out

            // This can be any easing function: it takes a number between
            // 0 and 1 and returns another number between 0 and 1.
            easing (t) {
                return t;
            },

            // this animation is considered essential with respect to prefers-reduced-motion
            essential: true
        });
}