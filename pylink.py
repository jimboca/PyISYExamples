#!/usr/bin/python
#
# sudo dpkg-reconfigure tzdata
# sudo apt-get install libyaml-cpp0.3
# sudo pip-3.2 install datetime
# sudo pip-3.2 install collections
# sudo pip-3.2 install pyaml
# sudo pip-3.2 install apscheduler
#
# TODO:
# - Check config params are defined
# - Add config to update every second

# When run in directory containing downloaded PyIsy
import sys
sys.path.insert(0,"../PyISY")

# Load our dependancies
import re
import requests
import logging
import yaml
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import PyISY
from asus import AsusDeviceScanner

# Load the config file.
config_file = open('config.yaml', 'r')
config = yaml.load(config_file)
config_file.close

# Start the log_file
print('pylink: Started: %s' % datetime.now())
logfile = config['log_file']
print('pylink: Writing to log: ' + config['log_file'])
logging.basicConfig(filename=config['log_file']);
logger = logging.getLogger()
logger.setLevel(0)
info = "Startinsg PyISY: host=" + config['isy_host'] + " PORT=" + str(config['isy_port']) + "log=" + logfile
logger.info(info)

isy = PyISY.ISY(config['isy_host'], config['isy_port'], config['isy_user'], config['isy_password'], False, "1.1", logger)
logger.info("Connected: " + str(isy.connected))
isy.auto_update = True

def second_function():
    print('second_function: The time is: %s' % datetime.now())

def minute_function():
    logger.debug('minute_function: The minute is: %s' % datetime.now().minute)
    isy.variables[2]['s.PyISY.Minute'].val = datetime.now().minute

def router_check():
    sc = AsusDeviceScanner(config['router_host'],config['router_user'],config['router_password'])
    if sc.client_connected("android-8c4066f") is True:
        isy.variables[2]['s.OC.JimConnected.Router'].val = 1
    else:
        isy.variables[2]['s.OC.JimConnected.Router'].val = 0

def hour_function():
    logger.debug('hour_function: The hour is: %s' % datetime.now().hour)
    isy.variables[2]['s.PyISY.Hour'].val = datetime.now().hour

def day_function():
    dt = datetime.now()
    print('day_function: It is a new day!  The time is: %s' % dt)
    isy.variables[2]['s.PyISY.Day'].val = dt.day
    isy.variables[2]['s.PyISY.Month'].val = dt.month
    isy.variables[2]['s.PyISY.Year'].val = dt.year

# Initialize all on startup
minute_function()
hour_function()
day_function()
router_check()

sched = BlockingScheduler()

# Schedules second_function to be run at the change of each second.
#sched.add_job(second_function, 'cron', second='0-59')

# Schedules minute_function to be run at the change of each minute.
sched.add_job(minute_function, 'cron', second='0')

# Schedules hour_function to be run at the change of each hour.
sched.add_job(hour_function, 'cron', minute='0', second='0')

# Schedules day_function to be run at the start of each day.
sched.add_job(day_function, 'cron', minute='0', second='0', hour='0')

sched.add_job(router_check, 'cron', minute="10,20,30,40,50")

sched.start()
