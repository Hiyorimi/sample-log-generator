#!/usr/bin/env python

import time
import sys
from random import randrange
import numpy as np
import telnetlib
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open('defaults.cfg'))

try:
    MAX_USERS = config.getint("log_generator",'MAX_USERS')
except:
    MAX_USERS = 10000
    
HOST = config.get("log_generator",'HOST')
PORT = config.getint("log_generator",'PORT')

try:
    DELAY = config.getfloat("log_generator",'DELAY')
    if DELAY > 1:
        DELAY = 1
except:
    DELAY = 1

try:
    TELNET_DEBUGLEVEL = config.getint("log_generator",'TELNET_DEBUGLEVEL')
except:
    TELNET_DEBUGLEVEL = 0
    
sample_events_shape, sample_events_scale = 3., 2.# mean and dispersion

def dice_rolling (denominator):
    dice = randrange(denominator)
    if dice == 0:
        return True
    return False

def generate_random_log_entry (user_id):
    
    log_entry = ''
    
    # Event type
    event_roll = np.random.random()
    duration = 0   
    event_type = ''
    
    event_owner_id = randrange(MAX_USERS)
    event_id = randrange(29)
    
    if event_roll > 0.3:
        event_type = 'sample_event_1'
        duration = np.random.randint(1,15)
    elif event_roll < 0.85:
        event_type = 'sample_event_2'
    else:
        event_type = 'sample_event_3'
     
    log_entry += event_type + ";"
    log_entry += str(user_id) + ";"
    log_entry += str(event_owner_id) + ";"
    log_entry += str(event_owner_id) + str(event_id) + ";"
    
    if duration > 0:
        log_entry += str(duration)
    log_entry += "\n"
    
    return log_entry

try: 

    tn = telnetlib.Telnet(HOST, PORT)
    tn.set_debuglevel(TELNET_DEBUGLEVEL)
    counter = 0
    second_counter = 0.0

    while True:
        users_active = randrange(MAX_USERS / 100)
        user_id_start = randrange(MAX_USERS / 100)
        if second_counter >= 1:
            print counter
            second_counter = 0.0
            counter = 0
        for user_id in xrange(user_id_start*100, user_id_start*100 + users_active):
            #generate user activity for this second
            
            # 1 / 2 probability to do something
            if dice_rolling(2):
                try:
                    tn.write(generate_random_log_entry(user_id))
                    counter += 1
                except KeyboardInterrupt:
                    exit(0)
                except all:
                    tn = telnetlib.Telnet(HOST, PORT)
                    pass
            
        second_counter += DELAY
        time.sleep(DELAY)

except KeyboardInterrupt:
    exit(0)
except all:
    pass
