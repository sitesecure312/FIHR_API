
from pandas import DataFrame
import datetime
import collections
import logging
import json
import iso8601
import pytz
import numpy as np

def flatten(d, parent_key='', sep='.'):
    """
    Flattens a dictionary
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)

def map_metrics(row):

    field = row['content.name.coding']
    metric=field[0]['display']

    try:
        metric=field[1]['display']
    except:
        pass

    return metric

def parse_iso8601_date(row, field):
    try:
        return iso8601.parse_date(row[field]).astimezone(pytz.utc).replace(tzinfo=None)
    except:
        return np.nan

class FIHR_stats(object):

    def __init__(self):
        self.now = datetime.datetime.utcnow().replace(second=0, microsecond=0)
        logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s', level=logging.INFO)
        self.log = logging.getLogger("FIHR_stats")
        self.data = []

    def load_stats(self, filename):
        with open(filename) as f:
            for line in f:
                self.data.append(json.loads(line))

    def stats_to_df(self):

        array = []

        try:
            for record in self.data:

                try:
                    row = flatten(record)
                    array.append(row)

                except Exception as e:
                    print "Exception: %s" % e

        except KeyError:
            self.log.info("Key Error")

        self.df = DataFrame.from_dict(array)
