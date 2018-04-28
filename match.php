<link rel="stylesheet" href="../assets/css/main.css" type="text/css">
<?php
// outputs the username that owns the running php/httpd process
// (on a system with the "whoami" executable in the path)
echo '<pre>'; print_r($output); echo '</pre>';
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
							<h2>Match Summary (Step 1)</h2>
						</header>';
						echo '<h2>';
						echo $_POST['team1'];
						// echo '<br>';
						echo '  vs.  ';
						echo $_POST['team2'];
						echo '</h2>';
						$json = exec('python match_info.py "' . $_POST['team1'] . '" "' . $_POST['team2'] . '" ' . $_POST['season'], $output1);
						echo '<p>';
						$array = json_decode($json, true);				
						echo '</p>';
						// echo '<pre>'; print_r($array); echo '</pre>';
						echo 'Match Info Table';
						echo '<table style="width:100%">
							  <tr>
							    <th>Home Team</th>
							    <th>Away Team</th> 
							    <th>League</th>
							    <th>Season</th>
							    <th>Home Goals</th>
							    <th>Away Goals</th>
							    <th>Win Odds</th>
							  </tr>
							  <tr>
							    <td>'.$array['ht'].'</td>
							    <td>'.$array['at'].'</td> 
							    <td>'.$array['league'].'</td>
							    <td>'.$array['season'].'</td>
							    <td>'.$array['fthg'].'</td> 
							    <td>'.$array['ftag'].'</td>
							    <td>'.$array['odd_h'].' : '.$array['odd_a'].'</td>
							  </tr>
							</table>';
						$json_events = exec('python event_info.py ' . $array['id_odsp'], $output11);
						echo '<p>';
						$array1 = json_decode($json_events, true);
						// echo '<pre>'; print_r($array1); echo '</pre>';
						echo 'Event Timeline Table';
						echo '<table style="width:100%">
							  <tr>
							    <th>Time</th>
							    <th>Event Type</th> 
							    <th>Event Team</th>
							    <th>Player</th>
							    <th>Is Goal?</th>
							    <th>Location</th>
							    <th>Bodypart Used</th>
							  </tr>';
						foreach($array1 as $event){
							echo '<tr>
							    <td>'.$event['time'].'</td>
							    <td>'.$event['event_type'].'</td> 
							    <td>'.$event['event_team'].'</td>
							    <td>'.$event['player'].'</td>
							    <td>'.$event['is_goal'].'</td> 
							    <td>'.$event['location'].'</td>
							    <td>'.$event['bodypart'].'</td>
							  </tr>';
						}
						echo '</table>';
			echo '</div>
			</section>
		</div>
		<br><br>
		<div id="main">
		<!-- Introduction -->
			<section id="intro" class="main">
				<div class="spotlight">
					<div class="content">
						<header class="major">
							<h2>Match Summary (Step 2)</h2>
						</header>';
						echo '<h2>';
						echo $_POST['team1'];
						// echo '<br>';
						echo '  vs.  ';
						echo $_POST['team2'];
						echo '</h2>';
						exec('python summary.py "' . $_POST['team1'] . '" "' . $_POST['team2'] . '" ' . $_POST['season'], $output2);
						echo '<p>';
						// echo '<pre>'; print_r($output); echo '</pre>';
						foreach($output2 as $line){
							echo '<p>'.$line.' </p>';
						}
						echo '</p>';
			echo '</div>
			</section>
		</div>
		<br><br>
		<div id="main">
		<!-- Introduction -->
			<section id="intro" class="main">
				<div class="spotlight">
					<div class="content">
						<header class="major">
							<h2>Match Summary (Step 3)</h2>
						</header>';
						echo '<h2>';
						echo $_POST['team1'];
						// echo '<br>';
						echo '  vs.  ';
						echo $_POST['team2'];
						echo '</h2>';
						exec('python final_summary.py "' . $_POST['team1'] . '" "' . $_POST['team2'] . '" ' . $_POST['season'], $output3);
						echo '<p>';
						// echo '<pre>'; print_r($output); echo '</pre>';
						foreach($output3 as $line){
							echo $line.' ';
						}
						echo '</p>';
			echo '</div>
			</section>
		</div>
		<br><br>
	</div>';
echo '<script src="assets/js/jquery.min.js"></script>
	<script src="assets/js/jquery.scrollex.min.js"></script>
	<script src="assets/js/jquery.scrolly.min.js"></script>
	<script src="assets/js/skel.min.js"></script>
	<script src="assets/js/util.js"></script>
	<!--[if lte IE 8]><script src="assets/js/ie/respond.min.js"></script><![endif]-->
	<script src="assets/js/main.js"></script>';
?>