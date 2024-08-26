var map = L.map('map').setView([51.254539, -1.604310], 8); // Center coordinates and zoom level
L.tileLayer('http://{s}.google.com/vt?lyrs=p&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
}).addTo(map);

var airplaneIcon = L.icon({
    iconUrl: '../static/img/airplane.png',
    iconSize: [36, 36],
    iconAnchor: [18, 18]
});

var airplaneIconSel = L.icon({
    iconUrl: '../static/img/airplane-selected.png',
    iconSize: [36, 36],
    iconAnchor: [18, 18]
});
