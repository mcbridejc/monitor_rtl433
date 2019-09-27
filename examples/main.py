from monitor_rtl433 import run
from monitor_rtl433.metrics import Metric, MetricFilter, MetricDescription

def degc2f(x):
    return x * 9.0/5.0 + 32.0

class AcuriteTower(MetricFilter):
    def __init__(self, id):
        self.id = id
        # The `_match` property will be used to determine which sensor records
        # this filter will be applied to
        self._match = {"model": "Acurite tower sensor", "id" : self.id}
        
    def process(self, r):
        """Takes a single sensor record, and converts it to 0 or more metrics
        """
        sensor_id = "%s%s" % (str(self.id), r['channel']) 
        yield Metric('temperature', degc2f(r['temperature_C']), labels={'sensor_id': sensor_id})
        yield Metric('humidity', r['humidity'], labels={'sensor_id': sensor_id})
        yield Metric('battery_warning', r['battery_low'], labels={'sensor_id': sensor_id})

class LaCrosse(MetricFilter):
    def __init__(self, id):
        self.id = id
        self._match = {"model": "TX141TH-Bv2 sensor", "id": self.id}

    def process(self, r):
        sensor_id = "LaCross_%s" % (str(self.id))
        battery_warning = 0
        if r['battery'] == "OK":
            battery_warning = 0
        elif r['battery'] == "LOW":
            battery_warning = 1
        else:
            battery_warning = 99 # Unrecognized. (I'm not sure right now what all the battery field options are)

        yield Metric('temperature', degc2f(r['temperature_C']), labels={'sensor_id': sensor_id})
        yield Metric('humidity', r['humidity'], labels={'sensor_id': sensor_id})
        yield Metric('battery_warning', battery_warning, labels={'sensor_id': sensor_id})

def main():
    # List all metric names that we will expose
    metric_descriptions = [
        MetricDescription("temperature", "gauge", "Temperature in degrees F"),
        MetricDescription("humidity", "gauge", "Relative humidity in percent"),
        MetricDescription("battery_warning", "gauge", "0 when battery normal, 1 when low"),
    ]
    # For each sensor that we want to convert to metrics, create a MetricFilter class that will do that
    metric_filters = [
        AcuriteTower(15352),
        LaCrosse(158),
    ]

    run(metric_descriptions, metric_filters)

if __name__ == '__main__':
    main()