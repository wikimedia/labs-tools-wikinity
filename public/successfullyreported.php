<?php
// Force HTTPS for our users
if (getallheaders()['X-Forwarded-Proto'] == "http") {
	header("Location: https://".$_SERVER['HTTP_HOST'].$_SERVER['PHP_SELF']);
	die();
}
require_once __DIR__ . '/../vendor/autoload.php';
$I18N = new Intuition( 'wikinity' );
$I18N->registerDomain( 'wikinity', __DIR__ . '/../messages' );
?>
<!DOCTYPE HTML>
<html lang="cs">
	<head>
	  <meta charset="utf-8">
	  <meta http-equiv="X-UA-Compatible" content="IE=edge">
	  <meta name="viewport" content="width=device-width, initial-scale=1">
	  <title>Wikinity</title>
	  <!-- font awesome -->
	  <link rel="stylesheet" href="https://tools-static.wmflabs.org/cdnjs/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
	  <!-- Latest compiled and minified CSS -->
	  <link rel="stylesheet" href="https://tools-static.wmflabs.org/cdnjs/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
	    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
	  <script src="https://tools-static.wmflabs.org/cdnjs/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
	  <!-- Latest compiled and minified JavaScript -->
	  <script src="https://tools-static.wmflabs.org/cdnjs/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
	  <script src="https://tools-static.wmflabs.org/cdnjs/ajax/libs/sweetalert/1.1.3/sweetalert.min.js" charset="utf-8"></script>
	  <link rel="stylesheet" href="https://tools-static.wmflabs.org/cdnjs/ajax/libs/sweetalert/1.1.3/sweetalert.min.css">
	</head>
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
	</body>
</html>
