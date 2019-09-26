from functools import reduce

class MetricDescription(object):
    ALLOWED_TYPES = ['counter', 'gauge', 'histogram', 'summary']
    def __init__(self, name, type, help):
        if type not in self.ALLOWED_TYPES:
            raise ValueError("Metric type %s not allowed, must be one of: %s" % (type, str(self.ALLOWED_TYPES)))
        
        self.name = name
        self.type = type
        self.help = help
    
    def header(self):
        """Return the header for this metric in prometheus plain text exposition format
        """
        s = "# HELP %s %s\n" % (self.name, self.help)
        s += "# TYPE %s %s\n" % (self.name, self.type)
        return s

class MetricFilter(object):
    def __init__(self):
        self._match = None
    
    def match(self, sensor_record):
        if self._match is None:
            raise RuntimeError("MetricFilter must either set _match attr or implement match()")
        return all([k in sensor_record and sensor_record[k] == self._match[k] for k in self._match.keys()])

    def process(self, sensor_record):
        raise RuntimeError("process method must be provided by sub-class")
    
    def filter(self, record):
        if not self.match(record):
            return []
        return self.process(record)


class Metric(object):
    def __init__(self, name, value, timestamp=None, labels=None):
        self.name = name
        self.value = value
        self.timestamp = timestamp
        self.labels = labels

    def to_string(self):
        s = self.name
        if self.labels is not None:
            s += '{' + ",".join(["%s=\"%s\"" % (k,v) for k,v in self.labels.items()]) + '}'
        s += " " + str(self.value)
        if self.timestamp is not None:
            self += " " + str(self.timestamp)
        s += "\n"
        return s

class MetricMaker(object):
    def __init__(self, metric_descriptions, metric_filters):
        self.descriptions = metric_descriptions
        self.filters = metric_filters
        # Memoize the names because we'll use them a lot
        self._metric_names = [d.name for d in self.descriptions]

    def to_metrics(self, records):
        """Convert a list of dicts to a list of metrics using the provided filters
        """
        metrics = []
        # Each filter may generate any number of metrics, or none
        for f in self.filters:
            for r in records:
                for m in f.filter(r):
                    if m.name not in self._metric_names:
                        raise ValueError("Tried to create metric %s, but no description was provided. Provide a MetricDescription to MetricMaker constructor.")
                    metrics.append(m)
        
        return metrics

    def to_string(self, records_or_metrics):
        """Convert a list of records (dicts), or Metric objects to exposition format"""
        s = ""
        if len(records_or_metrics) > 0 and isinstance(records_or_metrics[0], dict):
            metrics = self.to_metrics(records_or_metrics)
        else:
            metrics = records_or_metrics

        for d in self.descriptions:
            s += d.header()
            lines = filter(lambda m: m.name == d.name, metrics)
            for l in lines:
                s += l.to_string()
            s += "\n" # blank line for readability only
        
        return s
