<?php
session_start(); //wajib paling atas
?>

<!DOCTYPE html>
<html>
    <head>
        <title>Login</title>
</head>
<body>
<h2>LOGIN</h2>

<form method="POST">
    Username:
    <input type="text" name="username" required><br><br>

    Password
    <input type="password" name="password" required><br><br>

    <button type="submit">Login</button>
</form>

<?php
if (isset($_POST['username'])) {
    
$username = $_POST['username'];
$password = $_POST['password'];

//data login
if ($username =="admin1" && $password == "123") {

//bikin session 
$_SESSION['login'] = true;
$_SESSION['username'] = $username;

//pindah ke dashboard
header("location: dashboard.php");
exit;

} else {
    echo "login gagal";


}
}

?>
</body>
</html>