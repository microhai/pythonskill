import json
import time
import uuid
import random
import os
from queue import Queue, LifoQueue, PriorityQueue
from selenium import webdriver
# from seleniumwire import webdriver 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import psutil

cookie = ''
header = {
    "Cookie": cookie,
    "Lang":"enus",
    "Connection":"keep-alive",
    "Accept": "*.*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
caps = DesiredCapabilities.CHROME
q = Queue(maxsize=0)


def get_body(log, driver):
        #获得log里面的requestid，通过id来获得response的内容
        requestId = json.loads(log.get("message")).get("message").get("params").get("requestId")
        # 
        try:
            # requestpostdata = driver.execute_cdp_cmd('Network.getRequestPostData', {'requestId': requestId})
            # pd = requestpostdata["postData"]
            # print(pd)
            response_dict = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
            #注意，这里获得的body是字符串形式，需要序列化为json对象/
            body = response_dict["body"]
            print(body)
            if body.find("searchCollections") != -1:
                return True,body
                # filename = str(time.time()) + '.json'
                # with open(filename, 'w') as f:
                #     f.write(body)
        except:
            print('=--==')        
        #Jres = json.loads(body)
        #return Jres
        return False,None

def GenerateNewDriver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')   #无头模式
    # options.add_argument('--no-sandbox') #非沙盒
    # options.add_argument('--disable-gpu') #禁用gpu，一般生产环境会使用，因为服务器大多没有gpu
    prefs = {"profile.managed_default_content_settings.images": 2} #不加载图片
    options.add_experimental_option("prefs", prefs)
    #重点来了
    options.add_experimental_option('perfLoggingPrefs', {'enableNetwork': True})
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('ignore-certificate-errors')#忽略ssl证书认证错误
    datadir = "D:\\Tmp\\ch" + str(uuid.uuid1())
    chrage = "--user-data-dir=" + datadir
    options.add_argument(chrage)
    #重点又来了
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}   
    driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe", options=options, desired_capabilities=caps)
    # options = {
    #     'verify_ssl': True  # Verify SSL certificates but beware of errors with self-signed certificates
    # }
    # driver = webdriver.Chrome(seleniumwire_options=options)
    driver.maximize_window()
    #driver.implicitly_wait(5)
    # driver = webdriver.Chrome(desired_capabilities=caps)

    #屏蔽webdrive检测
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                                            Object.defineProperty(navigator, 'webdriver', {
                                                get: () => undefined
                                            })
                                            """
    })


    try:
        driver.get("https://www.baidu.com")
    except:
        sleep(3)
    sleep(5)

    lpids = []
    for process in psutil.process_iter():
        if process.name() == 'chrome.exe' and  chrage in process.cmdline():
           print(process.pid)
           lpids.append(process.pid)
           #os.system('taskkill /f /pid %s' % str(process.pid))

    return driver,lpids, datadir

def CloseChrome(pids, datadir):
    print("CloseChrome")
    try:
        for pid in pids:
            os.system('taskkill /f /pid %s' % str(pid))
        #删除目录
        print("delete dir:" + datadir)
        #shutil.rmtree(datadir, onerror=readonly_handler)
    except Exception as e:
        print("CloseChrome error")
        print(e)

if __name__ == '__main__':
    
    driver, pids, datadir = GenerateNewDriver()

    driver.get("https://www.baidu.com/")
    print(driver.page_source)

    while True:
        if q.qsize() == 0:
            break
        if createNewDriver:
            createNewDriver = False
            driver, pids, datadir = GenerateNewDriver()
            driver.get("https://www.baidu.com/")
            print(driver.page_source)
        
        url = 'https://www.baidu.com'
        driver.get(url)
        time.sleep(random.randrange(1, 3))
        src = driver.page_source
        cks = driver.get_cookies()
        cookie_dict = []
        for cookie in cks:
            cookie_dict.append([cookie['name'], cookie['value']])

        ##  seleniumwire
        # for request in driver.requests:
        #     if request.response:
        #         print(
        #             request.url,
        #             request.response.status_code,
        #             request.response.headers['Content-Type'],
        #             request.response.body
        #         )

        ## log get body
        logs = driver.get_log("performance")
        print(len(logs))
        #driver.execute_script('console.clear()')
        #_ = driver.get_log('browser') # returns the browser log and also clears it.
        #logs = driver.get_log("performance")
        #print(len(logs))
        for log in logs[:]:
            try:
                url = json.loads(log.get("message")).get("message").get("params").get("request").get("url")
                # print(json.loads(log.get("message")).get("message").get("response"))#空的
            except:
                continue
            print(url)
            bCatchOK,bodyInfo = get_body(log, driver)
            print('===============================================================================')


        if src == '':
            CloseChrome(pids, datadir)
            time.sleep(5)
            createNewDriver = True
            continue

    a = input()