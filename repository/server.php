<?php

/*
Cati repository server side script
@author parsa mpsh <parsampsh@gmail.com>
*/

/**
 * crawls an directory and extracts data of packages from that
 */
function get_data($path){
    // TODO : return real data
    return '[]';
}

if(isset($_GET['cati-repo-test'])){
    // this is a just test request
    die('OK');
}

$requested_uri = explode('?', $_SERVER['REQUEST_URI'])[0];

$full_path = __DIR__ . '/' . $requested_uri;

if(is_dir($full_path) || is_file($full_path)){
    // requested path exists
    if(is_file($full_path)){
        // return file content by webserver
        return FALSE;
    }else{
        if(isset($_GET['get_data'])){
            die(get_data($full_path));
        }else{
            $items = glob($full_path . '/*');
            foreach($items as $item){
                $tmp = explode('/', $item);
                $tmp = $tmp[count($tmp)-1];
                if($tmp !== 'server.php'){
                    echo '<a href="' . str_replace('//', '/', ($requested_uri . '/' . $tmp)) . '">' . $tmp . '</a><br />';
                }
            }
        }
    }
}else{
    // 404 not found
    http_response_code(404);
    die('<h2>404 Not Found</h2>');
}
