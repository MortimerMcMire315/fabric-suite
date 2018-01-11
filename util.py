from fabric.api import sudo,env,settings
from fabric.context_managers import cd
from functools import wraps
from fabric.contrib.console import confirm

def dangerous(f):
    @wraps(f)
    def wrapper(*args, **kw):
        result = confirm("This may have disastrous effects. Is everything backed up? ")
        if result:
            f(*args, **kw)
        else:
            exit(1)
    return wrapper

def get_moodle_root():
    if env.host_string == 'wemta':
        return '/var/www/moodle/battle'
    if env.host_string == 'eclass':
        return '/var/www/wordpress/courses'
    if env.host_string == 'crowd':
        return '/home/crowdmanagers/public_html/moodle'
    possible_roots=sudo("grep -RE '^[^#]*root' /etc/nginx/sites-available/ | grep -vE '(wordpress|totara|moodle_test|moodle32|fastcgi_param|moodle.bak)' | awk '{$1=\"\";print}' | grep -v '/usr/share/nginx/html'",quiet=True,shell=False).split('\n')
    possible_roots=set([i.strip() for i in possible_roots])

    if len(possible_roots) > 1:
        print("%s has more than one possible root: " % env.host_string)
        print(possible_roots)
        exit(1)

    real_root=list(possible_roots)[0].split(' ')[1]
    if real_root[len(real_root) - 1] == ';':
        real_root = real_root[0:len(real_root) - 1]
    return real_root

def get_cfgoption(opt_name):
    moodleroot = get_moodle_root()
    config = moodleroot + "/config.php"
    return sudo("grep -E '[^\/\$]*\$CFG->" + opt_name + "' " + config + " | awk '-F=' '{print $2}' | awk '-F;' '{print $1}'", quiet=True, shell=False)

def set_cfgoption(cfg_file, opt_name, new_val):
    print(opt_name)
    print(new_val)
    sed_string = "sed -i.bak -re 's/(" + opt_name + """ *=[^'\\''"]*['\\''"]).+(['\\''"].*$)/\\1""" + new_val.replace('/','\\/') + """\\2/' """ + cfg_file
    print(sed_string)
    sudo(sed_string)
