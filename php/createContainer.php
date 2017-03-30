<?php
	session_start();
	require_once('connect.php');
	
	//create connection
	$conn = mysqli_connect(DBHOST,DBUSER,DBPASS,DBNAME);
	$error = mysqli_connect_errno();
	
	//if connection failed
	if($error != null)
	{
		$output = "<p>Unable to connect to the database</p>";
		exit($output);
	}
	
	//storing information to variables
	$username = $_SESSION["username"]; 
	$id = $_SESSION["userid"];
	$image = $_POST["image_name"];
	
	$sql = "INSERT INTO container(imageName,createdBy) VALUES ('$image','$id')";
	
	//send query to database and get result
		if($conn->query($sql) == TRUE)
			echo "Container created";
		else
			exit("Error on creating container");

	//load next page
	header("Location: ../web/Container.html"); 
?>