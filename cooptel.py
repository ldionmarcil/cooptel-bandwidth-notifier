import os
import urllib
import urllib2
import re
import base64
import ConfigParser
from datetime import date
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

def sendMail(subject, message):
    message = MIMEText(message)
    message["To"] = config.get("recipient", "email")
    message["Subject"] = subject
    #feel free to modify this to suit your setup, or create a symbolic link
    process = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE) 
    process.communicate(message.as_string())

config = ConfigParser.ConfigParser()
config.read("%s/cooptel.conf" % os.path.dirname(os.path.abspath(__file__)))
username = config.get("Credentials", "username")
password = config.get("Credentials", "password")
url = 'http://www2.cooptel.qc.ca/services/temps/index.php'

values = {'mois' : date.today().month, # specifies the current month
          'cmd' : 'Visualiser'}

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
#Basic access authentication as defined in RFC1945
base64_credentials = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
req.add_header("Authorization", "Basic %s" % base64_credentials)

response = urllib2.urlopen(req)
the_page = response.read()

utilisation_reg = re.match(r'.*[ ]+([0-9.]+)</B></TD>\n    <TD ALIGN="RIGHT"><B>[ ]+([0-9.]+)</B>.*', the_page, re.S)
quota_reg = re.match(r'.*riode</TD><TD ALIGN="RIGHT">([0-9]+)<.*', the_page, re.S)

if (utilisation_reg.group(2),quota_reg.group(1)) != (None,None): #response appears valid
    download_currently = float(utilisation_reg.group(1))
    upload_currently = float(utilisation_reg.group(2))
    total_currently = download_currently + upload_currently
    
    data_quota = float(quota_reg.group(1))
    
    used_data_percentage = total_currently/data_quota*100
    warning_percentage = int(config.get("warnings", "percentage"))
    
    if used_data_percentage > warning_percentage: #send email when true
        message = "Used: %.2f Mo. (%.2f%%) [D:%.2f|U:%.2f]" % (total_currently, used_data_percentage, download_currently, upload_currently)
        sendMail("Critical bandwidth level", message)
else:
    sendMail("Cooptel bandwidth fetcher", "Could not properly fetch Cooptel data.")

