import json
import smtplib
import logging
import os
from email.mime.text import MIMEText
#
## Open a plain text file for reading.  For this example, assume that
## the text file contains only ASCII characters.
#fp = open(textfile, 'rb')
## Create a text/plain message
#msg = MIMEText(fp.read())
#fp.close()
#
## me == the sender's email address
## you == the recipient's email address
#msg['Subject'] = 'The contents of %s' % textfile
#msg['From'] = me
#msg['To'] = you
#

def send_email(event, context):
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    log.debug("Received event {}".format(json.dumps(event)))

    body = event['body']
    parameters = json.loads(body)

    smtp_user       = os.getenv('SMTP_USER')
    smtp_password   = os.getenv('SMTP_PASSWORD')
    smtp_host       = os.getenv('SMTP_HOST')
    smtp_port       = os.getenv('SMTP_PORT')
    smtp_domain     = os.getenv('SMTP_DOMAIN')

    from_website    = 'techride.it'
    subject         = 'Contatto da %s' % from_website
    send_from       = 'techride@palazzinifrancesco.com'
    customer_email  = parameters['customer_email'] # visitor email
    send_to         = os.getenv('RECEIVER_EMAIL')
    message         = "{} si e' iscritto alla newsletter di {}".format(reply_to, from_website)

    msg             = MIMEText(message)
    msg['Subject']  = subject
    msg['From']     = send_from
    msg['Reply-To'] = customer_email
    msg['To']       = send_to 

    customer_message = """
Grazie per aver richesto la DEMO dell'applicazione.
Presto la contatteremo per darle l'accesso DEMO al portale.

Grazie
Francesco Palazzini
    """
    customer_send_from       = "no-reply@palazzinifrancesco.com"
    customer_msg             = MIMEText(customer_message)
    customer_msg['Subject']  = "TECHRIDE.IT - Accesso DEMO"
    customer_msg['From']     = customer_send_from
    customer_msg['Reply-To'] = customer_send_from
    customer_msg['To']       = customer_email 

    s = smtplib.SMTP_SSL(smtp_host, smtp_port, smtp_domain)
    s.set_debuglevel(1)
    s.login(smtp_user, smtp_password)

    s.sendmail(send_from, [send_to], msg.as_string())
    s.sendmail(customer_send_from, [customer_email], customer_msg.as_string())
    s.quit()

    response = {
        "statusCode": 200,
        "body": json.dumps('{"success": true}')
    }

    return response
