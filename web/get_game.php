<?php

$servername = "db";
$username = "changethis";
$password = "changethistoo";
$database = "fpgames";

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

try {
  $pdo = new PDO("mysql:host=$servername;dbname=$database", $username, $password);
} catch(PDOException $e) {
  die("Connection failed +".$e);
}

#Add more tags if neded
$extreme = isset($_GET['extreme']) ? ($_GET['extreme'] == 'allowed' ? '' : "AND isExtreme = '1'" ) : "AND isExtreme = '0' AND NOT (suggestedTag IN ('Adult', 'Sexual Content'))";

$query = "SELECT * FROM game
WHERE vote_yes < 2 AND vote_no < 2
%s
ORDER BY RAND() LIMIT 1";

$stmt = $pdo->query(sprintf($query, $extreme));
$row = $stmt->fetch();

echo json_encode($row);

?>