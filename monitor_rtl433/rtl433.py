import json
import subprocess

class rtl433(object):
    def __init__(self):
        self.process = None
    
    def open(self):
        self.process = subprocess.Popen(['rtl_433 -F json'], shell=True, stderr=None, stdout=subprocess.PIPE)

    def get_message(self, timeout=30):
        """Wait for a message from the radio

        timeout: time to wait in seconds

        Returns message as a dict, or None if no message is received before timeout is reached
        """
        try:
            outs = self.process.stdout.readline()
            
            if self.process.poll() is not None:
                raise RuntimeError("rtl_433 process terminated")
            return json.loads(outs)

        except subprocess.TimeoutExpired:
            return None