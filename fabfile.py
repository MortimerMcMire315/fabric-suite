from fabric.api import sudo,env,settings,parallel,task

from util import dangerous

import commands.check_ssl          as cmd_check_ssl
import commands.update_unoconv     as cmd_update_unoconv
import commands.update_php         as cmd_update_php
import commands.switch_database    as cmd_switch_database
import commands.package_moodle     as cmd_package_moodle
import commands.setup_test_site    as cmd_setup_test_site
import commands.fix_aws_cloudwatch as cmd_fix_aws_cloudwatch

"""
I have a file called host_list.py containing my host aliases. Since this is
mildly-sensitive data, I am withholding it from the repo.

KNOWN_HOSTS is just a list of host strings that can be put into env.hosts.
"""
from host_list import KNOWN_HOSTS

env.use_ssh_config = True

"""
If no host given, execute on all.
"""
if not env.hosts:
    env.hosts = KNOWN_HOSTS

@task
def check_ssl():
    cmd_check_ssl.execute()

@task
def update_unoconv():
    cmd_update_unoconv.execute()

@task
@dangerous
def update_php():
    cmd_update_php.execute()

@task
def get_php_version():
    cmd_update_php.get_php_version()

@task
@dangerous
def switch_database():
    cmd_switch_database.execute()

@task
@dangerous
def package_moodle():
    cmd_package_moodle.execute()

@task
@dangerous
def setup_test_site():
    cmd_setup_test_site.execute()


"""
Regenerate AWS instance id; fix server datetime
"""
@task
@dangerous
def fix_aws_cloudwatch():
    cmd_fix_aws_cloudwatch.execute()
