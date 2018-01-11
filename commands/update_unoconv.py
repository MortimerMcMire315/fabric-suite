from fabric.api import sudo,settings
from fabric.context_managers import cd

def execute():
    with settings(warn_only=True):
        sudo("mv /usr/bin/unoconv /usr/bin/unoconv_bak", quiet=True)
    with cd("/usr/bin"):
        sudo("wget https://raw.githubusercontent.com/dagwieers/unoconv/master/unoconv")
        sudo("sed --in-place -re 's/^(#!\/usr\/bin\/env )python/\\1python3/' /usr/bin/unoconv")
        sudo("chmod ugo+x /usr/bin/unoconv")
        sudo("apt-add-repository -y ppa:libreoffice/ppa")
        sudo("apt-get -y update")
        sudo("apt-get -y install libreoffice")
