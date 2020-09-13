var mapsPlaceholder = []
L.Map.addInitHook(function () {
    mapsPlaceholder.push(this);
});
function GetValues() {
	$('#mapcontainer').html("");
	$('#error').addClass("hidden");
	$('#processing').removeClass("hidden");
	if($('#payload').text() == '') {
		if(mapsPlaceholder.length == 1) {mapsPlaceholder[0].remove()}
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

			if (payload["article"] == "" || payload["project"] == "") {
				payload["article"] = "Praha";
				payload["project"] = "cswiki";
			}
		} else if (type == "item") {
			payload["item"] = $('input[name="cislo"]').val();

			if(payload["item"] == "") {
				payload["item"] = "Q1085";
			}
		} else if (type == "coordinate") {
			if($("#degdec").hasClass("in")) {
				var lat = $('input[name="lat-degdec"]').val();
				var lon = $('input[name="lon-degdec"]').val();

				if(lat === "" || lon === "") {
					lat = 50.088611;
					lon = 14.421389;
				}

				payload["lat"] = lat;
				payload["lon"] = lon;
			} else {
				var lat = {};
				var lon = {};

				components = ["deg", "min", "sec"];

				for(component of components) {
					lat[component] = $(`input[name="lat-${component}"]`).val();
					lon[component] = $(`input[name="lon-${component}"]`).val();
				}

				var latInDegrees = dmsToDegrees(lat);
				var lonInDegrees = dmsToDegrees(lon);

				if(isNaN(latInDegrees) || isNaN(lonInDegrees)) {
					latInDegrees = 50.088611;
					lonInDegrees = 14.421389;
				}

				payload["lat"] = latInDegrees;
				payload["lon"] = lonInDegrees;
			}
		}
	} else {
		payload = JSON.parse($('#payload').text());
	}
	$.post($('#root').text() + 's/store', { payload: JSON.stringify(payload) }, function(data) {
		var url = window.location.origin + $('#root').text() + 's/' + data;
		$('#shortUrl').html('<a href="' + url + '">' + url + '</a>');
	});

	$.get($('#root').text() + 'map', payload, function(data) {
        $('#mapcontainer').html('<div class="bigmap" id="map"></div>');
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

        $.get($('#root').text() + "stats", function (data, status) { $('#statnum').text(data) })
    }).fail(function(data) {
        $('#processing').addClass("hidden");
        $('#error').removeClass("hidden");
        $('#error').text(data.responseJSON.errortext);
    });
}

function dmsToDegrees(coord) {
    var converted =
        parseFloat(coord.deg) +
        parseFloat(coord.min / 60) +
        parseFloat(coord.sec / 3600);

    converted = converted.toFixed(6);

    return converted;
}
