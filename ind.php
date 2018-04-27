<?php
echo '<!DOCTYPE HTML>
<!--
	Stellar by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
	<head>
		<title>Stellar by HTML5 UP</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
		<link rel="stylesheet" href="assets/css/main.css" />
		<!--[if lte IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
		<!--[if lte IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
	</head>
	<body>

		<!-- Wrapper -->
			<div id="wrapper">

				<!-- Header -->
					<header id="header" class="alt">
						<span class="logo"><img src="images/logo.svg" alt="" /></span>
						<h1>Soccer Summarisation</h1>
						<p>By Nikhil Gupta and Ayush Bhardwaj</p>
					</header>

				<!-- Main -->
					<div id="main">

						<!-- Introduction -->
							<section id="intro" class="main">
								<div class="spotlight">
									<div class="content">
										<header class="major">
											<h2>Select Teams</h2>
										</header>
										<form name="insert" action="season.php" method="POST" >
										<select name="team1", placeholder="home team>';
									
										exec('python team_names.py', $team_names1);
										foreach($team_names1 as $name){
											$pieces = explode(":", $name);
											$team = $pieces[1];
										echo '<option value="'.$team.'">'.$name.'</option>';
										}
										echo '</select>';
										echo '<select name="team2", placeholder="away team>';
									
										exec('python team_names.py', $team_names2);
										foreach($team_names2 as $name){
											$pieces = explode(":", $name);
											$team = $pieces[1];
										echo '<option value="'.$team.'">'.$name.'</option>';
										}
										echo '</select>';
										echo'<br>
										<ul class="actions">
											<li><input type="submit" value="Send" class="special" /></li>
											<li><input type="reset" value="Reset" /></li>
										</ul>
										</form>
									</div>
									<span class="image"><img src="images/messi.jpg" alt="" /></span>
								</div>
							</section>
					</div>		
			</div>
			<br><br>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrollex.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<!--[if lte IE 8]><script src="assets/js/ie/respond.min.js"></script><![endif]-->
			<script src="assets/js/main.js"></script>

	</body>
</html>'
?>