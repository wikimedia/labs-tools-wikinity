<?php include 'header.php'; ?>
	<body>
		<!-- navbar -->
		<nav class="navbar navbar-inverse bg-faded" style="background-color:#337ab7;border-color: 2e6da4; border-radius: 0;">
			<a class="navbar-brand" href="#" style="color: #fff">
			  Wikinity
			</a>

			<a class="navbar-brand" href="https://github.com/urbanecm/wikinity/" style="color: #fff;float: right">
				<i class="fa fa-github fa-lg" aria-hidden="true"></i> GitHub - zdrojový kód
			</a>
		  <a style="float: right; color: white;" class="navbar-brand no-hover" href="reportproblem.php">Nahlásit problém</a>
		</nav>
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
