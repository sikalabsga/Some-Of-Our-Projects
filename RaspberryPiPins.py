import RPi.GPIO as GPIO
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests

#Setup requests retries
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

class PiPins(object):
    def __init__(self, pin, pin_name):
        self._pin = pin
        self._pin_name = pin_name
        if ' ' in self._pin_name:            
            self.Id_left, self.Id_right = self._pin_name.split(' ')            
            self.Id = (self.Id_left + '_' + self.Id_right)
            
        else:
            self.Id = self._pin_name
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._pin, GPIO.OUT)
        GPIO.setwarnings(False)
        
    def value(self):
        """
        Read the current state of a channel set up as an output using the input() function
        Don't try to setup that channel as an input
        """
        return GPIO.input(self._pin)
    
    def on(self):
        GPIO.output(self._pin, GPIO.HIGH)
        payload = {'Id': self.Id, 'Status':'on'}
        post_status = session.post('https://sikalabsga.000webhostapp.com/APIControl/control_update.php', data = payload).json()
        
        
    def off(self):
        GPIO.output(self._pin, GPIO.LOW)
        payload = {'Id': self.Id, 'Status':'off'}
        post_status = session.post('https://sikalabsga.000webhostapp.com/APIControl/control_update.php', data = payload).json()
        

