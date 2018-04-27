<link rel="stylesheet" href="../assets/css/main.css" type="text/css">
<?php
// outputs the username that owns the running php/httpd process
// (on a system with the "whoami" executable in the path)
// echo "<center><h1>Match Season Results</h1></center>";
// echo '<div class = input><center><button onclick="history.go(-1);">Back </button></div><br>';
// echo $_POST['team1'];
// echo '<br>';
// echo $_POST['team2'];
// echo '<div class="content"> 
// 		<form name="insert" action="match.php" method="POST" >
// 		<select name="season", placeholder="season>';
// exec('python get_matches.py "' . $_POST['team1'] . '" "' . $_POST['team2'] . '"', $output);
// // echo '<pre>'; print_r($output); echo '</pre>';
// foreach($output as $season){
// 	echo '<option value="'.$season.'">'.$season.'</option>';
// }
// echo '</select>';
// echo '<br>';
// echo '<input type="hidden" name="team1" value="' . $_POST['team1'] . '">';
// echo '<input type="hidden" name="team2" value="' . $_POST['team2'] . '">';
// echo '<ul class="actions">
// 				<li><input type="submit" value="Send" class="special" /></li>
// 				<li><input type="reset" value="Reset" /></li>
// 			</ul>
// 			</form>
// 		</div>';

echo '<div id="wrapper">
		<!-- Header -->
			<header id="header" class="alt">
				<h1>Soccer Summarisation</h1>
			</header>
		<div class = input><center><button onclick="history.go(-1);">Back </button></div><br>
		<div id="main">
		<!-- Introduction -->
			<section id="intro" class="main">
				<div class="spotlight">
					<div class="content">
						<header class="major">
							<h2>Select Season</h2>
						</header>';
						echo '<h2>';
						echo $_POST['team1'];
						// echo '<br>';
						echo '  vs.  ';
						echo $_POST['team2'];
						echo '</h2>';

						echo '<div class="content"> 
								<form name="insert" action="match.php" method="POST" >
								<select name="season", placeholder="season>';
						exec('python get_matches.py "' . $_POST['team1'] . '" "' . $_POST['team2'] . '"', $output);
						// echo '<pre>'; print_r($output); echo '</pre>';
						foreach($output as $season){
							echo '<option value="'.$season.'">'.$season.'</option>';
						}
						echo '</select>';
						echo '<br>';
						echo '<input type="hidden" name="team1" value="' . $_POST['team1'] . '">';
						echo '<input type="hidden" name="team2" value="' . $_POST['team2'] . '">';
						echo '<ul class="actions">
						<li><input type="submit" value="Send" class="special" /></li>
						<li><input type="reset" value="Reset" /></li>
					</ul>
					</form>
					</div>
				</div>
			</section>
		</div>
		<br><br>
	</div>
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrollex.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<!--[if lte IE 8]><script src="assets/js/ie/respond.min.js"></script><![endif]-->
			<script src="assets/js/main.js"></script>'

?>