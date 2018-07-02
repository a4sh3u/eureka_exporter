import requests
import xml.etree.ElementTree
import re
import time

start_time = time.time()

app_list = []
eureka_url = 'http://213.183.195.222:8761/eureka/apps'
eureka_xml = requests.get(eureka_url)
eureka_list = xml.etree.ElementTree.fromstring(eureka_xml.text)
for eureka_app in eureka_list.iter('name'):
    app_name = eureka_app.text
    if app_name != 'MyOwn':
        app_list.append(app_name)
        eureka_app_url = eureka_url + '/' + app_name
        eureka_app_xml = requests.get(eureka_app_url)
        eureka_app_instance_list = xml.etree.ElementTree.fromstring(eureka_app_xml.text)
        for instance in eureka_app_instance_list.iter('instanceId'):
            if re.search(':',instance.text):
                eureka_app_instance_url = eureka_app_url + '/' + instance.text
                eureka_app_instance_xml = requests.get(eureka_app_instance_url)
                eureka_app_instance_text = xml.etree.ElementTree.fromstring(eureka_app_instance_xml.text)
                eureka_app_instance_statusurl = eureka_app_instance_text.find('statusPageUrl').text
                try:
                    eureka_app_instance_statusurl_status_code = requests.get(eureka_app_instance_statusurl, timeout=0.001).status_code
                except requests.exceptions.RequestException:
                    eureka_app_instance_statusurl_status_code = '001'
                print(app_name, instance.text, eureka_app_instance_statusurl, eureka_app_instance_statusurl_status_code)
print("My program took", time.time() - start_time, " seconds to run")
