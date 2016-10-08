#! /usr/bin/python
import sys
import os
import json

CONFIG_FILE = '/etc/serf/serf.json'


def get_hostname():
    with open('/allconf/hostname.conf', 'r') as f:
        for line in f:
            return line.strip().split('=')[-1]


def get_ip_addr(hostname):
    return '.'.join(hostname.rsplit('-', 4)[-4:])


def generate_config_file(role, bind_port, rpc_port, master_addr):
    hostname = get_hostname()
    addr = get_ip_addr(hostname)
    data = {}
    data["node_name"] = hostname
    data["tags"] = {"role": role}
    data["bind"] = addr + ':' + bind_port
    data["rpc_addr"] = "127.0.0.1:" + rpc_port
    data["log_level"] = "warn"
    data["retry_interval"] = "30s"
    data["retry_join"] = [master_addr]
    data["replay_on_join"] = True
    data["snapshot_path"] = "/var/log/serf_snapshot.log"
    data["encrypt_key"] = "NUNBQscg1UkEeM2sC+lsVw=="

    with open(CONFIG_FILE, "w") as f:
        f.write(json.dumps(data, indent=2, sort_keys=True))


def update_config_file():
    hostname = get_hostname()
    addr = get_ip_addr(hostname)

    with open(CONFIG_FILE) as f:
        data = json.load(f)
        old_addr, port = data["bind"].split(':')
        old_hostname = data["node_name"]
        if addr == old_addr and hostname == old_hostname:
            return False
        data["bind"] = addr + ':' + port
        data["node_name"] = hostname

    with open(CONFIG_FILE, "w") as f:
        f.write(json.dumps(data, indent=2, sort_keys=True))

    return True

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            if update_config_file():
                os.system('service serf restart')
                os.system('supervisorctl restart que')
        elif len(sys.argv) == 5:
            generate_config_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
            os.system('chkconfig serf on')
            os.system('service serf start')
        else:
            print('Usage:setup.py role bind_port rpc_port master_addr')
        exit(0)
    except Exception, e:
        print(e)
        exit(1)
