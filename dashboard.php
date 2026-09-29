<?php
session_start();

//////cek login
if(!isset($_SESSION['login'])) {
    header("location: login.php");
    exit;
}
?>

<!DOCTYPE html>
<html>
<head>
       <title> DASHBOARD </title> 
</head>
<body>
    <h2> DASHBOARD </h2>
    <p> welcome, <b><?php echo $_SESSION['username']; ?> </b>    </p>
    <a href="logout.php"> LOGOUT</a>
</body>
</html>