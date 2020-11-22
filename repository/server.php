<?php

/*
Cati repository server side script
@author parsa mpsh <parsampsh@gmail.com>
*/

class Crawler{
    protected $scaned_packages = [];

    public function add_once($filepath){
        if($filepath === null){
            return;
        }

        $ext = explode('.', $filepath);
        $ext = $ext[count($ext)-1];
        if($ext !== 'json'){
            return;
        }
        $pkg_ext = explode('.', $filepath);
        $pkg_ext = $pkg_ext[count($pkg_ext)-2];

        $f = fopen($filepath, 'r');
        $content = fread($f, filesize($filepath));
        fclose($f);

        $obj = json_decode($content);

        if($obj === null){
            return;
        }

        $obj->file_path = substr($filepath, 0, strlen($filepath)-5);
        $obj->file_path = str_replace('//', '/', $obj->file_path);
        $obj->file_path = str_replace('//', '/', $obj->file_path);
        $obj->file_path = substr($obj->file_path, strlen(__DIR__));
        $obj->file_path = str_replace('//', '/', $obj->file_path);
        $obj->file_path = str_replace('//', '/', $obj->file_path);
        $obj->file_path = 'http://' . $_SERVER['HTTP_HOST'] . '/' . $obj->file_path;
        $obj->pkg_type = $pkg_ext;

        array_push($this->scaned_packages, $obj);
    }

    public function start(string $path){
        $items = glob($path . '/*');
        for($i = 0; $i < count($items); $i++){
            $item = $items[$i];
            if(is_dir($item)){
                $this->start($item);
            }else{
                $this->add_once($item);
            }
        }
    }

    public function get_packages(){
        return $this->scaned_packages;
    }
}

/**
 * crawls an directory and extracts data of packages from that
 */
function get_data($path){
    $path = str_replace('//', '/', $path);
    $path = str_replace('//', '/', $path);
    $crawler = new Crawler;
    $crawler->start($path);
    $packages = $crawler->get_packages();
    $content = json_encode($packages);
    if($content === null){
        return '[]';
    }
    return $content;
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
            echo '<h1>Cati repository</h1>';
            if($requested_uri !== '' && $requested_uri !== '/'){
                echo '<a href="..">..</a><br />';
            }
            $items = glob($full_path . '/*');
            foreach($items as $item){
                $tmp = explode('/', $item);
                $tmp = $tmp[count($tmp)-1];
                if($tmp !== 'server.php' && $tmp !== 'serve.sh'){
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
