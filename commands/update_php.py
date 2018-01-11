from fabric.api import sudo
from fabric.context_managers import cd

def get_php_version():
    return sudo("php -r 'echo phpversion();' | sed -re 's/[^0-9]*([0-9]+\.[0-9]+)\..*/\\1/g'")

def execute():
    v = get_php_version().strip()
    if v == '5.6':
        print("Already up-to-date.")
    elif v == '5.5':
        do_update()
    else:
        print("Unsupported PHP version: " + v)
    return

def do_update():
    with cd('/home/ubuntu'):
        sudo('mkdir 12-2017_upgrade_workspace')
        with cd('12-2017_upgrade_workspace'):
            nginx_confs = sudo("for f in /etc/nginx/sites-enabled/*; do echo $f; done").replace("\r","").split("\n")
            sudo('''apt-get -y purge `dpkg -l | grep php | awk '{print $2}' |tr "\n" " "`''')
            sudo("add-apt-repository -y ppa:ondrej/php")
            sudo("apt-get -y update")
            sudo("apt-get -y install php5.6 php5.6-common php5.6-fpm php5.6-curl php5.6-zip php5.6-gd php5.6-mysql php5.6-xml php5.6-json php5.6-soap php5.6-xmlrpc php5.6-intl php5.6-mbstring php5.6-ldap")
            for nginx_conf in nginx_confs:
                bn = sudo("basename " + nginx_conf)
                sudo("cp " + nginx_conf + " ./" + bn + ".bak")
                print("Replacing socket in " + nginx_conf)
                sudo("sed --in-place -re 's/unix:\/var\/run\/php5-fpm.sock/unix:\/var\/run\/php\/php5.6-fpm.sock/g' " + nginx_conf)
            sudo("nginx -s reload")

            sudo("cp /etc/php/5.6/fpm/php.ini ./php.ini.bak")
            sudo("sed -i.bak -re 's/post_max_size *=.*/post_max_size = 800M/g' /etc/php/5.6/fpm/php.ini")
            sudo("sed -i.bak -re 's/upload_max_filesize *=.*/upload_max_filesize = 800M/g' /etc/php/5.6/fpm/php.ini")
            sudo("service php5.6-fpm restart")
