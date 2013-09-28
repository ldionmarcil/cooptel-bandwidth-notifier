cooptel-bandwidth-notifier
==========================

Python 2.7 script that will send an email when your cooptel bandwidth usage reaches a certain percentage.
This script is best used with a running postfix server running locally, relaying to a third party SMTP, server for example. 
You have to modify cooptel.conf with your cooptel's username and password, the recipient email, and the warning percentage at which point you want to start receiving warning emails.
This script should be added to your crontab with a setup similar as this one:

0       12      *       *       *       /usr/sbin/python2.7 /home/user/cooptel-bandwidth-notifier/cooptel.py

This will execute the script every day at noon.
