<?php
session_start();
unset($_SESSION['OPENID_JWT']);

if($_SERVER["REQUEST_METHOD"] == "GET" && isset($_GET['code'])){
    require_once __DIR__ . '/openid.php';
    OPENID::authentication_authorization($_GET['code']);
    header('Location: index.php');
}
else {
    header('Location: forbidden.php');
}
?>