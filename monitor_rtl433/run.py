from .metrics import MetricMaker
from .sensor_database import SensorDatabase
from .server import create_app
from .rtl433 import rtl433
import threading
import time
import os

def run(metric_descriptions=None, metric_filters=None):
    if metric_descriptions is None:
        metric_descriptions = []
    if metric_filters is None:
        metric_filters = []
    
    db = SensorDatabase()

    metric_maker = MetricMaker(metric_descriptions, metric_filters)

    receiver = rtl433()
    receiver.open()
    
    error_event = threading.Event()
    def rx_thread_entry():
        while True:
            try:
                message = receiver.get_message()
                if message is not None:
                    db.store(message)
            except:
                error_event.set()
                raise
        
    rx_thread = threading.Thread(target=rx_thread_entry, daemon=True)
    rx_thread.start()

    host = os.getenv('MONITOR_RTL433_HOST', None)
    port = os.getenv('MONITOR_RTL433_PORT', None)
    def http_thread_entry():
        try:
            app = create_app(db,  metric_maker)
            app.run(host=host, port=port)
        except:
            error_event.set()
            raise
    
    http_thread = threading.Thread(target=http_thread_entry, daemon=True)
    http_thread.start()

    while(not error_event.wait()):
        pass

    time.sleep(1)