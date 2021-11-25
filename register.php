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
    $smtpusermail = ""; //SMTP服务器的用户邮箱    TODO
    $smtpuser = ""; //SMTP服务器的用户帐号    TODO
    $smtppass = ""; //SMTP服务器的用户密码    TODO
    $smtp = new Smtp($smtpserver, $smtpserverport, true, $smtpuser, $smtppass); //这里面的一个true是表示使用身份验证,否则不使用身份验证.
    $emailtype = "HTML"; //信件类型，文本:text；网页：HTML
    $smtpemailto = $email;
    $smtpemailfrom = $smtpusermail;
    $emailsubject = "bestätigen Ihre Upload-Ergebnisse 上传数据确认"; // TODO
    $emailbody = "Sehr geehrte Damen und Herren,
    Sie haben schon ihre Document hochgeladen.
     Klicken Sie auf den untenstehenden Link, 
    um Ihre E-Mail zu bestätigen.

    http://www.php.cn/demo/active.php?verify=" . $token . " 

    Mit freundlichen Grüßen.
    GoAsia Supermarkt

    亲爱的顾客您好：
  感谢您在我站上传了抽奖证明。
  请点击链接激活您的本次上传。
  
  
    http://www.php.cn/demo/active.php?verify=" . $token . " 
  
    
  如果以上链接无法点击，请将它复制到你的浏览器地址栏中进入访问。
  如果此次激活请求非你本人所发，请忽略本邮件。
  
  祝您生活愉快
  德国东方超市
    ";
    $rs = $smtp->sendmail($smtpemailto, $smtpemailfrom, $emailsubject, $emailbody, $emailtype);
    if ($rs == 1) {
      $msg = 'Sie haben Ihre Daten schon erfolgreich hochgeladen!
      Bitte loggen Sie sich in Ihr Postfach ein, um Ihre Upload-Ergebnisse rechtzeitig zu aktivieren.
      恭喜您，上传成功！
  请登录到您的邮箱及时激活您的上传结果！';
    } else {
      $msg = $rs;
    }
    echo $msg;
  }
?>