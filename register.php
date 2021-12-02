<?php
// 发送邮件
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require './src/Exception.php';
require './src/PHPMailer.php';
require './src/SMTP.php';

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
    $mail->addAddress('', 'Jue');  // 收件人
    //$mail->addAddress('');  // 可添加多个收件人
    $mail->addReplyTo('', 'info'); //回复的时候回复给哪个邮箱 建议和发件人一致
    //$mail->addCC('cc@example.com');                    //抄送
    //$mail->addBCC('bcc@example.com');                    //密送

    //发送附件
    // $mail->addAttachment('../xy.zip');         // 添加附件
    // $mail->addAttachment('../thumb-1.jpg', 'new.jpg');    // 发送附件并且重命名

    //Content
    $mail->isHTML(true);                                  // 是否以HTML文档格式发送  发送后客户端可直接显示对应HTML内容
    $token = '12345';
    $id = '1';
    $mail->Subject = 'Title' . time();
    $mail->Body    = "Sehr geehrte Damen und Herren,<br>
     <br>
    Sie haben schon ihre Document hochgeladen.<br>
     Klicken Sie auf den untenstehenden Link, um Ihre E-Mail zu bestätigen.<br>
     <br>
    <a href='http://localhost:3000/active.php?id=".$id."&verify_code=".$token."'>klicken</a></br>
    <br>
    Wenn der obige Link nicht angeklickt werden kann, kopieren Sie ihn bitte in die Adressleiste Ihres Browsers, um darauf zuzugreifen. <br>
   Falls diese Aktivierungsanfrage nicht von Ihnen gesendet wurde, ignorieren Sie diese E-Mail bitte. <br>
   <br>
    Mit freundlichen Grüßen.<br>
    GoAsia Supermarkt<br>
    <br>
    亲爱的顾客您好：<br>
  感谢您在我站上传了抽奖证明。<br>
  请点击链接激活您的本次上传。<br>
   <br>
    <a href='http://localhost:3000/active.php?id=".$id."&verify_code=".$token."'>点击此处</a></br>
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
