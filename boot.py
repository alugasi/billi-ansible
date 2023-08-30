#!/usr/bin/env python3

from redfish import Redfish
import sys
import yaml
import socket

inventory = sys.argv[1] if len(sys.argv) > 1 else 'inventory'
nodes = int(sys.argv[2]) if len(sys.argv) > 2 else 3
with open(inventory) as f:
    data = yaml.safe_load(f)['all']['vars']


default_bmc_user = data.get('bmc_user', 'root')
default_bmc_password = data.get('bmc_password', 'calvin')
default_bmc_model = data.get('bmc_model', 'dell')

iso_url = data.get('iso_url')
if not iso_url:
    ipaddr = socket.gethostbyname(socket.gethostname())
    cluster = data.get('cluster')
    iso_url = f"http://{ipaddr}/{cluster}.iso"
print ("****************** DEBUG ************** isourl = ", iso_url)

hosts = data['hosts']
for index, host in enumerate(hosts):
    if index >= nodes:
        break
    bmc_url = host.get('bmc_url')
    bmc_user = host.get('bmc_user', default_bmc_user)
    bmc_password = host.get('bmc_password', default_bmc_password)
    bmc_model = host.get('bmc_model', default_bmc_model)
    if bmc_url is not None:
        red = Redfish(bmc_url, bmc_user, bmc_password, model=bmc_model)
        red.set_iso(iso_url)
