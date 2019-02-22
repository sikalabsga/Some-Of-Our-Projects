
import schedule
import time
from RaspberryPiPins import PiPins
import logging
from datetime import datetime
import os
import requests
from threading import Thread



logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(message)s')

file_handler = logging.FileHandler('errors.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)


file_handler2 = logging.FileHandler('message.log')
file_handler2.setLevel(logging.INFO)
file_handler2.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(file_handler2)

cwd = os.path.dirname(os.path.abspath(__file__))


Guestroom_Light, Kitchen_Light, Balcony_Light, Heating, Cooling = [PiPins(i,n) for i, n in ((29,'Guestroom Light'), (31,'Kitchen Light'),(33,'Balcony Light'),(35,'Heating'),(37,'Cooling'))]


def Control_Loop():
    while True:
        time.sleep(30)
        print('Receiving control data')
        read_all_status = requests.get('https://sikalabsga.000webhostapp.com/APIControl/control_read.php?').json()
        for control_item in read_all_status['control']:
            print(control_item)
            control = getattr(globals()[(control_item['Id'])], control_item['Status'])
            print(control)
            control()
    
                    




def pending_loop():
               
    while True:
        time.sleep(1) #Necessary for queuing coros
        try:
            schedule.run_pending()
        except Exception:
            logger.exception('Occured with scheduling: ')
        
    


def Schedule_Loop():
    
    all_schedules = requests.get('https://sikalabsga.000webhostapp.com/APISchedules/readall_schedule.php?').json()
    if all_schedules['success']:
        for item in all_schedules['Schedule']:
            print(item)
            job_db = getattr(globals()[(item['action'])], item['turn'])            
            if item['every'] == 'day':
                schedule.every().day.at(item['time']).do(job_db)
            elif item['every'] == 'sunday':
                schedule.every().sunday.at(item['time']).do(job_db)
            elif item['every'] == 'monday':
                schedule.every().monday.at(item['time']).do(job_db)
            elif item['every'] == 'tuesday':
                schedule.every().tuesday.at(item['time']).do(job_db)
            elif item['every'] == 'wednesday':
                schedule.every().wednesday.at(item['time']).do(job_db)
            elif item['every'] == 'thursday':
                schedule.every().thursday.at(item['time']).do(job_db)
            elif item['every'] == 'friday':
                schedule.every().friday.at(item['time']).do(job_db)
            elif item['every'] == 'saturday':
                schedule.every().saturday.at(item['time']).do(job_db)
            
    while True:
        time.sleep(90)
        print('requesting.......')
        req_sched = requests.get('https://sikalabsga.000webhostapp.com/APISchedules/request_schedule.php?').json()
        print(req_sched)
        if 'request' in req_sched:            
            for row in req_sched['request']:
                method, Id = (row['Method'], row['Id'])
                print(Id)
                print(method)
                payload = {'Id': int(Id)}
                print(payload)
                if method == 'POST':
                    post_request = requests.post('https://sikalabsga.000webhostapp.com/APISchedules/read_schedule.php', data = payload).json()
                    print(post_request)
                    if 'Schedule' in post_request:
                        new_schedule = post_request['Schedule']
                        for new_schedule_item in new_schedule:
                            job = getattr(globals()[(new_schedule_item['action'])], new_schedule_item['turn'])
                            if new_schedule_item['every'] == 'day':
                                schedule.every().day.at(new_schedule_item['time']).do(job)
                            elif new_schedule_item['every'] == 'sunday':
                                schedule.every().sunday.at(new_schedule_item['time']).do(job)
                            elif new_schedule_item['every'] == 'monday':
                                schedule.every().monday.at(new_schedule_item['time']).do(job)
                            elif new_schedule_item['every'] == 'tuesday':
                                schedule.every().tuesday.at(new_schedule_item['time']).do(job)
                            elif new_schedule_item['every'] == 'wednesday':
                                schedule.every().wednesday.at(new_schedule_item['time']).do(job)
                            elif new_schedule_item['every'] == 'thursday':
                                schedule.every().thursday.at(new_schedule_item['time']).do(job)
                            elif new_schedule_item['every'] == 'friday':
                                schedule.every().friday.at(new_schedule_item['time']).do(job)
                            elif new_schedule_item['every'] == 'saturday':
                                schedule.every().saturday.at(new_schedule_item['time']).do(job) 
                            

                elif method == 'PUT':
                    put_request = requests.post('https://sikalabsga.000webhostapp.com/APISchedules/read_schedule.php', data = payload).json()
                    if 'Schedule' in put_request:                        
                        update_schedule = put_request['Schedule']
                        for update_schedule_item in update_schedule:
                            print(update_schedule_item)
                            job_delete_update = getattr(globals()[(update_schedule_item['action'])], update_schedule_item['turn'])
                            schedule.cancel_job(job_delete_update)
                            
                            '''
                                map received data into object functions. The inner method maps to the on or off function while
                                the outer to the outer methods like Cooling, Heating, Balcony_Light. End result e.g Cooling.on,
                                Balcony_Light.off etc
                            '''
                            job_update = getattr(globals()[(update_schedule_item['action'])], update_schedule_item['turn'])
                            if update_schedule_item['every'] == 'day':
                                schedule.every().day.at(update_schedule_item['time']).do(job_update)
                            elif update_schedule_item['every'] == 'sunday':
                                schedule.every().sunday.at(update_schedule_item['time']).do(job_update)
                            elif update_schedule_item['every'] == 'monday':
                                schedule.every().monday.at(update_schedule_item['time']).do(job_update)
                            elif update_schedule_item['every'] == 'tuesday':
                                schedule.every().tuesday.at(update_schedule_item['time']).do(job_update)
                            elif update_schedule_item['every'] == 'wednesday':
                                schedule.every().wednesday.at(update_schedule_item['time']).do(job_update)
                            elif update_schedule_item['every'] == 'thursday':
                                schedule.every().thursday.at(update_schedule_item['time']).do(job_update)
                            elif update_schedule_item['every'] == 'friday':
                                schedule.every().friday.at(update_schedule_item['time']).do(job_update)
                            elif update_schedule_item['every'] == 'saturday':
                                schedule.every().saturday.at(update_schedule_item['time']).do(job_update)
                            
     
                        
                elif method == 'DELETE':
                    if Id == 0:
                        schedule.clear()
                        all_delete_schedules = requests.post('https://sikalabsga.000webhostapp.com/APISchedules/deleteall_schedule.php', data = payload).json()
                        print(all_delete_schedules)
                    else:
                        delete_request = requests.post('https://sikalabsga.000webhostapp.com/APISchedules/read_schedule.php', data = payload).json()
                        if 'Schedule' in delete_request:
                            delete_schedule = delete_request['Schedule']
                            for delete_schedule_item in delete_schedule:
                                print(delete_schedule_item)
                                job_delete = getattr(globals()[(delete_schedule_item['action'])], delete_schedule_item['turn'])
                                schedule.cancel_job(job_delete)
                                deleted_sched = requests.post('https://sikalabsga.000webhostapp.com/APISchedules/read_delete_schedule.php', data = payload).json()
                                print(deleted_sched) 
                        

              
            





    

if __name__ == '__main__':
    t = Thread(target= Control_Loop,)
    t2 = Thread(target= Schedule_Loop,)
    t3 = Thread(target= pending_loop,)
    t.daemon = True
    t2.daemon = True
    t3.daemon = True
    t.start()
    t2.start()
    t3.start()
