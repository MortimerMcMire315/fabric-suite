from fabric.api import sudo,env,settings,parallel
from fabric.context_managers import cd
from util import get_moodle_root, get_cfgoption

WORKSPACE='09_2017_upgrade_workspace'

def execute():
    old_dbhost = get_cfgoption('dbhost').strip("'")
    old_dbname = get_cfgoption('dbname').strip("'")
    old_dbuser = get_cfgoption('dbuser').strip("'")
    old_dbpass = get_cfgoption('dbpass').strip("'")
    root_dbuser = "shared1"
    root_dbpass = "XSZehFScggxKv6j9"
    new_dbhost = old_dbhost.replace("shared1","mysql57test")
    create_commands = '"CREATE DATABASE ' + old_dbname + ' DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;' + \
                      "CREATE USER " + old_dbuser + "@'%' IDENTIFIED BY '" + old_dbpass + "';" + \
                      "GRANT ALL ON " + old_dbname + ".* TO " + old_dbuser + "@'%';\""
    sudo("echo " + create_commands + " | mysql -h " + new_dbhost + " -u " + root_dbuser + " -p" + root_dbpass)
    sudo("mysqldump -h " + old_dbhost + " -u " + old_dbuser + " -p" + old_dbpass + " " + old_dbname + " | " + \
          "mysql -h " + new_dbhost + " -u " + old_dbuser + " -p" + old_dbpass + " -D " + old_dbname)

    moodleroot = get_moodle_root()
    config = moodleroot + "/config.php"
    sudo("sed -i.bak -re 's/shared1/mysql57test/g' " + config)

    print(moodleroot)
    print(config)
    print(old_dbhost)
    print(old_dbpass)
