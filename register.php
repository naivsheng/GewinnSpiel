<?php
$email = trim($_POST['email']); //邮箱
$regtime = time();
$token = md5($username.$regtime); //创建用于激活识别码
$sql = "insert into `t_user` (`username`,`email`,`token`) values ('$username','$email','$token')";
mysql_query($sql);

if (mysql_insert_id()) {//写入成功，发邮件
    include_once("smtp.class.php");
    $smtpserver = "smtp.163.com"; //SMTP服务器 TODO
    $smtpserverport = 25; //SMTP服务器端口  TODO
    $smtpusermail = "hjl416148489_4@163.com"; //SMTP服务器的用户邮箱    TODO
    $smtpuser = "hjl416148489_4@163.com"; //SMTP服务器的用户帐号    TODO
    $smtppass = "hjl7233163"; //SMTP服务器的用户密码    TODO
    $smtp = new Smtp($smtpserver, $smtpserverport, true, $smtpuser, $smtppass); //这里面的一个true是表示使用身份验证,否则不使用身份验证.
    $emailtype = "HTML"; //信件类型，文本:text；网页：HTML
    $smtpemailto = $email;
    $smtpemailfrom = $smtpusermail;
    $emailsubject = "上传数据确认"; // TODO
    $emailbody = "亲爱的" . $username . "：
  感谢您在我站上传了抽奖证明。
  请点击链接激活您的本次上传。
  
  
    http://www.php.cn/demo/active.php?verify=" . $token . " 
  
    
  如果以上链接无法点击，请将它复制到你的浏览器地址栏中进入访问。
  如果此次激活请求非你本人所发，请忽略本邮件。
  
  
    ";
    $rs = $smtp->sendmail($smtpemailto, $smtpemailfrom, $emailsubject, $emailbody, $emailtype);
    if ($rs == 1) {
      $msg = '恭喜您，上传成功！
  请登录到您的邮箱及时激活您的上传结果！';
    } else {
      $msg = $rs;
    }
    echo $msg;
  }
?>