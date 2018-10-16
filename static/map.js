var mapsPlaceholder = []
L.Map.addInitHook(function () {
    mapsPlaceholder.push(this);
});
function GetValues() {
    $('#processing').removeClass("hidden");
    if(mapsPlaceholder.length == 1) {mapsPlaceholder[0].remove()}
    $('#map').attr("class", "");
    var type = $('input[name="optradio"]:checked').val();
    
    var subtype = "unphotographed";
    if ($('#nafocene')[0].checked && $('#nenafocene')[0].checked) subtype = "all";
    else if ($('#nafocene')[0].checked && !$('#nenafocene')[0].checked) subtype = "photographed";
    else if (!$('#nafocene')[0].checked && $('#nenafocene')[0].checked) subtype = "unphotographed";

    var payload = {
        type: type,
        subtype: subtype,
        radius: $('#radius').val(),
    };

    if (type == "article") {
        payload["article"] = $('input[name="wikiSearchPole"]').val();
        payload["project"] = $('#project-language').val() + $('#project-project').val();
    } else if (type == "item") {
        payload["item"] = $('input[name="cislo"]').val();
    } else if (type == "coordinate") {
        payload["lat"] = $('input[name="lat"]').val();
        payload["lon"] = $('input[name="lon"]').val();
    }

    $.get('map', payload, function(data) {
        $('#map').html("").addClass("bigmap");
        $('#processing').addClass("hidden");
        var style = 'osm-intl';
        var server = 'https://maps.wikimedia.org/';

        var map = L.map('map');
        map.setView([data.lat, data.lon], 13);
        L.tileLayer(server + style + '/{z}/{x}/{y}.png', {
                    maxZoom: 18,
                    id: 'wikipedia-map-01',
                    attribution: 'Wikimedia maps beta | Map data &copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
        }).addTo(map);

        var overlays = {};
        for(var layer in data.wikidata)
        {
            var markers = L.markerClusterGroup();
            var markerHtmlStyles = `
            background-color: #${data.wikidata[layer].color};
            width: 3rem;
            height: 3rem;
            display: block;
            left: -1.5rem;
            top: -1.5rem;
            position: relative;
            border-radius: 3rem 3rem 0;
            transform: rotate(45deg);
            border: 1px solid #FFFFFF`;
            var icon = L.divIcon({
                className: "my-custom-pin",
                iconAnchor: [0, 24],
                labelAnchor: [-6, 0],
                popupAnchor: [0, -36],
                html: `<span style="${markerHtmlStyles}" />`
            });
            for(var i = 0; i < data.wikidata[layer].points.length; i++)
            {
                var point = data.wikidata[layer].points[i];
                var marker = L.marker(new L.LatLng(point.lat, point.lon), {
                    icon: icon
                });
                marker.bindPopup(`<a href="${point.url}">${point.name}</a>`);
                markers.addLayer(marker);
            }
            overlays[data.wikidata[layer].html_name] = markers.addTo(map);
        }
        L.control.layers(null, overlays, { collapsed: false }).addTo(map);

        $.get("stats", function (data, status) { $('#statnum').text(data) })
    })
}
