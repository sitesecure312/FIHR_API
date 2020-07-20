__author__ = "mauricio"

import time
import json

DELAY=1

credentials = [
                '{"username":"sam.s.smith", "password":"MyFood4Health!"}',
                '{"username":"nancy.anderson", "password":"OneHabit,2beU"}',
                '{"username":"charlie.miller", "password":"1ce.Upon.a.Time"}',
                '{"username":"mark.taylor", "password":"Going4ther$"}',
                '{"username":"karen.young", "password":"What1This?"}'
              ]

fileout = 'records.csv'

from FHIR import *

cls = Philips_FHIR()

if not cls.get_token():
    cls.finish(1)

outfile=open(fileout, 'a')

for c in credentials:

    if not cls.login(c):
        cls.finish(1)

    if not cls.get_patient():
        cls.finish(1)

    if not cls.get_observation(next=False):
        cls.finish(1)

    while cls.get_observation():
        time.sleep(DELAY)
        continue

    for record in cls.records:
        record.update(cls.metadata)
        json.dump(record, outfile)
        outfile.write('\n')

    cls.logout()

    time.sleep(10)
