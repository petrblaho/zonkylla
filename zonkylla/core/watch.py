#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017  zonkylla Contributors see COPYING for license

'''Zonky watch module'''

from datetime import datetime, timedelta
import subprocess
from time import sleep

def watch_loans(zonky, callbacks=None, minutes=1):
    '''Watches for new Loans at marketplace'''
    if callbacks is None:
        callbacks = []
    interval = timedelta(minutes=minutes)

    while True:
        try:
            current_time = datetime.now()
            loans = zonky.get_loans(from_dt=(current_time - interval))
            for callback in callbacks:
                callback(loans)
            sleep(60*minutes)
        except KeyboardInterrupt:
            break

def print_loans(loans=None):
    '''Print Loans'''
    if loans is None:
        loans = []
    print(loans)

def notify(messages):
    '''Send Linux desktop notification'''
    for message in messages:
        notification_message = ''
        notification_message += str(message['rating']) + ' - '
        notification_message += str(message['interestRate'] * 100.0) + '% - '
        notification_message += str(message['termInMonths']) + 'm - '
        notification_message += str(message['url'])

        notification_options = 'notify-send -a zonkylla -t 5000'.split()
        notification_options.append(notification_message)
        subprocess.run(notification_options)
