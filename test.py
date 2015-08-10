#!/usr/bin/python
#
import sys
sys.path.insert(0,"../PyISY")

import PyISY
from time import sleep
from functools import partial
import logging

# load settings
f = open('config.txt', 'r')
ADDR = f.readline().strip()
PORT = f.readline().strip()
USER = f.readline().strip()
PASS = f.readline().strip()
f.close()

logfile = "test.log"
logging.basicConfig(filename=logfile);
logger = logging.getLogger()
logger.setLevel(0)

info = "Starting PyISY: ADDR=" + ADDR + " PORT=" + PORT
print(info + " LOG=" + logfile)
logger.info(info)

import pdb; pdb.set_trace()

isy = PyISY.ISY(ADDR, PORT, USER, PASS, False, "1.1", logger)
print("Connected: ",isy.connected)
isy.auto_update = True
#print(isy.nodes.nids)
#NODE = '21 8F 5B 1'
#node = isy.nodes[NODE]
#node.off()
#sleep(5)
#node.on()

#var = isy.variables[2][142]
#print(var.val)
#var.val = 6
#print(var.val)

def change_fun(e, name):
    print(name, 'changed to', str(e.handles))

var = isy.variables[2]['s.Pyl.Test']
print(var.val)
var.val.subscribe('changed', partial(change_fun,name='s.Pyl.Test'))
print("Sleeping...")
sleep(120)
#print(var.val)
