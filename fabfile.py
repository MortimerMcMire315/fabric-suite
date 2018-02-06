from fabric.api import sudo,env,settings,parallel,task

from util import dangerous

import commands

import commands.check_ssl
import commands.update_unoconv
import commands.update_php
import commands.switch_database
import commands.package_moodle
import commands.setup_test_site
import commands.fix_aws_cloudwatch
import commands.create_sftp_account
import commands.check_hd_space
import commands.check_mem_free

"""
I have a file called hostlist.py containing my hostnames. Since this is
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
    commands.check_ssl.execute()

@task
def update_unoconv():
    commands.update_unoconv.execute()

@task
@dangerous
def update_php():
    commands.update_php.execute()

@task
def get_php_version():
    commands.update_php.get_php_version()

@task
@dangerous
def switch_database():
    commands.switch_database.execute()

@task
@dangerous
def package_moodle():
    commands.package_moodle.execute()

@task
@dangerous
def setup_test_site():
    commands.setup_test_site.execute()


"""
Regenerate AWS instance id; fix server datetime
"""
@task
@dangerous
def fix_aws_cloudwatch():
    commands.fix_aws_cloudwatch.execute()

@task
@dangerous
def create_sftp_account():
    commands.create_sftp_account.execute()

@parallel(20)
@task
def check_hd_space():
    commands.check_hd_space.execute()

@parallel(20)
@task
def check_mem_free():
    commands.check_mem_free.execute()
