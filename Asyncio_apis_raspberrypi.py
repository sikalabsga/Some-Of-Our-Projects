import schedule
from RaspberryPiPins import PiPins
import logging
#from datetime import datetime
import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import asyncio


#create path to files locations using
#__file__ as in the path location of this file
cwd = os.path.dirname(os.path.abspath(__file__))


logger = logging.getLogger('httpserver')
logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(message)s')

file_handler = logging.FileHandler(os.path.join(cwd, "errors.log"))
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

'''
file_handler2 = logging.FileHandler(os.path.join(cwd, "message.log"))
file_handler2.setLevel(logging.INFO)
file_handler2.setFormatter(formatter)
'''


logger.addHandler(file_handler)
#logger.addHandler(file_handler2)



Guestroom_Light, Kitchen_Light, Balcony_Light, Heating, Cooling = [PiPins(i,n) for i, n in ((29,'Guestroom Light'), (31,'Kitchen Light'),(33,'Balcony Light'),(35,'Heating'),(37,'Cooling'))]

#Setup requests retries
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


def job_print():
    print('Dummy job')



async def Control_Loop():
    while True:
        await asyncio.sleep(35)
        print('Receiving control data')
        try:
            read_all_status = session.get('https://sikalabsga.000webhostapp.com/APIControl/control_read.php?').json()
            if read_all_status['control']:
                for control_item in read_all_status['control']:
                    print(control_item)
                    control_job = getattr(globals()[(control_item['Id'])], control_item['Status'])
                    control_job()
        except Exception as e:
            logger.exception("Control loop error %s \r\n" % e)
        
            
                    




async def pending_loop():
    schedule.every(10).minutes.do(job_print)               
    while True:
        try:
            schedule.run_pending()
        except Exception:
            logger.exception('Occured with scheduling: ')

        await asyncio.sleep(1)#Necessary for queuing coros
        
        
    


async def Schedule_Loop():
    try:
        all_schedules = session.get('https://sikalabsga.000webhostapp.com/APISchedules/readall_schedule.php?').json()
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
    except Exception as e:
        logger.exception("From initial reading from database %s \r\n" % e)       

        

    
    while True:
        print('requesting.......')
        try:
            request_schedule = session.get('https://sikalabsga.000webhostapp.com/APISchedules/request_schedule.php?').json()
            print(request_schedule)
            if request_schedule['success']:
                if 'request' in request_schedule:            
                    for row in request_schedule['request']:
                        method, Id = (row['Method'], row['Id'])
                        print(Id)
                        print(method)
                        payload = {'Id': int(Id)}
                        print(payload)
                        if method == 'POST':
                            post_request = session.post('https://sikalabsga.000webhostapp.com/APISchedules/read_schedule.php', data = payload).json()
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
                            put_request = session.post('https://sikalabsga.000webhostapp.com/APISchedules/read_schedule.php', data = payload).json()
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
                                all_delete_schedules = session.post('https://sikalabsga.000webhostapp.com/APISchedules/deleteall_schedule.php', data = payload).json()
                                print(all_delete_schedules)
                            else:
                                delete_request = session.post('https://sikalabsga.000webhostapp.com/APISchedules/read_schedule.php', data = payload).json()
                                if 'Schedule' in delete_request:
                                    delete_schedule = delete_request['Schedule']
                                    for delete_schedule_item in delete_schedule:
                                        print(delete_schedule_item)
                                        job_delete = getattr(globals()[(delete_schedule_item['action'])], delete_schedule_item['turn'])
                                        schedule.cancel_job(job_delete)
                                        deleted_sched = requests.post('https://sikalabsga.000webhostapp.com/APISchedules/read_delete_schedule.php', data = payload).json()
                                        print(deleted_sched)


        except Exception as er:
            logger.exception("In schedule loop %s \r\n" % er)

        await asyncio.sleep(120)#Necessary for queuing coros
            

              
            



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    cors = asyncio.wait([Schedule_Loop(),Control_Loop(),pending_loop()])
    loop.run_until_complete(cors)
    
    
