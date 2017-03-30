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
	
	$username = $_SESSION["username"];
	$id = $_SESSION["userid"];
	$containerid = $_POST["containerID"];
	
	$sql="SELECT createdBy FROM container WHERE containerID = '$containerid'";
	$result = $conn->query($sql);
	
	if($result-> num_rows > 0)
	{
		$row = $result -> fetch_assoc();
		$temp = $row["createdBy"];
		
		if($temp == $id)
			//remove container
		else
			//alert

		header("Location: ../web/Container.html"); 
	}
	else
	{
		echo "<script>alert(\"Username or password is incorrect! Try Again!\");</script>";
		header("Location: ../web/Login.html");
	}
?>
