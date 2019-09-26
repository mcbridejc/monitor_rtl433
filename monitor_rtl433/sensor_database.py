from datetime import datetime 
import dateutil.parser as parser

def sanitize_sensor_record(r):
    """Fix any inconsistencies in the way rtl_433 returns json
    """
    r2 = r.copy()
    if 'sensor_id' in r2 and 'id' not in r2:
        r2['id'] = r2['sensor_id']
        del r2['sensor_id']
    return r2

class SensorDatabase(object):
    HASH_KEYS = ['model', 'id', 'channel']

    def __init__(self):
        self.sensors = {}
    
    def store(self, record):
        record = sanitize_sensor_record(record)
        key = tuple([record[k] for k in self.HASH_KEYS & record.keys()])

        self.sensors[key] = record

    def all(self):
        return list(self.sensors.values())

    def recent(self, max_age=5 * 60):
        """Get only sensors that have been updated within `max_age` seconds
        """
        now = datetime.now()
        return [x for x in self.sensors.values() if (now - parser.parse(x['time'])).total_seconds() < max_age]