import requests
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import xml.etree.ElementTree
import re
import time
import socket

start_time = time.time()
timeout = 10
socket.setdefaulttimeout(timeout)
app_list = []
eureka_url = 'http://213.183.195.222:8761/eureka/apps'
eureka_xml = requests.get(eureka_url)
eureka_list = xml.etree.ElementTree.fromstring(eureka_xml.text)
print("############################################", time.time() - start_time)
for eureka_app in eureka_list.iter('name'):
    app_name = eureka_app.text
    if app_name != 'MyOwn':
        app_list.append(app_name)
        eureka_app_url = eureka_url + '/' + app_name
        eureka_app_xml = requests.get(eureka_app_url)
        print("...........................................", time.time() - start_time)
        eureka_app_instance_list = xml.etree.ElementTree.fromstring(eureka_app_xml.text)
        for instance in eureka_app_instance_list.iter('instanceId'):
            if re.search(':',instance.text):
                eureka_app_instance_url = eureka_app_url + '/' + instance.text
                eureka_app_instance_xml = requests.get(eureka_app_instance_url)
                eureka_app_instance_text = xml.etree.ElementTree.fromstring(eureka_app_instance_xml.text)
                eureka_app_instance_statusurl = eureka_app_instance_text.find('statusPageUrl').text
                try:
                    #eureka_app_instance_statusurl_request = urlopen(eureka_app_instance_statusurl)
                    #eureka_app_instance_statusurl_status_code = eureka_app_instance_statusurl_request.getcode()
                    eureka_app_instance_statusurl_status_code = urlopen(eureka_app_instance_statusurl).getcode()
                except HTTPError as e:
                    eureka_app_instance_statusurl_status_code = e.code
                except URLError as e:
                    eureka_app_instance_statusurl_status_code = '001'
                print(app_name, instance.text, eureka_app_instance_statusurl, eureka_app_instance_statusurl_status_code)
print("My program took", time.time() - start_time, " seconds to run")
