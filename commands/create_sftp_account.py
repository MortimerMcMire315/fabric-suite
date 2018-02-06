from fabric.api import sudo,env,settings,parallel
from fabric.context_managers import cd
from util import get_cfgoption, get_moodle_root

def execute():
    username = env.host_string
    sudo("useradd -mg ssh -s /bin/bash " + username)
    password = sudo("< /dev/urandom tr -dc A-Za-z0-9 | head -c16; echo", quiet=True)
    sudo("chown -R " + username + " /home/" + username)
    sudo("echo -e \"" + password + "\\n" + password + "\" | passwd " + username)
    sudo("sed -i.bak -re 's/PasswordAuthentication +no/PasswordAuthentication yes/' /etc/ssh/sshd_config")
    sudo("service ssh restart")

    print("Send the following credentials to the user:")
    print("Protocol: SFTP (port 22)")
    print("Host: " + env.host)
    print("Username: " + username)
    print("Password: " + password)
    print("DON'T FORGET TO SET SECURITY GROUP TO SSH(Insecure) in AWS!!!")
