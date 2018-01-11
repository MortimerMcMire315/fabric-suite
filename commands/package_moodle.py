from fabric.api import sudo,env,settings,parallel
from fabric.context_managers import cd
from util import get_cfgoption, get_moodle_root

def execute():
    moodleroot=get_moodle_root()
    username = env.host_string
    sudo("useradd -mg ssh -s /bin/bash " + username)
    datadir = get_cfgoption('dataroot')
    dbhost = get_cfgoption('dbhost')
    dbname = get_cfgoption('dbname')
    dbuser = get_cfgoption('dbuser')
    dbpass = get_cfgoption('dbpass')
    data_archive = username + "_moodledata.tar.gz"
    core_archive = username + "_moodlecore.tar.gz"
    db_dump = "./" + username + "_db.sql.gz"
    password = sudo("< /dev/urandom tr -dc A-Za-z0-9 | head -c16; echo", quiet=True)
    with cd("/home/" + username):
        sudo("mysqldump -h " + dbhost + " -u " + dbuser + " -p" + dbpass + " " + dbname + " | gzip > " + db_dump)
        sudo("tar -C " + sudo("dirname " + moodleroot, quiet=True) + " -czf " + core_archive + " " + sudo("basename " + moodleroot, quiet=True))
        sudo("tar -C " + sudo("dirname " + datadir, quiet=True) + " -czf " + data_archive + " " + sudo("basename " + datadir, quiet=True))
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
