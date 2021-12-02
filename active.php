<span style="font-size:18px;">
<?php
    // get
    $id = $_GET['id'];
    $verify_code = $_GET['verify_code'];
    // 创建连接
    $conn = mysqli_connect("localhost","root","admin",'db');
    // check
    //$query = sprintf("SELECT * FROM test WHERE `id`=%s and `verify_code`=%s;",$id,$verify_code);
    $query = "SELECT * FROM test WHERE `id`=".$id;
    $result = mysqli_query($conn,$query);
    if ($result){
        // update
        /*
        $query = sprintf("UPDATE test SET verify_code='-' WHERE id=%s;",$id);
        mysqli_query($conn,$query);
        echo 'verify erfolgt';
        */
        ///*
        while($row = mysqli_fetch_array($result))
        {
            //echo $row['id'] . " " . $row['verify_code'];
            //echo "<br>";
            if($row['verify_code'] == $verify_code){
                $query = sprintf("UPDATE test SET verify_code='-' WHERE id=%s;",$id);
                mysqli_query($conn,$query);
                echo 'verify erfolgt';
            }
            }
        //*/
        }
    else {
        echo 'Falsch Code!';
    }
    $conn->close();
?></span>
