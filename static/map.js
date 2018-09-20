function GetValues() {
    $('#map').html("<h1>Processing...</h1>");
    var type = $('input[name="optradio"]:checked').val();
    
    var subtype = "unphotographed";
    if ($('#nafocene')[0].checked && $('#nenafocene')[0].checked) subtype = "all";
    else if ($('#nafocene')[0].checked && !$('#nenafocene')[0].checked) subtype = "unphotographed";
    else if (!$('#nafocene')[0].checked && $('#nenafocene')[0].checked) subtype = "photographed";

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
        payload["lat"] = $('input[name="cislo"]').val();
        payload["lon"] = $('input[name="lon"]').val();
    }

    $.get('map', payload, function(data) {
        $('#map').html("").addClass("bigmap");
        var style = 'osm-intl';
        var server = 'https://maps.wikimedia.org/';

        var map = L.map('map');
        map.setView([50, 16], 7);
        L.tileLayer(server + style + '/{z}/{x}/{y}.png', {
                    maxZoom: 18,
                    id: 'wikipedia-map-01',
                    attribution: 'Wikimedia maps beta | Map data &copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
        }).addTo(map);

        var markers = L.markerClusterGroup();
        for(var i = 0; i < data.results.bindings.length; i++)
        {
            var pointData = data.results.bindings[i];
            var coor = pointData.coord.value.replace("Point(", "").replace(")", "").split(" ");
            if(pointData.rgb) {
                var markerHtmlStyles = `
                background-color: #${pointData.rgb.value};
                width: 3rem;
                height: 3rem;
                display: block;
                left: -1.5rem;
                top: -1.5rem;
                position: relative;
                border-radius: 3rem 3rem 0;
                transform: rotate(45deg);
                border: 1px solid #FFFFFF`;
            } else {
                continue;
            }
            var marker = L.marker(new L.LatLng(coor[1], coor[0]), {
                icon: L.divIcon({
                    className: "my-custom-pin",
                    iconAnchor: [0, 24],
                    labelAnchor: [-6, 0],
                    popupAnchor: [0, -36],
                    html: `<span style="${markerHtmlStyles}" />`                  
                }),
                title: pointData.itemLabel.value
            });
            marker.bindPopup(`<a href="${pointData.item.value}">${pointData.itemLabel.value}</a>`);
            markers.addLayer(marker);
        }
        map.addLayer(markers);

        $.get("stats", function (data, status) { $('#statnum').text(data) })
    })
}