<span style="font-size:18px;">
<?php
    // get
    $id = $_GET['id'];
    $verify_code = $_GET['verify_code'];
    // 创建连接
    $conn = mysqli_connect("localhost","root","admin",'db');
    // check
    $query = "SELECT * FROM test WHERE `id`=".$id;
    $result = mysqli_query($conn,$query);
    if ($result){
        // update
        while($row = mysqli_fetch_array($result))
        {
            if($row['verify_code'] == $verify_code){
                $query = sprintf("UPDATE test SET verify_code='-' WHERE id=%s;",$id);
                mysqli_query($conn,$query);
                echo 'verify erfolgt';
            }
            }
        }
    else {
        echo 'Falsch Code!';
    }
    $conn->close();
?></span>
