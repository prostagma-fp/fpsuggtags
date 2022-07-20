<?php

if(isset($_GET['id']) && isset($_GET['suggestedTag']) && isset($_GET['vote']) && ($_GET['vote'] == 'yes' || $_GET['vote'] == 'no')){

    $servername = "db";
	$username = "changethis";
	$password = "changethistoo";
    $database = "fpgames";
	
	try {
	  $pdo = new PDO("mysql:host=$servername;dbname=$database", $username, $password);
	} catch(PDOException $e) {
		die("Connection failed +".$e);
	}
	
    $query = "UPDATE game
    SET vote_%s = (vote_%s + 1)
    WHERE id = (?)
    AND suggestedTag = (?)";
	$stm = $pdo->prepare(sprintf($query, $_GET['vote'], $_GET['vote']));
	$res = $stm->execute(array($_GET['id'], $_GET['suggestedTag']));
    
    #echo $stm;
    
    if($res){
        echo 'committed';
    }
    else{
        echo 'no changes done';
    }
}

?>