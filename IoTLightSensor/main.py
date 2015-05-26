#!/usr/bin/env python

from flask import Flask, render_template
from flask_bootstrap import Bootstrap        
from MCP3008 import *
from twilio.rest import TwilioRestClient
from credentials import *

adc = MCP3008(0, 0)
app = Flask(__name__, static_folder='static', static_url_path='')
adcChannel = 0


sms = TwilioRestClient(account_sid, auth_token)



@app.route("/")
def index():
    return render_template('index.html',
        homePage = True,
        page_title = "Home Page",
        light = adc.read(adcChannel))
    
    
@app.route("/testSMS")
def testSMS():
    level = adc.read(adcChannel)
    try:
        msg = sms.messages.create(to=to_num, 
            from_ = twilio_num, 
            body = "Light Level: "+str(level))

        return render_template('index.html',
            homePage = True,
            page_title = "Home Page",
            light = level,
            successMsg = "Text Sent!")            
            
    except TwilioRestException:
        return render_template('index.html',
            homePage = True,
            page_title = "Home Page",
            light = level,
            errorMsg = "Error sending text!")        
        
    


if __name__ == "__main__":
    try:
        app.debug = True
        Bootstrap(app)
        app.run(host="0.0.0.0")        
        
    finally:
        adc.close()
        






