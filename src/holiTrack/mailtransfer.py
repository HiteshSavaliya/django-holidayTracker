'''
Created on 6 Feb 2013

@author: hitesh
'''
def send_email(toemail,subject,body):
    import smtplib
    
    gmail_user = "hitesh.savaliya@gmail.com"
    gmail_pwd = "XXXXXXX"
    FROM = 'hitesh.savaliya@gmail.com'
    TO = [toemail] #must be a list
    
    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), subject, body)
    try:
        #server = smtplib.SMTP(SERVER) 
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        #server.quit()
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"
        
#send_email()