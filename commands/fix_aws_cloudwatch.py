from fabric.api import sudo,env,settings

def execute():
    with settings(warn_only=True):
        sudo('rm /var/tmp/aws-mon/instance-id')
    sudo('crontab -l > /etc/crontab.bak')
    sudo('if [ -z "$(crontab -l | grep ntpdate)" ]; then (crontab -l; echo "7 */6 * * * ntpdate pool.ntp.org") | crontab -; fi')
    sudo('if [ ! -d /home/ubuntu/aws-scripts-mon ]; then cd /home/ubuntu; wget -O aws-scripts-mon.tar.gz \'https://drive.google.com/uc?export=download&id=0B8cHr_8HnFKYTllaamlUUnV6NW8\'; tar -zxvf aws-scripts-mon.tar.gz; apt-get -y install libwww-perl libdatetime-perl; else echo "AWS scripts already installed.";fi')
    sudo('ntpdate pool.ntp.org')
    sudo('/home/ubuntu/aws-scripts-mon/mon-put-instance-data.pl --mem-util --mem-used --mem-avail  --disk-space-util --disk-space-used --disk-space-avail --disk-path=/')
