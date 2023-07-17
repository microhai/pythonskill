from cefpython3 import cefpython as cef
import sys
import os
import time
import threading
import win32gui
import pyautogui
import pyperclip
import cv2
import sqlite3 as db
from PIL import ImageGrab
import win32api
import win32.lib.win32con as win32con
#https://github.com/cztomczak/cefpython/blob/master/api/RequestHandler.md#onbeforebrowse
#https://github.com/cztomczak/cefpython/tree/master/src
HTML_code = """
<div>hello world</div>
"""
titlename = 'PYCEF login subway'
subwaycktxt = ''#'D:\subwayck.txt'
subwayckdb = ''#'D:\cefdata\Cookies'
cachedir = ''
currentFileDir = ''
#锁屏下截图
def grab_screen_1(left,top,right,bottom, path):
    im = ImageGrab.grabclipboard()
    while True:
        win32api.keybd_event(win32con.VK_SNAPSHOT, 0, 0, 0)
        time.sleep(1)
        win32api.keybd_event(win32con.VK_SNAPSHOT, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(3)
        #filename = 'a.png'
        im = ImageGrab.grabclipboard()
        if im is None:
            print('===>is None ')
        else:
            print('===>' + str(im.size))
            break

    print('===>get ' + str(im.size))
    rect = (left, top, right, bottom)
    im = im.crop(rect)
    #im.show()
    #im.save(filename, 'PNG')
    im.save(path, 'PNG')
    return im
    
    
# 从SQLite文件中读取数据
def readFronSqllite(db_path,exectCmd):
    conn = db.connect(db_path)  # 该 API 打开一个到 SQLite 数据库文件 database 的链接，如果数据库成功打开，则返回一个连接对象
    cursor=conn.cursor()        # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
    conn.row_factory=db.Row     # 可访问列信息
    cursor.execute(exectCmd)    #该例程执行一个 SQL 语句
    rows=cursor.fetchall()      #该例程获取查询结果集中所有（剩余）的行，返回一个列表。当没有可用的行时，则返回一个空的列表。
    return rows


def main():
    logpath = cachedir + '\\debug.log'
    print(logpath)
    print(cachedir)
    settings = {
        "debug": True,
        "log_severity": cef.LOGSEVERITY_INFO,
        "log_file": logpath,
        "cache_path":cachedir,
        "user_agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    }

    sys.excepthook = cef.ExceptHook
    cef.Initialize(settings=settings)
    url = ''
    ckm = cef.CookieManager.CreateManager(path=cachedir, persist_session_cookies=True)
    ckm.SetStoragePath(path=cachedir, persistSessionCookies=True)
    browser = cef.CreateBrowserSync(url=url, window_title=titlename)  # cef.GetDataUrl(HTML_code))
    
    browser.SetClientHandler(RequestHandler())
    browser.SetUserData("cookieManager", ckm)
    #hwnd = win32gui.GetForegroundWindow()
    hwnd = win32gui.FindWindow(None, titlename)
    if hwnd != None:
        win32gui.MoveWindow(hwnd, 0, 0, 1280, 768, True)
    cef.MessageLoop()
    cef.Shutdown()

    
class RequestHandler(object):
    def __init__(self):
        self.getcount = 0
        self.setcount = 0
 
    def GetResourceHandler(self, frame, request, **_):
        return
        #print("GetResourceHandler url="+request.GetUrl())
        #str = request.GetHeaderMultimap()
        #print(str)
        #ms = request.GetHeaderMap()
        #for key in ms:
        #    print("GetResourceHandler key=" + key + '---value=' + ms[key])
       
    def CanGetCookies(self, frame, request, **_):
        #return True
        # There are multiple iframes on that website, let's log
        # cookies only for the main frame.
        #if frame.IsMain():
        self.getcount += 1
        print("-- CanGetCookies #"+str(self.getcount))
        print("url="+request.GetUrl()[0:80])
        print("")
        return True
        # Return True to allow reading cookies or False to block
        #return True
 
    def CanSetCookie(self, frame, request, cookie, **_):
        #return True
        # There are multiple iframes on that website, let's log
        # cookies only for the main frame.
        #if frame.IsMain():
        self.setcount += 1
        print("-- CanSetCookie @"+str(self.setcount))
        print("url="+request.GetUrl()[0:80])
        print("Name="+cookie.GetName())
        print("Value="+cookie.GetValue())
        
        #filter url get cookie
        if request.GetUrl().find('') != -1 or request.GetUrl().find('') != -1 or request.GetUrl().find('') != -1:
            if cookie.GetValue() != '':
                strcookie = cookie.GetName() + '=' + cookie.GetValue() + ';'
                try:
                    file1 = open(subwaycktxt, 'a+')
                    file1.write(strcookie)
                finally:
                    file1.close()
        # Return True to allow setting cookie or False to block
        # need subway cookie
        return True
        
def GetImgPos(srcfile, targetfile):
    imgsrc = cv2.imread(srcfile)
    imgtget = cv2.imread(targetfile)
    res=cv2.matchTemplate(imgsrc,imgtget,cv2.TM_CCOEFF_NORMED)
    min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
    return max_loc
    
def AutoInput2():
    bigimgpath = currentFileDir + "\\screen.png"
    #imgsr = grab_screen_1(0, 0, 1000, 1000, bigimgpath)#pyautogui.screenshot(bigimgpath)
    imgsr = pyautogui.screenshot(bigimgpath)
    #与模版比对
    tbuserloc = GetImgPos(bigimgpath, currentFileDir + '\\tbname.png')
    print(tbuserloc)
    num_seconds = 2
    pyautogui.moveTo(tbuserloc[0] + 50, tbuserloc[1] + 10, duration=num_seconds)
    time.sleep(3) 
    pyautogui.click()
    pyperclip.copy("username")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2)   
    

    tbuserloc = GetImgPos(bigimgpath, currentFileDir + '\\tbpwd.png')
    num_seconds = 2
    pyautogui.moveTo(tbuserloc[0] + 50, tbuserloc[1] + 10, duration=num_seconds)
    time.sleep(3) 
    pyautogui.click()
    pyperclip.copy("userpwd")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2)
    
    #需要重新截图，获得滑动块的位置
    #imgsr = pyautogui.screenshot(bigimgpath)

    #tbdrag = GetImgPos(bigimgpath, currentFileDir + '\\tbdrag.png')
    #moveToX = tbdrag[0]
    #moveToY = tbdrag[1]
    #pyautogui.moveTo(moveToX,moveToY, duration=num_seconds)      #移动到滑块的位置
    #pyautogui.mouseDown()                  #按下鼠标
    #moveToX=moveToX+300                    #要拖动的距离
    #pyautogui.moveTo(moveToX,moveToY)      #拖动
    #pyautogui.mouseUp()                    #松开鼠标，验证完成
    #time.sleep(2)
    
    tbdrag = GetImgPos(bigimgpath, currentFileDir + '\\tbbtnlogin.png')
    moveToX = tbdrag[0]
    moveToY = tbdrag[1]
    pyautogui.moveTo(moveToX,moveToY, duration=num_seconds)
    pyautogui.click()
    time.sleep(25)
    cef.Shutdown()
    
    
def AutoInput1():
    hwnd = win32gui.FindWindow(0, titlename)
    if hwnd != None:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        print('left-' + str(left) + '-top-' + str(top))
        
        userleft = left + 416
        usertop = top + 128
        pwdleft = left + 416
        pwdtop = top + 190
        time.sleep(2)
        pyautogui.moveTo(userleft, usertop, duration=2)
        pyautogui.click()
        pyperclip.copy("username")
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)
        pyautogui.moveTo(pwdleft, pwdtop, duration=2)
        pyautogui.click()
        pyperclip.copy("userpwd")
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)
        dropbeginleft = left + 380
        dropbegintop = top + 250
        dropendleft = left + 640
        dropendtop = top + 270
        moveToX = dropbeginleft
        moveToY = dropbegintop
        
        #移动滑块
        pyautogui.moveTo(moveToX,moveToY)      #移动到滑块的位置
        pyautogui.mouseDown()                  #按下鼠标
        moveToX=moveToX+300                    #要拖动的距离
        pyautogui.moveTo(moveToX,moveToY)      #拖动
        pyautogui.mouseUp()                    #松开鼠标，验证完成
        time.sleep(2)
        
        #登录
        pyautogui.moveTo(moveToX-250,moveToY+60)  #移动到登录位置
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        
        #pyautogui.click(dropbeginleft, dropbegintop, button='left')
        #pyautogui.dragRel(270, 0, button='left',duration=5) #相对位置
        #pyautogui.dragTo(dropendleft, dropendtop, 3, pyautogui.easeOutQuad)#先慢后快的方式
        time.sleep(20)
        cef.Shutdown()
            
def AutoLogin(hello):
    while True:
        time.sleep(20)
        print(hello)
        AutoInput2()
        break
        
def ReadCkSql():
    rowinfo = readFronSqllite(subwayckdb, 'select host_key,name,value from main.cookies')
    towriteck = ''
    for item in rowinfo:
        host_key = item[0]
        name = item[1]
        value = item[2]
        print(host_key + ',' + name + '=' + value)
        if host_key.find('.taobao.com') != -1:
            towriteck = towriteck + name
            towriteck = towriteck + '='
            towriteck = towriteck + value
            towriteck = towriteck + ';'
    print(towriteck)
    try:
        file1 = open(subwaycktxt, 'a')
        file1.write(towriteck)
    finally:
        file1.close()

if __name__ == '__main__':
    #print(os.getcwd())
    currentFileDir = os.path.abspath(os.path.dirname(__file__))
    print(currentFileDir)
    subwaycktxt = currentFileDir + '\\subwayck.txt'#'D:\subwayck.txt'
    cachedir = currentFileDir + '\\cefdata'
    subwayckdb = cachedir + '\\Cookies'
    print(subwaycktxt)
    print(subwayckdb)
    try:
        file1 = open(subwaycktxt, 'w')
        file1.write('')
    finally:
        file1.close()
    hw = 'hello hi'
    t = threading.Thread(target = AutoLogin, args=(hw,))
    t.start()
    main()
    time.sleep(3)
    ReadCkSql()
    