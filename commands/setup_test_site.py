from fabric.api import sudo,env,settings,parallel
from fabric.context_managers import cd
from util import get_cfgoption, set_cfgoption, get_moodle_root
import re

KNOWN_DB_SERVERS = ["shared1", "mysql57test"]

def enough_free_space():
    ext4s = sudo("df -h -t ext4 | grep -v Filesystem", quiet=True).split('\n')
    for ext4 in ext4s:
        fill = re.sub(r'.* ([0-9]{1,3})% .*',r'\1',ext4)
        print(fill + "%")
        if int(fill) > 40:
            return False
    return True

def clone_dir(dirname, appendix):
    newname = dirname + appendix

    if directory_exists(newname):
        print("Error: %s: directory already exists." % dirname)
        exit(1)

    sudo("cp -r " + dirname + " " + newname)
    return(newname)

def directory_exists(dirname):
    if sudo("if [ -d " + dirname + " ]; then echo 'found'; fi", quiet=True):
        return True
    return False

def execute(sitename):
    if not enough_free_space():
        print("Error: Not enough free space!")
        return False

    moodle_root = get_moodle_root()
    newroot=clone_dir(moodle_root, "_sandbox")
    sudo("chown -R www-data:www-data " + newroot)

    dataroot=get_cfgoption('dataroot')
    new_dataroot=clone_dir(dataroot, "_sandbox")
    sudo("chown -R www-data:www-data " + new_dataroot)
    sudo("chmod -R go+rwX " + new_dataroot)

    (new_dbname, new_dbhost) = copy_database("mysql57test")
    set_cfgoption(newroot + "/config.php", "dataroot", new_dataroot)
    set_cfgoption(newroot + "/config.php", "dirroot", newroot)
    set_cfgoption(newroot + "/config.php", "dbhost", new_dbhost)
    set_cfgoption(newroot + "/config.php", "dbname", new_dbname)

def copy_database(db_server):
    if not db_server in KNOWN_DB_SERVERS:
        print("Error: " + db_server + ": unknown database.")
        exit(1)

    old_dbhost = get_cfgoption('dbhost').strip("'")
    old_dbname = get_cfgoption('dbname').strip("'")
    old_dbuser = get_cfgoption('dbuser').strip("'")
    old_dbpass = get_cfgoption('dbpass').strip("'")
    new_dbname = old_dbname + "_sandbox"
    root_dbuser = "shared1"
    root_dbpass = "XSZehFScggxKv6j9"
    new_dbhost = old_dbhost.replace("shared1",db_server)
    create_commands = '"CREATE DATABASE ' + new_dbname + ' DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;' + \
                      "CREATE USER IF NOT EXISTS " + old_dbuser + "@'%' IDENTIFIED BY '" + old_dbpass + "';" + \
                      "GRANT ALL ON " + new_dbname + ".* TO " + old_dbuser + "@'%';\""
    sudo("echo " + create_commands + " | mysql -h " + new_dbhost + " -u " + root_dbuser + " -p" + root_dbpass)
    sudo("mysqldump -h " + old_dbhost + " -u " + old_dbuser + " -p" + old_dbpass + " " + old_dbname + " | " + \
          "mysql -h " + new_dbhost + " -u " + old_dbuser + " -p" + old_dbpass + " -D " + new_dbname)

    moodleroot = get_moodle_root()
    config = moodleroot + "/config.php"
    sudo("sed -i.bak -re 's/shared1/mysql57test/g' " + config)
    return (new_dbname, new_dbhost)

