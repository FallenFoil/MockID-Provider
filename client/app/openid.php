<?php
class OPENID {
    public static function authorize(){
        $ini_array = parse_ini_file("/var/www/html/config.ini", true);

        $url = $ini_array["openid"]["OPENID_AUTHORITY"] . '/oauth2/v2.0/authorize?';
        $url = $url . 'client_id=' . $ini_array["openid"]["OPENID_CLIENTID"];
        $url = $url . '&response_type=code';
        $url = $url . '&redirect_uri=' . urlencode($ini_array["openid"]['OPENID_REDIRECT']);
        $url = $url . '&response_mode=query';
        $url = $url . '&scope=' . urlencode($ini_array["openid"]['OPENID_SCOPE']);

        header('Location: ' . $url);
    }

    private static function token($code){
        $ini_array = parse_ini_file("/var/www/html/config.ini", true);
        
        $url = $ini_array["openid"]["OPENID_AUTHORITY"] . '/oauth2/v2.0/token';
        $post = [
            'client_id' => $ini_array["openid"]['OPENID_CLIENTID'],
            'scope' => $ini_array["openid"]['OPENID_SCOPE'],
            'code' => $code,
            'redirect_uri' => $ini_array["openid"]['OPENID_REDIRECT'],
            'grant_type' => 'authorization_code',
            'client_secret' => $ini_array["openid"]['OPENID_SECRET'],
        ];

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        $response_token = curl_exec($ch);

        $fp = fopen("/var/www/html/debug.txt", "w");
        fwrite($fp, $response_token);

        curl_close($ch);
        
        $token = json_decode($response_token);
        
        if($token === null){
            header("Location: failure.php");
            exit();
        }
        
        if(property_exists($token, "error") && property_exists($token, "error_description")){
            header("Location: failure.php?error=" . $token->error);
            exit();
        }

        $accessToken = $token->access_token;
        return $accessToken;
    }

    public static function authentication_authorization($code){
        $_SESSION['OPENID_JWT'] = self::token($code);
    }
}
?>