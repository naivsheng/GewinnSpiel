<span style="font-size:18px;">
<?php
    // get
    $id = $_GET['id'];
    $verify_code = $_GET['verify_code'];
    // DB
    $servername = "localhost";
    $username = "root";
    $password = "admin";
    // 创建连接
    //$conn = new mysqli($servername, $username, $password);
    $conn = mysqli_connect($servername,$username,$password,'db');
    /* 检验连接
        if (mysqli_connect_errno()) 
        { 
            echo "连接 MySQL 失败: " . mysqli_connect_error(); 
        } else
            {
                echo "连接成功";
            }
        */
    // check
    /*  检查数据
        $result = mysqli_query($conn,"SELECT * FROM tmp;");
        if ($result){
            while($row = mysqli_fetch_array($result))
            {
                echo $row['id'] . " " . $row['email'];
                echo "<br>";
            }
        }else{
            echo "no findout";
            echo "<br>";
        }
    */
    $query = sprintf("SELECT * FROM tmp WHERE `id`=%s and `verify_code`=%s;",$id,$verify_code);
    $result = mysqli_query($conn,$query);
    echo mysqli_fetch_array($result);
    echo "<br>";
    // if ($row = mysqli_fetch_array($result) !== ''){
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

<?php
    //echo phpinfo();
?>
