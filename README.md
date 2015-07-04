Disk_Monitoring
===============

This is for the semi-automated installation of smartmontools and postfix to monitor hard drive health.

My goal is to setup monitoring the health of attached hard drives and send an email alert about a failure or pending failure.  In particular while using a software RAID system.

The information on the web is scattered and sometimes missing. The python program is based on information found at or on the following:

* http://blog.shadypixel.com/monitoring-hard-drive-health-on-linux-with-smartmontools/
* http://mhawthorne.net/posts/postfix-configuring-gmail-as-relay.html
* man smartd.conf
* http://www.howtoforge.com/checking-hard-disk-sanity-with-smartmontools-debian-ubuntu

This notebook is designed to be run as a python program, not as a notebook.

After it is complete you may manually check the self test logs with the following command:

    sudo smartctl -l selftest /dev/sda

Where /dev/sda can be any disk drive listed with the following command:

    sudo fdisk -l | grep "Disk /dev"

To see the code in an IPython notebook form click on the link below.

[Notebook](http://nbviewer.ipython.org/github/damontallen/Disk_Monitoring/blob/master/Installing.ipynb)

To use this program, either download a zipped verion of the code and unzip it or clone the repo with the command:
    
    git clone https://github.com/damontallen/Disk_Monitoring.git

Navigate to the directory containing the Installing.py file and enter the following command:

    sudo python Installing.py
    
## Trouble Shooting

Information about trouble shooting is at the end of the [notebook](http://nbviewer.ipython.org/github/damontallen/Disk_Monitoring/blob/master/Installing.ipynb).
