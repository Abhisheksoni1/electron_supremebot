from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import random
import requests
import os
import json
from tqdm import tqdm

def randdelay(a, b):
    time.sleep(random.uniform(a, b))


def randdelay(a, b):
    time.sleep(random.uniform(a, b))


def get_token():
    return str(requests.get("http://cartchefs.supremenewyork.com:5000/token").text)


def search(driver,query,del_details,payment_details):
    links=driver.execute_script(loadscript)  

    for link in links:
        driver.execute_script("window.location='%s';"%(link))
        details=driver.find_element_by_id("details")
        # name=details.find_element_by_tag_name('h1').text
        color=details.find_element_by_class_name('style').text

        if color==query['color']:
            driver.execute_script("document.getElementById('size').value=%d;"%(query['size']) +\
                                  "document.getElementsByName('commit')[0].click();")
            time.sleep(0.5)
            driver.execute_script("window.location='https://www.supremenewyork.com/checkout';")
            time.sleep(0.1)
            driver.execute_script(script)
            time.sleep(0.5)

            token = get_token()
            cap="""
                document.getElementById("g-recaptcha-response").innerHTML = '%s';
                
                checkoutAfterCaptcha();
                """%(token)
            #document.getElementById("recaptcha-token").setAttribute('value', '%s');
            driver.execute_script(cap)
            time.sleep(0.5)
            driver.execute_script("document.getElementById('order_terms').click();document.getElementsByClassName('checkout')[0].click();")
            # captcha harvester trick not working now thats why commented

            # driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML='{}';".format(get_token()))
            # time.sleep(0.5)
            # driver.execute_script("document.getElementById('order_terms').click();document.getElementsByClassName('checkout')[0].click();")
            break
        # driver.back()


home="https://www.supremenewyork.com/shop/all/"
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--user-data-dir=C:\\Users\gaura\\AppData\\Local\\Google\\Chrome\\User Data")
# prefs={"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
# chrome_options.add_experimental_option("prefs", prefs)
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(executable_path='chromedriver',chrome_options=chrome_options)
# input()
driver.execute_script("window.location='%s';"%(home))

query={"category":"accessories","size":50894,"color":"Black"}
del_details={"firstname":"gaurav","lastname":"singh","email":"gaurav@moonraft.com","phone":"9898989898","state":" 愛知県","city":"asdf","add":"ffhsyfgshfgsgfghsgdfhdf","zip":"676498"}
payment_details={"method":"jcb","cardno":"7787987897667031","expmonth":"01","expyear":"2021","cvv":"569"}

loadscript="""
        window.location='%s';
        var articles= document.getElementsByClassName('inner-article');
        var avail_articles= [];
        for (var i = 0, len = articles.length; i < len; i++) {
                if ((articles[i].getElementsByClassName('sold_out_tag').length) ==0)
                avail_articles.push(articles[i].getElementsByTagName('a')[0].getAttribute('href'));
                }
        return avail_articles;
        """ %(
            home+query['category']
        )
    


script= """
        document.getElementById('credit_card_last_name').setAttribute('value', '%s');
        document.getElementById('credit_card_first_name').setAttribute('value', '%s');
        document.getElementById('order_email').setAttribute('value', '%s'); 
        document.getElementById('order_tel').setAttribute('value', '%s');
        document.getElementById('order_billing_state').value='%s';
        document.getElementById('order_billing_city').setAttribute('value', '%s');
        document.getElementById('order_billing_address').setAttribute('value', '%s');
        document.getElementById('order_billing_zip').setAttribute('value', '%s');
        document.getElementById('credit_card_type').value='%s';
        document.getElementById('cnb').setAttribute('value', '%s');
        document.getElementById('credit_card_month').value= '%s';
        document.getElementById('credit_card_year').value= '%s';
        document.getElementById('vval').setAttribute('value', '%s');
        """ %(
            del_details['lastname'],
            del_details['firstname'],
            del_details['email'],
            del_details['phone'],
            del_details['state'],
            del_details['city'],
            del_details['add'],
            del_details['zip'],
            payment_details['method'],
            payment_details['cardno'],
            payment_details['expmonth'],
            payment_details['expyear'],
            payment_details['cvv']
        )
 

tic1=time.time()
search(driver,query,del_details,payment_details)
print("total time",time.time()-tic1)

time.sleep(100)
# driver.close()