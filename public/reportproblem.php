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
		<form action="issue.py" method="post">
			<div class="row">
				<div class="col">
					<label for="email">Váš e-mail</label><br>
					<input type="text" name="email" id="email" value="">
				</div>
				<div class="col">
					<label for="title">Shrnutí problému</label><br>
					<input type="text" name="title" id="title" value="">
				</div>
				<div class="col">
					<label for="body">Podrobnější popis</label><br>
					<textarea name="body" rows="8" cols="80"></textarea>
				</div>
			</div>
			<div class="col-3">
				  <button type="submit" class="btn btn-primary" id="submit">Submit</button>
			</div>
		</form>
	</div>
</body>
</html>
