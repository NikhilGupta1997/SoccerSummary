<link rel="stylesheet" href="../assets/css/main.css" type="text/css">
<?php
// outputs the username that owns the running php/httpd process
// (on a system with the "whoami" executable in the path)
echo "<center><h1>Match Summary Results</h1></center>";
echo '<div class = input><center><button onclick="history.go(-1);">Back </button></div><br>';
echo $_POST['team1'];
echo '<br>';
echo $_POST['team2'];
exec('python summary.py "' . $_POST['team1'] . '" "' . $_POST['team2'] . '" ' . $_POST['season'], $output);
echo '<pre>'; print_r($output); echo '</pre>';
?>