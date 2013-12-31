
## Installation of smartmontools and postfix

# ####Goal: Monitor the health of attached hard drives and send an email alert about a failure or pending failure.

# The information on the web is scattered and sometimes missing.  This program
# is based on information found at or on the following:
# 
# * http://blog.shadypixel.com/monitoring-hard-drive-health-on-linux-with-smartmontools/
# * http://mhawthorne.net/posts/postfix-configuring-gmail-as-relay.html
# * man smartd.conf
# * http://www.howtoforge.com/checking-hard-disk-sanity-with-smartmontools-debian-ubuntu
# 
# This notebook is designed to be run as a python program, not as a notebook.
# 
# After it is complete you may manually check the self test logs with the following command:
#     
#     sudo smartctl -l selftest /dev/sda
# 
# Where /dev/sda can be any disk drive listed with the following command:
# 
#     sudo fdisk -l | grep "Disk /dev"
# 

### Get gmail address and password

# In[4]:

import getpass
mod = [] # list of modifications that were made
gmail_address = raw_input("Enter your gmail address (user@gmail.com): ")
print("Your password input will not be echoed")
gmail_password = getpass.getpass("Enter your gmail password: ")
gmail_ID, domain = gmail_address.split('@')
assert domain.lower()=='gmail.com', "You must use a gmail address"




### Installing packages

# In[20]:

import os


# In[ ]:

text = """Installing the following:
    smartmontools 
    smart-notifier 
    postfix
    """
mod+=text.split('\n')
print(text)
os.system('sudo apt-get install smartmontools smart-notifier postfix --assume-yes')


##### Get user's id

# In[ ]:

from subprocess import check_output
id_user = 'echo $USER'
user_byte = check_output(id_user,shell=True)
user = user_byte.decode('ascii')
#print(user)


### Modifying configuration files

#### smartmontools

# remove the # in the lines that read
#     #start_smartd=yes
#     #smartd_opts="--interval=1800"
# from the /etc/default/smartmontools file

# In[24]:

content = []
original = []
with open('/etc/default/smartmontools', 'r') as f:
    for line in f:
        original.append(line)
        if 'start_smartd=yes' in line or 'smartd_opts="--interval=1800"' in line:
            text = line.strip('#')
        else:
            text = line
        content.append(text)
Files = os.listdir('.')
if "smartmontools_orig" not in Files:
    with open('smartmontools_orig', 'w') as f:
        text = "Writing the original contents of /etc/default/smartmontools to smartmontools_orig"
        mod+=[text]
        print(text)
        for line in original:
            f.write(line)
with open('smartmontools', 'w') as f:
    for line in content:
        f.write(line)


#### Copy smartmontools back to /etc/default/smartmontools

# In[ ]:

os.system('sudo cp smartmontools /etc/default/smartmontools')


### Edit /etc/postfix/main.cf

##### Get the current file

# In[52]:

content = []
original = []
with open('/etc/postfix/main.cf', 'r') as f:
    for line in f:
        original.append(line)
        if 'relayhost =' in line and 'smtp' not in line:
            text = '#'+line
        else:
            text = line
        content.append(text)
if "main.cf_orig" not in Files:
    with open('main.cf_orig', 'w') as f:
        text = "Writing the original contents of /etc/postfix/main.cf to main.cf_orig"
        mod+=[text]
        print(text)
        for line in original:
            f.write(line)


# Out[52]:

#     Writing the original contents of /etc/postfix/main.cf to main.cf_orig
# 

# In[53]:

additional = """# sets gmail as relay
relayhost = [smtp.gmail.com]:587 

#  use tls
smtp_use_tls=yes

# use sasl when authenticating to foreign SMTP servers
smtp_sasl_auth_enable = yes 

# path to password map file
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd

# list of CAs to trust when verifying server certificate
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt

# eliminates default security options which are imcompatible with gmail
smtp_sasl_security_options ="""
add = additional.split('\n')
content+='\n'
for line in add:
    skip = False
    text = line.strip()
    #print text
    for entry in content:
        comp = entry.strip()
        if text in comp:
            skip = True
            #print("skiping")
            break
    #print(skip)
    if not skip:
        content+=[line+'\n']


# In[55]:

with open('main.cf', 'w') as f:
    for line in content:
        f.write(line)


##### Copy main.cf to /etc/postfix/main.cf

# In[ ]:

os.system('sudo cp main.cf /etc/postfix/main.cf')


### Edit /etc/smartd.conf

# In[61]:

print("Based on information found at: ")
print("http://blog.shadypixel.com/monitoring-hard-drive-health-on-linux-with-smartmontools/")
print("and using information found in: man smartd.conf \n")

additional = """DEVICESCAN -a \ #Monitor all health activities on all connected drives.
           -I 194 \ #Ignore the temperature fluctuations on the SATA drives
           -W 4,45,55 \ #Warn when the drive temperatures fluctuate more than 4 degC, or are outside 45 to 55 degC
           -R 5 \ #Monitor when sectors are realocated
           -l selfteststs \ #Report any problems with the selftests
           -s (S/../.././18|L/../../6/19) \ #Run a short test at 6pm every night and a long test at 7pm on Saturdays
           -m USERID@gmail.com \ #Email any detected problems to this email address
           """ #add '-M test'  #To test the email function upon startup 
additional = additional.replace('USERID',gmail_ID)
print("Adding the following to the /etc/smartd.conf file:\n")
print(additional)
print("\nThat information was found in man smartd.conf\n")
content = []
original = []
with open('/etc/smartd.conf', 'r') as f:
    for line in f:
        original.append(line)
        if len(line)>0:
            text = '#'+line
        else:
            text = line
        content.append(text)
if "smartd.conf_orig" not in Files:
    with open('smartd.conf_orig', 'w') as f:
        text = "Writing the original contents of /etc/smartd.conf to smartd.conf_orig"
        mod+=[text]
        print(text)
        for line in original:
            f.write(line)



# 

### Edit /etc/postfix/sasl_passwd 

# In[79]:

pwd = os.getcwd()
if os.path.exists('/etc/postfix/sasl_passwd'):
    cmd = 'cp /etc/postfix/sasl_passwd "'+pwd+'"/sasl_passwd_orig'
    #print cmd
    os.system(cmd)
    text = "Writing the original contents of /etc/postfix/sasl_passwd to sasl_passwd_orig"
    mod+=[text]
    print(text)
else:
    with open("sasl_passwd_orig",'w') as f:
        f.write('')
found = False
content = []
add = "[smtp.gmail.com]:587  username:password\n".replace("username:password",gmail_ID+":"+gmail_password)
with open("sasl_passwd_orig",'r') as f:
    for line in f:
        if add in line:
            found = True
        content.append(line)

if not found:
    content.append(add)
with open("sasl_passwd",'w') as f:
    for line in content:
        f.write(line)


# Out[79]:

#     Writing the original contents of /etc/postfix/sasl_passwd to sasl_passwd_orig
# 

# In[69]:

os.system('sudo cp sasl_passwd /etc/postfix/sasl_passwd')
os.system('sudo postmap /etc/postfix/sasl_passwd')
os.system('sudo chown postfix /etc/postfix/sasl_passwd*')
os.system('sudo updatedb')
os.system('sudo /etc/init.d/postfix reload')
with open(".forward",'w') as f:
    f.write(gmail_address)
print("Writing the .forward file to your /home/%s directory and to the /root directory."%user)
os.system('cp .forward ~/.forward')
os.system('sudo cp .forward /root/.forward')




### Validate Email

# In[85]:

print("Testing email:")
print("    You should recieve an email with a subject of 'Email Test' at the email you have specified.")
os.system('mail -s "Email Test" %s@gmail.com'%gmail_ID)
print("    If you do not then there is a problem with your email setup.")
print("Please check: http://mhawthorne.net/posts/postfix-configuring-gmail-as-relay.html for trouble shooting.")


# Out[85]:

#     Testing email:
#         You should recieve an email with a subject of 'Email Test' at the email you have specified.
#         If you do not then there is a problem with your email setup.
#     Please check: http://mhawthorne.net/posts/postfix-configuring-gmail-as-relay.html for trouble shooting.
# 

# In[88]:

print('''Now that the installation is complete you may manually check the self test logs with the following command:
    
    sudo smartctl -l selftest /dev/sda

Where /dev/sda can be any disk drive listed with the following command:

    sudo fdisk -l | grep "Disk /dev"''')


# Out[88]:

#     Now that the installation is complete you may manually check the self test logs with the following command:
#         
#         sudo smartctl -l selftest /dev/sda
#     
#     Where /dev/sda can be any disk drive listed with the following command:
#     
#         sudo fdisk -l | grep "Disk /dev"
# 

# In[ ]:

os.system("sudo /etc/init.d/smartmontools start")

