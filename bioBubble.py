import time
import sys
import os
import grovepi
import math
import json
from grove.factory import Factory
from grovepi import *
import paho.mqtt.client as mqtt
from grove_rgb_lcd import *
                                                                                                     
lcd = None #define lcd screen variable


sensor = 4  # The temp/hum goes on digital port 4.
blue = 0    # The blue colored sensor.

light_sensor = 0 # Light sensor goes on A0

button_pin = 5 #the button goes on D5

buzzer_pin = 6 #the button goes on D6

water_counter = 0 #define variables for tracking water time
last_watered_time = None
reminder_threshold = 86400 #24 hours in seconds


# threshold for minimum light needed for plant
threshold = 50

#establish connection to thingsboard
thingsboard_host = 'thingsboard.cs.cf.ac.uk'
access_token = 'randomAccess'
pw = 'group062024'


#thingsboard functions
def on_publish(client,userdata,result):
    print('Success')
    
def on_connect(client,userdata, rc, *extra_params):
    print("Connected with result code: "+str(rc))

#set up LCD screen
def setScreen():
    global lcd
    
    lcd = Factory.getLcd("JHD1802")
    
    #output welcome message to the user
    lcd.setCursor(0,0)
    lcd.write('Hello BioBubble')
    time.sleep(4)
    
    
#set u buzzer and button    
def setBuzzerAndButton():
    grovepi.pinMode(button_pin, "INPUT")
    grovepi.pinMode(buzzer_pin, "OUTPUT")

#fetches data from the sensors
def getData():
    
        #temp and humidity data
        [temp,humidity] = grovepi.dht(sensor,blue)
            
        #get light sensor data
        light_sensor_value = grovepi.analogRead(light_sensor)

        
        if light_sensor_value < threshold:
            #warning message to user that light is too low
            light = 'Too dark!'
                
        else:
            #happy plant message
            light = 'Just right'
            
        #return collected data
        data = [temp, humidity, light]
            
        return data
    

#when button is pressed reset count down for watering schedule
def buttonPressCallback():
    global water_counter, last_watered_time
    water_counter +=1
    last_watered_time = time.time()
    lcd.clear()
    lcd.write("Plant has been watered!")
    
#calculate if watering is overdue    
def checkNeedToWater():
    if last_watered_time is None:
        return True # assume never been watered until button is pressed
    
    elapsed_time = time.time()-last_watered_time
    if elapsed_time > reminder_threshold:
        return True
    else:
        return False
    

def outputDataToScreen(temp, humidity, light):
    global lcd
    
    if math.isnan(temp) == False and math.isnan(humidity) == False:
        lcd.clear()
        lcd.write("Temperature: ")
        lcd.setCursor(1,0)
        lcd.write(format(temp)+ "C")
        time.sleep(3)
        
        lcd.clear()
        lcd.write("Humidity: ")
        lcd.setCursor(1,0)
        lcd.write(format(humidity))
        time.sleep(3)
        
        lcd.clear()
        lcd.write("Light levels: ")
        lcd.setCursor(1,0)
        lcd.write(format(light))
        time.sleep(3)
     
        
def outputWarningToScreen():
    lcd.clear()
    lcd.write("Plant needs")
    lcd.setCursor(1,0)
    lcd.write("watering!")
    time.sleep(4)
    
    
def soundBuzzer():
    grovepi.digitalWrite(buzzer_pin, 1)
    time.sleep(1)
    grovepi.digitalWrite(buzzer_pin, 0)
             
def main():
    setScreen()
    setBuzzerAndButton()
    
    #connect to thingsboard
    client = mqtt.Client()
    client.username_pw_set(access_token, pw)
    client.connect(thingsboard_host, 1883, 60)
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    while True:
        t = 0
        try:
            
            while t < 10:#t is the time between each 'please water plant' check
                
                #check button press
                button_state = digitalRead(button_pin)
                
                if button_state ==1:
                    buttonPressCallback()
                    
                
                data = []
                data = getData()
                temp = data[0]
                humidity = data[1]
                light = data[2]
 
                outputDataToScreen(temp, humidity, light)
                
                
                light_data = ({"light":light})

                
                temp_data = ({"temperature":temp})
                
                hum_data = ({"humidity":humidity})
                
                
                client.publish('v1/devices/me/telemetry', json.dumps(light_data),1)
                
                client.publish('v1/devices/me/telemetry', json.dumps(hum_data),1)
                
                client.publish('v1/devices/me/telemetry', json.dumps(temp_data),1)
                
            
                time.sleep(1)
                
                t +=10 #currently loop is 10 sec each
                
                
            if checkNeedToWater():
                outputWarningToScreen()
                soundBuzzer()
                
            

        except KeyboardInterrupt:
            print ("Terminated.")
            os._exit(0)
    
if __name__ == '__main__':
    main()
