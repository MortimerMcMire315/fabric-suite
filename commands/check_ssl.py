from fabric.api import sudo,env,settings,parallel
from fabric.contrib import files as fabfiles
from fabric.context_managers import cd
from dateutil import parser
from datetime import datetime, timedelta, timezone

def get_certs():
    proto_possible_certs = sudo("grep -sRE 'ssl_certificate[^_]' /etc/nginx/sites-enabled", quiet=True).split('\r\n')
    possible_certs = sudo("grep -soRE 'ssl_certificate[[:space:]]+[^;]+;.*$' /etc/nginx/sites-enabled | awk '{print $2}' | awk '-F;' '{print $1}'",quiet=True).split('\r\n')
    possible_certs = list(map(lambda i: i.strip(), possible_certs))

    #sanity check
    assert len(possible_certs) == len(proto_possible_certs)

    return possible_certs

def execute():
    certs = get_certs()
    for cert in certs:
        if fabfiles.exists(cert):
            raw_expdate=sudo("openssl x509 -enddate -noout -in " + cert + " | awk -F= '{print $2}'", quiet=True)
            expdate=parser.parse(raw_expdate)
            one_month_before = timedelta(days=-31)
            if datetime.now(timezone.utc) > (expdate + one_month_before):
                print_info("Certificate expires soon! Expiration date: " + str(expdate), "WARNING")
            else:
                print_info("Certificate expires " + str(expdate))
        else:
            print_info("Referenced certificate " + cert + " not found.", "WARNING")


def print_info(x, level="INFO"):
    print("[" + level + "] [" + env.host_string + "] : " + x)
