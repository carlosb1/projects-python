"""Docstring for MyClass."""

import datetime
import requests
from sqlalchemy import Column, Integer, String , create_engine
from celery import Celery
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

def timestamp_to_string(timestamp):
    """testing function."""
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

def set_up_msg(id_spot,local_timestamp, wind_speed, wind_unit,  wind_compass_direction, solid_rating, faded_rating, swell_primary_height, swell_primary_period, swell_primary_compass_direction
        , swell_secondary_height, swell_secondary_period, swell_secondary_compass_direction, swell_unit, condition_temperature, condition_unit):
    """Set up message email."""

    msg ="TIMESTAMP: "+timestamp_to_string(local_timestamp)+"<br/>"
    msg+="WIND: "+str(wind_speed)+" "+str(wind_unit)+"<br/>"+ "SWELL: primary(height,period,direction)="+str(swell_primary_height)+","+str(swell_primary_period)+" "+str(swell_unit)+","+str(swell_primary_compass_direction)+" second(height,period,direction)="+str(swell_secondary_height)+" "+str(swell_unit)+","+str(swell_secondary_period)+","+str(swell_secondary_compass_direction)+"<br/>"+"CONDITION: temperature="+str(condition_temperature)+" "+str(condition_unit)+"<br/>"
    
    #msg = "ID_SPOT: "+str(id_spot)+" SOLID RATE: "+str(solid_rating)+" FADED RATE: "+str(faded_rating)+"<br/>"+"TIMESTAMP: "+timestamp_to_string(local_timestamp)+"<br/>"+"WIND: "+str(wind_speed)+" "+str(wind_unit)+"<br/>"+str()+"<br/>"
    return msg   


# API Reader
class ApiReader(object):
    """Docstring for MyClass."""

    def __init__(self, key, id_spot,user,passwd,dest):
        """testing function."""
        self.id_spot = id_spot
        self.user = user
        self.passwd = passwd
        self.dest = dest
        self.key = key
        self.url = 'http://magicseaweed.com/api/'+str(self.key)+'/forecast/?spot_id='+str(self.id_spot)+'&units=eu&fields=timestamp,localTimestamp,fadedRating,solidRating,threeHourTimeText,wind.*,condition.temperature,charts.*'
     #   self.session = session

    def update(self):
        """testing function."""
        r = requests.get(self.url)
        json_values = r.json()
        msgs="<b>Barceloneta</b>\n"
        for value in json_values:
            #Parse times
            local_timestamp = value['localTimestamp']
            solid_rating = value['solidRating']
            faded_rating = value['fadedRating']
            chart_wind_url = value['charts']['wind']
            chart_period_url = value['charts']['period']
           # chart_sst =  value['charts']['sst'] #Honda
            wind_direction = value['wind']['direction']
            wind_compass_direction = value['wind']['compassDirection'] #Brujula
            wind_speed = value['wind']['speed']
            wind_unit = value['wind']['unit']
            wind_chill = value['wind']['chill'] #Frio
            swell_primary_height=value['swell']['primary']['height']
            swell_primary_period=value['swell']['primary']['period']
            swell_primary_compass_direction=value['swell']['primary']['compassDirection']
            swell_secondary_height=value['swell']['secondary']['height']
            swell_secondary_period=value['swell']['secondary']['period']
            swell_secondary_compass_direction=value['swell']['secondary']['compassDirection']
            swell_unit=value['swell']['unit']
            condition_temperature=value['condition']['temperature']
            condition_unit=value['condition']['unit']
            

            print 'time: '+timestamp_to_string(local_timestamp)+' solidRating='+str(solid_rating)+' fadedRating='+str(faded_rating)
            print 'chart_wind: '+str(chart_wind_url)
            print 'chart_period: '+str(chart_period_url)
            print 'wind_direction: '+str(wind_direction)+' wind_compass_direction: '+wind_compass_direction
            print 'wind_speed: '+str(wind_speed)+' '+str(wind_unit)
            print 'wind_chill: '+str(wind_chill)
            if solid_rating > 0 or faded_rating > 0 or swell_primary_height > 0.6 or swell_secondary_height > 0.6:
                msg = set_up_msg(self.id_spot,local_timestamp,wind_speed,wind_unit,wind_compass_direction,solid_rating,faded_rating, swell_primary_height, swell_primary_period, swell_primary_compass_direction, swell_secondary_height, swell_secondary_period, swell_secondary_compass_direction, swell_unit, condition_temperature, condition_unit)
                msgs += msg+'\n'
    
#           if not self.session.query(exists().where(InfoSpot.local_timestamp == local_timestamp).where(InfoSpot.id_spot == self.id_spot)).scalar():
 #               self.session.add(spot)
 #               self.session.commit()
        #TODO parametr. parameters
        send_email(self.user,self.dest,"Wave report",msgs,self.passwd)


def send_email(fromaddr, toaddr, subject, msg,passwd):
    """Send email via gmail."""
    import smtplib
    server = smtplib.SMTP_SSL('smtp.gmail.com:465')
    server.ehlo()
    server.login(fromaddr,passwd)
    headers = "\r\n".join(["From: " + fromaddr,
                        "To: " + toaddr,
                        "subject: "+ subject,
                        "mime-version: 1.0",                                
                        "content-type: text/html"])

    content = headers + "\r\n\r\n" + msg

    print content
    server.sendmail(fromaddr,toaddr,content)
    server.close()


print "Starting app!!"

#Read file configuration
#fname = 'secret_forecast'
#with open(fname) as f:
#    content = f.readlines()
import os
BROKER_URL=os.environ['REDIS_URL']
CELERY_RESULT_BACKEND=os.environ['REDIS_URL']
key=os.environ['KEY']
secret=os.environ['SECRET']
username=os.environ['USERNAME']
password=os.environ['PASSWORD']
dest=os.environ['DEST']
#TODO  get content correctly (via dict)
#key = content[0].split(':')[1].rstrip().lstrip().strip()
#secret = content[1].split(':')[1].rstrip().lstrip().strip()
#username = content[2].split(":")[1].rstrip().lstrip().strip()
#password = content[3].split(":")[1].rstrip().lstrip().strip()
#dest = content[4].split(":")[1].rstrip().lstrip().strip()



#SQL alchemy
#engine = create_engine('sqlite:///spots3.db')
#Base.metadata.create_all(engine)


#Base.metadata.bind = engine
#DBSession = sessionmaker(bind=engine)
#session = DBSession()



celery = Celery('forecast')
celery.config_from_object('celeryconfig')
celery.conf.update(BROKER_URL=BROKER_URL, CELERY_RESULT_BACKEND = CELERY_RESULT_BACKEND)

#Defined spots
#TODO add waves
idBarceloneta = 3535
reader = ApiReader(key,idBarceloneta,username,password,dest)


@celery.task
def search_spot():
    """testing function."""
    print 'Calling searching spot'
    reader.update()
