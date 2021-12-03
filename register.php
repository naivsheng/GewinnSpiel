<?php
// 发送邮件时生成token
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require './src/Exception.php';
require './src/PHPMailer.php';
require './src/SMTP.php';

$conn = mysqli_connect("localhost","root","admin",'db');
$query = "SELECT * FROM test WHERE verify_code is Null;";
$result = mysqli_query($conn,$query);
while($row = mysqli_fetch_array($result))
{
    $str=rand();
    $token = md5($str);
    if(sendMail($row['id'],$row['email'],$token)){
        $query = "UPDATE test SET verify_code = ".$token." WHERE `id` = ".$row['id'].";";
        mysqli_query($conn,$query);
    }
}
function sendMail($id,$email,$token)
{
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

    $mail->setFrom("", 'No Reply');  //发件人
    $mail->addAddress($email, 'GA Kunde');  // 收件人
    $mail->addReplyTo('', 'No Reply'); //回复的时候回复给哪个邮箱 建议和发件人一致
    
    //Content
    $mail->isHTML(true);                                  // 是否以HTML文档格式发送  发送后客户端可直接显示对应HTML内容
    $token = $token;
    $id = $id;
    $mail->Subject = 'confirm your email-adress' . time();
    $mail->Body    = "Sehr geehrte Damen und Herren,<br>
     <br>
    Sie haben schon ihre Document hochgeladen.<br>
     Klicken Sie auf den untenstehenden Link, um Ihre E-Mail zu bestätigen.<br>
     <br>
    <a href='http://localhost:3000/active.php?id=".$id."&verify_code=".$token."'>klicken</a></br>
    <br>
    Wenn der obige Link nicht angeklickt werden kann, kopieren Sie diesen Link bitte in die Adressleiste Ihres Browsers, um darauf zuzugreifen. <br>
    http://localhost:3000/active.php?id=".$id."&verify_code=".$token." <br>
   Falls diese Aktivierungsanfrage nicht von Ihnen gesendet wurde, ignorieren Sie diese E-Mail bitte. <br>
   <br>
    Mit freundlichen Grüßen.<br>
    GoAsia Supermarkt<br>
    <br>
    亲爱的顾客您好：<br>
  感谢您在我站上传了抽奖证明。<br>
  请点击链接激活您的本次上传。<br>
  <br>
  <a href='http://localhost:3000/active.php?id=".$id."&verify_code=".$token."'>klicken</a></br>
    <br>
  如果以上链接无法点击，请将以下链接复制到你的浏览器地址栏中进入访问。<br>
  http://localhost:3000/active.php?id=".$id."&verify_code=".$token." <br>
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
return True;
} catch (Exception $e) {
    echo '邮件发送失败: ', $mail->ErrorInfo;
    echo '<br>Fehler bei Emailsendung!<br>';
    return False;
}
}