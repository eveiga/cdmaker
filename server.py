# -*- coding: utf-8 -*-
import subprocess

def start_supplier(host, port):
    pass

def start_frontend(host, port):
    subprocess.Popen(
        ['python', 'frontend/manage.py', 'runserver', '%s:%s'%(host, port,)],
    )

def start_manufacturer(host, port):
    subprocess.Popen(['python', 'manufacturer/soap_services.py', host, port],)

def start_backoffice(host, port):
    subprocess.Popen(['python', 'backoffice/soap_services.py', host, port],)

if __name__=='__main__':
    try:
        start_frontend("127.0.0.1", "8000")
        start_manufacturer("localhost","7889")
        start_manufacturer("localhost","7890")

        start_backoffice("localhost","7891")
    except Exception, e:
           print "Error: unable to start process %s"%(str(e),)

    while True:
        pass
