
import win32gui,win32con,time,re,random,urllib
import win32clipboard as w
from selenium import webdriver
import pymysql

'''config'''
min_price=150			#最小价格
max_price=200			#最大价格
keyword='内存条'

'''config'''

def setText(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()

def send_MessageQQ(msg):
    setText(msg)
    qq=win32gui.FindWindow(None,"咸鱼")
    win32gui.SendMessage(qq, 258, 22, 2080193)
    win32gui.SendMessage(qq, 770, 0, 0)
    win32gui.SendMessage(qq, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.SendMessage(qq, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
def insert_sql(foods_id,price,message):
    query_sql="SELECT foods_id,price FROM `xianyu` WHERE foods_id="+str(foods_id)
    sql="INSERT INTO xianyu (foods_id,price) VALUES ('"+str(foods_id)+"',"+str(price)+");"
    print(sql)
    print(query_sql)


    cursor.execute(query_sql)
    results = cursor.fetchall()
    print(len(results))
    print(results)
    if len(results)>0:
            print("数据已存在，判断价格是否一致")
            print(str(results[0][0]))
            print(str(foods_id))
            if float(results[0][1])==price:
                print("价格未更新")
            else:
                print(str(results[0][1]))
                print(price)
                cursor.execute('UPDATE xianyu SET price='+str(price)+' WHERE foods_id='+str(foods_id))
                db.commit()
                send_MessageQQ("原价格："+str(results[0][1])+"更新至"+str(price)+'\n'+message)

                '''发送QQ消息提醒'''
    else:
        print("无数据，添加新数据")
        cursor.execute(sql)
        db.commit()
        send_MessageQQ(message)

        '''发送QQ消息提醒'''



if __name__ == '__main__':

    db = pymysql.connect(host='localhost', port=3306, user="root", passwd="123456", db="xianyu")
    cursor = db.cursor()
    url ="https://s.2.taobao.com/list/?spm=2007.1000337.6.2.43eb7e89z8dJat&st_edtime=1&q="+urllib.parse.quote(keyword,encoding='gb2312')+"&ist=1"
    '''url="https://s.2.taobao.com"'''
    print(url)
    Chrome =webdriver.Chrome()
    Chrome.get(url)
    
    num=0
    while num==0:
        print(time.strftime("%Y-%m-%d %H-%M-%S",time.localtime()))
        id = Chrome.find_elements_by_css_selector('.item-pic a')
        price=Chrome.find_elements_by_css_selector('.item-attributes .price em')
        desc=Chrome.find_elements_by_class_name("item-brief-desc")
        pub_time=Chrome.find_elements_by_class_name("item-pub-time")
        print("获取到"+str(len(id))+"条数据")
        if len(id)==0:
            send_MessageQQ("页面错误")
        else:
            for i in range(0,len(id)):
                print("********************************************************")
                print(time.strftime("%Y-%m-%d %H-%M-%S",time.localtime()))
                print("当前第"+str(i+1)+"条")
                
                if float(price[i].text)*100<max_price and float(price[i].text)*100>min_price :
                    id_data=re.search('id=(\d+)',id[i].get_attribute('href'))
                    print("id:"+id_data.group(1)+'\n'+"价格："+price[i].text+'\n'+"描述："+desc[i].text+'\n'+pub_time[i].text)
                    message="链接：https://market.m.taobao.com/app/idleFish-F2e/widle-taobao-rax/page-detail?wh_weex=true&wx_navbar_transparent=true&id="+id_data.group(1)+'\n'+"价格："+price[i].text+'\n'+"描述："+desc[i].text+'\n'
                    insert_sql(str(id_data.group(1)), float(price[i].text),message)
                else:
                    print("价格未在设定区间"+str(pub_time[i].text))
                time.sleep(2)
                print("********************************************************")
                print("\n")
        timesl=random.randint(10000,15000)
        print("延时"+str(timesl)+"秒")
        time.sleep(timesl)
        Chrome.get(url)
        time.sleep(20)
        Chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(30)
        
        

