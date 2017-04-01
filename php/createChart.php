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
	
	$sql = "SELECT imageName, count(*) as NUM FROM container GROUP BY imageName";
	$result = $conn->query($sql);
	$jsonArray = array();
	
	if($result->num_rows>0)
	{
		$max_row = $result->num_rows;
	
		for($i=0; $i<$max_row; $i++)
		{
			$rows = $result -> fetch_assoc();
			$jsonArrayItem = array();
			$jsonArrayItem["label"] = $rows["imageName"];
			$jsonArrayItem["value"] = $rows["NUM"];
			array_push($jsonArray, $jsonArrayItem);
		}
	}
	else
	{
		exit("Error in getting container count.");
	}
	
	$conn ->close();
	
	header('Content-type: application/json');
	
	echo json_encode($jsonArray);
?>