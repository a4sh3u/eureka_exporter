import requests, re, time, xml.etree.ElementTree
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from multiprocessing import Pool
from flask import Flask, render_template

eureka_url = 'http://213.183.195.222:8761/eureka/apps'


def millis():
    return int(round(time.time() * 1000))


def http_get(url):
    try:
        result = {"url": url, "status": urlopen(url).getcode()}
    except HTTPError as e:
        result = {"url": url, "status": e.code}
    except URLError as e:
        result = {"url": url, "status": 1001}
    return result


def get_result(url):
    instance_list = []
    instance_table = {}
    results_table = []
    start_time = millis()
    pool = Pool(processes=5)
    eureka_xml = requests.get(url)
    eureka_list = xml.etree.ElementTree.fromstring(eureka_xml.text)
    z = 1
    for eureka_app in eureka_list.iter('name'):
        app_name = eureka_app.text
        if app_name != 'MyOwn':
            eureka_app_url = url + '/' + app_name
            eureka_app_xml = requests.get(eureka_app_url)
            eureka_app_instance_list = xml.etree.ElementTree.fromstring(eureka_app_xml.text)
            for instance in eureka_app_instance_list.iter('instanceId'):
                if re.search(':',instance.text):
                    eureka_app_instance_url = eureka_app_url + '/' + instance.text
                    eureka_app_instance_xml = requests.get(eureka_app_instance_url)
                    eureka_app_instance_text = xml.etree.ElementTree.fromstring(eureka_app_instance_xml.text)
                    eureka_app_instance_statusurl = eureka_app_instance_text.find('statusPageUrl').text
                    instance_list.append(eureka_app_instance_statusurl)
                    instance_table[z] = {"app_name": app_name, "instance_id": instance.text, "status_page_url": eureka_app_instance_statusurl}
                    z = z + 1
    results = pool.map(http_get, instance_list)
    for i in results:
        for j, k in instance_table.items():
            if i['url'] == k['status_page_url']:
                app_name = str(k['app_name'])
                instance_id = str(k['instance_id'])
                status_page_url = str(k['status_page_url'])
                http_status = str(i['status'])
                results_table.append("eureka_collector_http_status{app_name=\"" + app_name + "\",instance_id=\"" + instance_id + "\",status_page_url=\"" + status_page_url + "\"} " + http_status)
    results_table.append("eureka_collector_scrape_time " + str(millis() - start_time))
    results_table.append("eureka_collector_alive_status " + str(requests.get(url).status_code))
    print("\nTotal time taken " + str(millis() - start_time) + " ms\n")
    return results_table


app = Flask(__name__)


@app.route("/metrics")
def home():
    return render_template("exporter", data=get_result(eureka_url))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
