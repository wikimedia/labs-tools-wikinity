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
			<p id="goback">Můžete se vrátit <a href="index.php">zpět k nástroji.</a></p>
		</div>
		<script type="text/javascript">
			swal ( "Problém nahlášen", "Co nejrychleji se mu budeme věnovat.", "success" );
		</script>
	</body>
</html>
