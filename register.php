<?php
$email = trim($_POST['email']); //邮箱
$data = trim($_POST['data']);
$regtime = time();
$token = md5($username.$regtime); //创建用于激活识别码
$con=mysql_connect("127.0.0.1", "root", "admin","db")
OR die('Could not connect to database.');
echo "Connected!";
$sql = "insert into `uploads` (`email`,`data`,`token`) values ('$email','$data','$token')";
mysql_query($sql,$con);

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require './src/Exception.php';
require './src/PHPMailer.php';
require './src/SMTP.php';

if (mysql_insert_id()) {//写入成功，发邮件
  $mail = new PHPMailer(true);                              // Passing `true` enables exceptions
  try {
      //服务器配置
      $mail->CharSet ="UTF-8";                     //设定邮件编码
      $mail->SMTPDebug = 0;                        // 调试模式输出
      $mail->isSMTP();                             // 使用SMTP
      $mail->Host = '';                // SMTP服务器
      $mail->SMTPAuth = true;                      // 允许 SMTP 认证
      $mail->Username = '';                // SMTP 用户名  即邮箱的用户名
      $mail->Password = '';             // SMTP 密码  部分邮箱是授权码(例如163邮箱)
      $mail->SMTPSecure = 'ssl';                    // 允许 TLS 或者ssl协议
      $mail->Port = 465;                            // 服务器端口 25 或者465 具体要看邮箱服务器支持
  
      $mail->setFrom("", 'Mailer');  //发件人
      $mail->addAddress($email, '');  // 收件人
      $mail->addReplyTo('', 're'); //回复的时候回复给哪个邮箱 建议和发件人一致
      
      //Content
      $mail->isHTML(true);                                  // 是否以HTML文档格式发送  发送后客户端可直接显示对应HTML内容
      $mail->Subject = 'Title' . time();
      $mail->Body    = "Sehr geehrte Damen und Herren,<br>
      <br>
      Sie haben schon ihre Document hochgeladen.<br>
       Klicken Sie auf den untenstehenden Link, um Ihre E-Mail zu bestätigen.<br>
       <br>
      http://localhost:3000/active.php?verify=" . $token . " <br>
      <br>
      Wenn der obige Link nicht angeklickt werden kann, kopieren Sie ihn bitte in die Adressleiste Ihres Browsers, um darauf zuzugreifen. <br>
     Falls diese Aktivierungsanfrage nicht von Ihnen gesendet wurde, ignorieren Sie diese E-Mail bitte. <br><br>
      Mit freundlichen Grüßen.<br>
      GoAsia Supermarkt<br>
      <br>
      亲爱的顾客您好：<br>
    感谢您在我站上传了抽奖证明。<br>
    请点击链接激活您的本次上传。<br>
    <br>
    http://localhost:3000/active.php?verify=" . $token . " <br>
    <br>
    如果以上链接无法点击，请将它复制到你的浏览器地址栏中进入访问。<br>
    如果此次激活请求非你本人所发，请忽略本邮件。<br>
     <br>
    祝您生活愉快<br>
    德国东方超市";
      $mail->AltBody = '如果邮件客户端不支持HTML则显示此内容';
  
      $mail->send();
      echo  'Sie haben Ihre Daten schon erfolgreich hochgeladen!
      Bitte loggen Sie sich in Ihr Postfach ein, um Ihre Upload-Ergebnisse rechtzeitig zu aktivieren.<br>
      恭喜您，上传成功！
  请登录到您的邮箱及时激活您的上传结果！';
  } catch (Exception $e) {
      echo '邮件发送失败: ', $mail->ErrorInfo;
  }
  }
?>
