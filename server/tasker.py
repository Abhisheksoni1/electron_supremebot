from django.core.exceptions import ObjectDoesNotExist
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import random
import os
import requests
import sys
import json
from supreme.models import SupremeTask, Setting


def get_token():
    return str(requests.get("http://cartchefs.supremenewyork.com:5000/token").text)


def select_by_text(id, text):
    out = """
        var sel = document.getElementById('%s');
        for(var i = 0, j = sel.options.length; i < j; ++i) {
            if(sel.options[i].innerHTML.toLowerCase() === '%s') {
                sel.selectedIndex = i;
                break;
                }
            }
        """ % (id.lower(), text.lower())
    return out


def init_task(headless=True, proxy=None, ):
    home = "https://www.supremenewyork.com/shop/all/"
    chrome_options = Options()
    if proxy:
        chrome_options.add_argument("--proxy-server='%s'" % proxy)
    # chrome_options.add_argument("--user-data-dir=C:\\Users\gaura\\AppData\\Local\\Google\\Chrome\\User Data")
    if headless:
        prefs = {"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
    else:
        chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(executable_path='server/chromedriver', chrome_options=chrome_options)
    driver.execute_script("window.location='%s';" % (home))

    return driver


def start_task(driver, category, incolor, insize, del_details, payment_details, supremetask, checkout_delay=0.5):
    loadscript = """
        var articles=[];
        console.log(window.location);
        articles = document.getElementsByClassName('inner-article');
        var avail_articles= []; 
        for (var i = 0, len = articles.length; i < len; i++) {
                if ((articles[i].getElementsByClassName('sold_out_tag').length) ==0)
                avail_articles.push(articles[i].getElementsByTagName('a')[0].getAttribute('href'));
                }
        return avail_articles;
        """

    script = """
        document.getElementById('credit_card_last_name').setAttribute('value', '%s');
        document.getElementById('credit_card_first_name').setAttribute('value', '%s');
        document.getElementById('order_email').setAttribute('value', '%s'); 
        document.getElementById('order_tel').setAttribute('value', '%s');
        document.getElementById('order_billing_city').setAttribute('value', '%s');
        document.getElementById('order_billing_address').setAttribute('value', '%s');
        document.getElementById('order_billing_zip').setAttribute('value', '%s');
        document.getElementById('cnb').setAttribute('value', '%s');
        document.getElementById('credit_card_month').value= '%s';
        document.getElementById('credit_card_year').value= '%s';
        document.getElementById('vval').setAttribute('value', '%s');
        """ % (
        del_details['lastname'],
        del_details['firstname'],
        del_details['email'],
        del_details['phone'],
        del_details['city'],
        del_details['add'],
        del_details['zip'],
        payment_details['cardno'],
        payment_details['expmonth'],
        payment_details['expyear'],
        payment_details['cvv']
    )
    script = script + select_by_text('order_billing_state', del_details['state'])
    script = script + select_by_text('credit_card_type', payment_details['method'])
    driver.delete_all_cookies()
    driver.get("https://www.supremenewyork.com/shop/all/" + category)
    # print(loadscript)
    links = driver.execute_script(loadscript)
    # print(links)
    supremetask.progress = "Searching"
    supremetask.save()
    found = False
    for link in links:
        print(supremetask.progress)
        driver.execute_script("window.location='%s';" % (link))
        details = driver.find_element_by_id("details")
        # name=details.find_element_by_tag_name('h1').text
        color = details.find_element_by_class_name('style').text
        if color.lower() == incolor.lower():
            if driver.find_elements_by_id('size'):
                driver.execute_script(select_by_text('size', insize))
            supremetask.progress = "Product Found"
            supremetask.save()
            found = True
            print(supremetask.progress)
            driver.execute_script("document.getElementsByName('commit')[0].click();")
            supremetask.progress = "Added to cart"
            supremetask.save()
            print(supremetask.progress)
            time.sleep(checkout_delay)
            driver.execute_script("window.location='https://www.supremenewyork.com/checkout';")
            time.sleep(0.1)
            driver.execute_script(script)
            supremetask.progress = "Checking out"
            supremetask.save()
            print(supremetask.progress)
            time.sleep(0.1)
            token = get_token()
            cap = """
                document.getElementById("g-recaptcha-response").innerHTML = '%s';
                checkoutAfterCaptcha();
                """ % (token)
            driver.execute_script(cap)
            time.sleep(0.5)
            driver.execute_script(
                "document.getElementById('order_terms').click();document.getElementsByClassName('checkout')[0].click();")
            # time.sleep(1)
            errors = driver.find_elements_by_class_name('errors')
            if errors:
                supremetask.progress = "Card Declined"
                supremetask.save()
                return False
            else:
                supremetask.progress = 'Checkout successful'
                supremetask.save()
                return False
                # driver.close()

            break
    if not found:
        supremetask.progress = "out of stock"
        supremetask.save()
        return True


#
# driver,loadscript,script = init_task(query,del_details,payment_details)
# start_task(driver,query['color'],query['size'],loadscript,script)


def manage_task(task_id):
    # task id pass as argument to manage each task asynchronously just by viewing it changes in model in real time
    supremetask = SupremeTask.objects.get(id=task_id)
    supremetask.progress = "Initialise!"
    supremetask.save()
    print("Task with id: {} ".format(task_id) + supremetask.progress)
    if supremetask.progress == 'Initialise!':
        # time to start task
        retry = False
        stop = False
        setting = Setting.objects.all()[0]
        driver = init_task(headless=True if setting.mode == "headless" else False)
        if supremetask.timer:
            time.sleep(supremetask.timer * 60)
            query = {"category": supremetask.category, "size": supremetask.size.capitalize(),
                     "color": supremetask.color.capitalize()}
            del_details = {"firstname": supremetask.profile.name.split(" ")[0],
                           "lastname": supremetask.profile.name.split(" ")[1],
                           "email": supremetask.profile.email, "phone": str(supremetask.profile.phone),
                           "state": supremetask.profile.country, "city": supremetask.profile.city,
                           "add": supremetask.profile.address1 + " " +
                                  supremetask.profile.address2, "zip": str(supremetask.profile.zip_code)}
            payment_details = {"method": supremetask.profile.payment_option,
                               "cardno": str(supremetask.profile.card_number),
                               "expmonth": str(supremetask.profile.expiry).zfill(2),
                               "expyear": str(supremetask.profile.year), "cvv": str(supremetask.profile.cvv)}

            start_task(driver, query['category'], query['color'], query['size'], del_details, payment_details,
                       supremetask,
                       setting.checkout_delay)
        else:
            while True:
                try:
                    supremetask = SupremeTask.objects.get(id=task_id)
                    if supremetask.progress == "Stopped":
                        stop = True
                    query = {"category": supremetask.category, "size": supremetask.size.capitalize(),
                             "color": supremetask.color.capitalize()}
                    del_details = {"firstname": supremetask.profile.name.split(" ")[0],
                                   "lastname": supremetask.profile.name.split(" ")[1],
                                   "email": supremetask.profile.email, "phone": str(supremetask.profile.phone),
                                   "state": supremetask.profile.country, "city": supremetask.profile.city,
                                   "add": supremetask.profile.address1 + " " +
                                          supremetask.profile.address2, "zip": str(supremetask.profile.zip_code)}
                    payment_details = {"method": supremetask.profile.payment_option,
                                       "cardno": str(supremetask.profile.card_number),
                                       "expmonth": str(supremetask.profile.expiry).zfill(2),
                                       "expyear": str(supremetask.profile.year),
                                       "cvv": str(supremetask.profile.cvv)}
                    if not retry:
                        if supremetask.progress == "Started":
                            print("in task")

                            retry = start_task(driver, query['category'], query['color'], query['size'], del_details,
                                               payment_details,
                                               supremetask, setting.checkout_delay)
                            # break
                    else:
                        if setting.moniter:
                            time.sleep(setting.moniter)
                            retry = start_task(driver, query['category'], query['color'], query['size'], del_details,
                                               payment_details, supremetask, setting.checkout_delay)

                except ObjectDoesNotExist:
                    print("hello")
                    driver.close()
                    sys.exit()
    time.sleep(10)
