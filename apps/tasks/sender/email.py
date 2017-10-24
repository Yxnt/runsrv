from apps import  celery
from apps.models import Monitor


@celery.task
def send_email():
    for i in Monitor.query.filter_by(operator=True).all():
        msg = "时间：{time}\n主机：{host}\n报警信息：{message}".format(
            time=i.c_time,
            host=i.hostname,
            message=i.message
        )
        email(msg)



def email(message):
    import smtplib
    from email.mime.text import MIMEText
    msg = MIMEText(message)

    msg['Subject'] = '服务器发现异常'
    msg['From'] = ''
    msg['To'] = ''

    with smtplib.SMTP('smtp.exmail.qq.com') as smtp:
        smtp.login('','')
        smtp.send_message(msg)