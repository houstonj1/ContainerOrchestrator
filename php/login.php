<?php
	ob_start();
	if(session_start() != PHP_SESSION_ACTIVE)
		session_start();
	
	require_once('connect.php');
	
	//create connection
	$conn = mysqli_connect(DBHOST,DBUSER,DBPASS,DBNAME);
	$error = mysqli_connect_errno();
	
	if($error != null)
	{
		$output = "<p>Unable to connect to database</p>";
		exit($output);
	}
	
	$user = $_POST['username'];
	$pass = $_POST['password'];
	
	$sql = "SELECT userid FROM account WHERE username = '$user' AND password = '$pass'";
	$result = $conn->query($sql);

	if($result-> num_rows > 0)
	{
		$row = $result -> fetch_assoc();
		$_SESSION["userid"] = $row["userid"];
		$_SESSION["username"] = $user;
		header("Location: ../web/Home.html"); 
	}
	else
	{
		echo "<script>alert(\"Username or password is incorrect! Try Again!\");</script>";
		header("Location: ../web/Login.html");
	}
?>