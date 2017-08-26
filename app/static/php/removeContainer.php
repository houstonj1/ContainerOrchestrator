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
	$temp = $_POST["data"];
	$array = explode(",","$temp");
	$first = $array[0];

	for($i=2;$i<count($array);$i+=2)
	{
		echo "$array[$i]";
		if(strcmp($first,$array[$i]) != 0)
			$status = "failed";
		else
		{
			if(strcmp($first,$username) == 0)
				$status = "success";
			else
				$status = "failed";
		}
	}
	
	if(strcmp($status,"success") == 0)
	{
		for($i=1;$i<=count($array);$i+=2)
		{
			$sql= "DELETE FROM container WHERE containerID = '$array[$i]'";
			$conn->query($sql);
		}
	}
	
	$_POST["data"] = $status;
	
	
?>
