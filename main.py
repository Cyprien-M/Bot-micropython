import network
import secret
from time import sleep
import urequests
import rp2
import sys
from machine import Pin

def connect():
    #connection au wifi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    wlan.connect(secret.ssid, secret.password)#you need to put your ssid and password
    
    while wlan.isconnected() == False:
        
        if rp2.bootsel_button() == 1: #if you want to stop the system
            sys.exit()
            
        print('Waiting for connection...')
        sleep(1)
        
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    
    return ip

API_URL = "https://api.telegram.org/bot" + secret.telegramToken

def init_bot():
    get_url = API_URL
    get_url += "/getme"
    r = urequests.get(get_url)
    return r.json()

text_id = secret.messageId
send =  API_URL + "/sendMessage?chat_id="+text_id+"&text=Quelqu'un est à la porte !!!"

button = Pin(18, Pin.IN, Pin.PULL_DOWN)

def send_alert(pin):
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("No internet connection. Retrying...")#checking if connected to wifi
        connect()
        
    #Send a message when button is pressed
    print("Button Pressed! Sending alert...")
    urequests.get(send)

# Attach an interrupt to the button (rising edge, meaning when pressed)
button.irq(trigger=Pin.IRQ_RISING, handler=send_alert)

connect()

# **Test Mode: Simulate Button Press**
TEST_MODE = False  # Set to False to disable simulation

if TEST_MODE:
    print("Test mode enabled: Simulating button press every 5 seconds...")
    while True:
        sleep(5)
        print("Simulating button press...")
        send_alert(None)  # Simulate a button press
else:
    print("Waiting for button press...")
    while True:
        sleep(1)  # Keep script running for interrupt to work
