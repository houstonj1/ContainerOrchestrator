<?php
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
	$username = $_POST["username"]; 
	$pass = $_POST["password"]; 
	$confirmpass = $_POST["confirm-password"];
	
	//Verify if the password and confirm pass are the same
	if($pass != $confirmpass)
	{
		$output = "<p>Passwords must be the same</p>";
		exit($output);
	}
	
	//create sql query
	$sql = "INSERT INTO account(username,password) VALUES ('$username','$pass')";
	
	//send query to database and get result
	if($conn->query($sql) == TRUE)
		echo "Account created";
	else
		exit("Error on creating account");
	
	
	//store user credential as cookies/sessions to use for other pages
	$sql = "SELECT userid FROM account WHERE username = '$username'";
	$result = $conn->query($sql);
	
	if($result-> num_rows > 0)
	{
		$row = $result -> fetch_assoc();
		$_SESSION["userid"] = $row["userid"];
		$_SESSION["username"] = $username;
	}
	
	//load next page
	header("Location: ../html/Login.html"); 
?>