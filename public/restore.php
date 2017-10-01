<?php include 'header.php'; ?>
	<body>
		<?php include 'navbar.php'; ?>
		<div class="container">
			<div class="col" id="map" style="padding-top:2.5%; width:70%">
			</div>
			<script type="text/javascript">
				function getParameterByName(name, url) {
					if (!url) url = window.location.href;
					name = name.replace(/[\[\]]/g, "\\$&");
					var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
						results = regex.exec(url);
					if (!results) return null;
					if (!results[2]) return '';
					return decodeURIComponent(results[2].replace(/\+/g, " "));
				}
				var id = getParameterByName('id');
				if (id == null) {
					swal ( "Oops" ,  "Something went wrong!" ,  "error" );
				} else {
					var url = 'https://tools.wmflabs.org/wikinity/getshort.py?id=' + id;
					$.get(url, function (data, status) {
						$('#map').load(data, "#map");
					})
				}
			</script>
		</div>
	</body>
</html>
