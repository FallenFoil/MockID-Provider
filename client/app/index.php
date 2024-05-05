<?php
session_start();

echo "Index";
echo "<br>";

$is_sso = true;
if($is_sso){
  if(isset($_SESSION['OPENID_JWT'])){
    echo "Welcome!<br>";
    echo $_SESSION['OPENID_JWT'];
  } else {
    require_once __DIR__ . '/openid.php';
    OPENID::authorize();
  }
}
else{
  echo "No SSO active";
}

?>