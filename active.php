<?php
include_once("connect.php");//连接数据库
$verify = stripslashes(trim($_GET['verify']));
$nowtime = time();
$query = mysql_query("select id,token_exptime from t_user where status='0' and `token`='$verify'");
$row = mysql_fetch_array($query);
if($row){
    # mysql_query("update t_user set status=1 where id=".$row['id']);
    mysql_query("update t_user set token='' where id=".$row['id']);
    if(mysql_affected_rows($link)!=1) die(0);
    $msg = '激活成功！';
}else{
  $msg = 'error.';
}
echo $msg;
?>