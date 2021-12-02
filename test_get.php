<span style="font-size:18px;">
<?php
    // get
    $id = $_GET['id'];
    $verify_code = $_GET['verify_code'];
    // 创建连接
    $conn = mysqli_connect("localhost","root","admin",'db');
    // check
    $query = sprintf("SELECT * FROM tmp WHERE `id`=%s and `verify_code`=%s;",$id,$verify_code);
    $result = mysqli_query($conn,$query);
    if ($result){
        // update
        $query = sprintf("UPDATE tmp SET verify_code='-' WHERE id=%s;",$id);
        mysqli_query($conn,$query);
        echo 'verify erfolgt';
    }
    else {
        echo 'Falsch Code!';
    }
    $conn->close();
?></span>