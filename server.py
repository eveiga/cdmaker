# -*- coding: utf-8 -*-
import subprocess

def start_manufacturer(host, port):
    subprocess.Popen(['python', 'manufacturer/soap_views.py', host, port],)

def start_backoffice(host, port):
    subprocess.Popen(['python', 'backoffice/soap_views.py', host, port],)

def start_carrier(host, port):
    subprocess.Popen(['python', 'carrier/soap_views.py', host, port],)

if __name__=='__main__':
    try:
        start_carrier("localhost","7885")
        start_carrier("localhost","7886")
        start_carrier("localhost","7887")
        start_manufacturer("localhost","7888")
        start_manufacturer("localhost","7889")
        start_manufacturer("localhost","7890")
        start_backoffice("localhost","7891")
    except Exception, e:
           print "Error: unable to start process %s"%(str(e),)

    # Start frontend and wait for calls
    process = subprocess.Popen(['python', 'frontend/server.py'])
    process.wait()
