<?php include 'header.php'; ?>
<body>
	<?php include 'navbar.php'; ?>
	<div class="container">
		<form action="issue.py" method="post">
			<div class="row">
				<div class="col">
					<label for="email"><?php echo $I18N->msg("your-email"); ?></label><br>
					<input type="text" name="email" id="email" value="">
				</div>
				<div class="col">
					<label for="title"><?php echo $I18N->msg("problem-summary"); ?></label><br>
					<input type="text" name="title" id="title" value="">
				</div>
				<div class="col">
					<label for="body"><?php echo $I18N->msg("problem-body"); ?></label><br>
					<textarea name="body" rows="8" cols="80"></textarea>
				</div>
			</div>
			<div class="col-3">
				  <button type="submit" class="btn btn-primary" id="submit"><?php echo $I18N->msg("submit"); ?></button>
			</div>
		</form>
		<?php include 'footer.php'; ?>
	</div>
</body>
</html>
