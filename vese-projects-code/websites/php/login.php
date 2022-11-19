<?php

include('DB.php');


function create_query($sql_query, $args){
    return vsprintf($sql_query, $args);
}

$dbhost = 'db-docker';
$dbuser = 'internal_dev';
$dbpass = 'internaldevpassword';
$dbname = 'users';

$db = new db($dbhost, $dbuser, $dbpass, $dbname);

if (isset($_POST['username']) && isset($_POST['pwd'])){
    $username = $_POST['username'];
    $sanitized_username = addslashes($username);

    $pwd = $_POST['pwd'];
    $sanitized_pwd = addslashes($pwd);
    
    # Password are MD5 hashed qL1cmCvxPS626V9MBVCL3x18LKZc4oc8
    $pwdmd5 = md5($sanitized_pwd);
   
    # cc5713089b0a9335111f55bd25e39130b843dabadf63e1170c668d0a4a6d5e37
    $sqlQuery = "SELECT * FROM users.users WHERE password=('%s') AND username=('%s')";
    $query = create_query($sqlQuery, array($pwdmd5, $username));
    // Execute the SQL Query    
    $res = $db->query($query);

    // Return rows
    $row = $db->fetchArray($res);
    if ($row) {
        $_SESSION['username'] = $row['username'];
        header("Location: http://internal.vese.com/logged.html");
    }
    else {
        header("Location: http://internal.vese.com/failed.html");
    }
    die();

}

$db->close();

?>