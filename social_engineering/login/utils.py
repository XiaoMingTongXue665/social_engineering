
from .models import UserProfile

from SocialRelations_Web.settings import EMAIL_HOST_USER, CONFIRM_DAYS

# 发送邮件工具
def send_mail(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '注册确认邮件'

    text_content = '''感谢注册，本站专注于Python、Django技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/user/confirm/?code={}" target=blank>社工管理系统</a></p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    result = msg.send()
    return result

