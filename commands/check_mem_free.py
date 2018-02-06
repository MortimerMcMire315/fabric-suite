from fabric.api import sudo,env,settings,parallel

def execute():
    mem_total = int(sudo("cat /proc/meminfo | grep 'MemTotal' | awk -F: '{print $2}' | tr -d ' ' | sed -re 's/kB//g'", quiet=True))
    mem_free = int(sudo("cat /proc/meminfo | grep 'MemFree' | awk -F: '{print $2}' | tr -d ' ' | sed -re 's/kB//g'", quiet=True))

    percentage_used = 100 * (1 - (mem_free / mem_total))
    print(env.host_string + " : " + "{:.1f}".format(percentage_used) + "%")
