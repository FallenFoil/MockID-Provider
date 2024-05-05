<?php
$ini_array = parse_ini_file("/var/www/html/config.ini", true);
echo "Config<br>";
echo "DB:<br>";
foreach ($ini_array["db"] as $key => $value) {
  echo "$key: $value<br>";
}
echo "OpenID:<br>";
foreach ($ini_array["openid"] as $key => $value) {
  echo "$key: $value<br>";
}
?>