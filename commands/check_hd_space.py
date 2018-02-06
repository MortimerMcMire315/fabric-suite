from fabric.api import sudo,env,settings,parallel
import re

def execute():
    ext4s = sudo("df -h -t ext4 | grep -v Filesystem", quiet=True).split('\n')
    for ext4 in ext4s:
        fill = re.sub(r'.* ([0-9]{1,3})% .*',r'\1',ext4)
        if int(fill) > 75:
            print("Warning: " + env.host_string + " - " + fill + "% full")
