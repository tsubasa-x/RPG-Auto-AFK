#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# get_ipython().system('conda activate web_surf')


import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import datetime


# In[ ]:


f = open("./rpg_log.txt", "a+")
battle_count = 0
quest_finished = 0


# In[ ]:


def check_health():
    health_bar = driver.find_element_by_xpath('//*[@id="mhp"]')
    health = health_bar.text.split('/')
    mana_bar = driver.find_element_by_xpath('//*[@id="mmp"]')
    mana = mana_bar.text.split('/')
    
    if int(health[0]) < int(health[1]) or int(mana[0]) < int(mana[1]):
    # if True:
        town_facilities = Select(driver.find_element_by_xpath('//*[@id="townf"]/select'))
        town_facilities.select_by_value('inn')
        exec_box = driver.find_element_by_xpath('//*[@id="townbutton"]')
        exec_box.click()
        time.sleep(1)
        
        driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@name='actionframe']"))
        back_town = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/input')
        back_town.click()
        driver.switch_to.parent_frame()
        driver.execute_script("window.scrollTo(0, 550)") 
        time.sleep(2)


# In[ ]:


def check_balance():
    balance_box = driver.find_element_by_xpath('//*[@id="mgold"]/font[1]')
    balance = balance_box.text
    if balance[-1] == 'd':
        return
    balance = balance.split('萬')
    
    if int(balance[0]) >= 30:
        town_facilities = Select(driver.find_element_by_xpath('//*[@id="townf"]/select'))
        town_facilities.select_by_value('bank')
        exec_box = driver.find_element_by_xpath('//*[@id="townbutton"]')
        time.sleep(0.5)
        exec_box.click()
        time.sleep(1)
        
        driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@name='actionframe']"))
        back_town = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/form[2]/input[6]')
        back_town.click()
        driver.switch_to.parent_frame()
        time.sleep(1)
    
        driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@name='actionframe']"))
        back_town = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/input')
        back_town.click()
        driver.switch_to.parent_frame()
        driver.execute_script("window.scrollTo(0, 550)")
        time.sleep(2)


# In[ ]:


def auto_attack(val):
    box = driver.find_element_by_xpath('//*[@id="autoattack"]')
    if box.is_selected() is not True:
        location = Select(driver.find_element_by_xpath('//*[@id="table1"]/tbody/tr/td[1]/select'))
        location.select_by_value('%d'%val)
        try:
            box.click()
            time.sleep(2)
        except:
            pass


# In[ ]:


def quest():
    global f
    town_facilities = Select(driver.find_element_by_xpath('//*[@id="townf"]/select'))
    town_facilities.select_by_value('quest')
    exec_box = driver.find_element_by_xpath('//*[@id="townbutton"]')
    exec_box.click()
    time.sleep(2)
    try:
        driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@name='actionframe']"))
        finish_quest = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/form[1]/input[6]')
        finish_quest.click()
        driver.switch_to.parent_frame()
        
        driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@name='actionframe']"))
        finish_quest = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/form/input[5]')
        finish_quest.click()
        driver.switch_to.parent_frame()
        
        driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@name='actionframe']"))
        get_quest = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/form[1]/input[6]')
        get_quest.click()
        driver.switch_to.parent_frame()
        
        driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@name='actionframe']"))
        text = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td')
        counts = text.text[22:25]
        if counts[-1].isdigit() == False:
            counts = counts[:-1]
        counts = int(counts)
        print("counts quest : %d"%counts)
        global battle_count
        battle_count = counts
        
        back_town = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/input')
        back_town.click()
        driver.switch_to.parent_frame()
        driver.execute_script("window.scrollTo(0, 550)")
        time.sleep(2)
        
        current_time = datetime.now().strftime("%H:%M:%S")
        f.write("%s\tQuest Done\r\n"%current_time)
        # return counts
    except:
        print("quest err")
        driver.switch_to.parent_frame()
        current_time = datetime.now().strftime("%H:%M:%S")
        f.write("%s\tQuest Failed\r\n"%current_time)
        # return 0
 


# In[ ]:


def get_battle_count():
    global f
    town_facilities = Select(driver.find_element_by_xpath('//*[@id="townf"]/select'))
    town_facilities.select_by_value('quest')
    exec_box = driver.find_element_by_xpath('//*[@id="townbutton"]')
    exec_box.click()
    time.sleep(1.5)
    
    driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@name='actionframe']"))
    quest_info = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td')
    
    global battle_count
    counts = quest_info.text[66:69]
    
    if counts[0].isdigit() is not True:
        try:
            finish_quest = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/form[1]/input[6]')
            finish_quest.click()
            driver.switch_to.parent_frame()

            driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@name='actionframe']"))
            finish_quest = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/form/input[5]')
            finish_quest.click()
            driver.switch_to.parent_frame()

            driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@name='actionframe']"))
            get_quest = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/form[1]/input[6]')
            get_quest.click()
            driver.switch_to.parent_frame()

            driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@name='actionframe']"))
            text = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td')
            counts = text.text[22:25]
            if counts[-1].isdigit() == False:
                counts = counts[:-1]
            counts = int(counts)
            print("counts quest : %d"%counts)
            battle_count = counts

            #back_town = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/input')
            #back_town.click()
            #driver.switch_to.parent_frame()
            #driver.execute_script("window.scrollTo(0, 550)")
            #time.sleep(2)

            current_time = datetime.now().strftime("%H:%M:%S")
            f.write("%s\tQuest Done\r\n"%current_time)
            # return counts
        except:
            print("quest err")
            driver.switch_to.parent_frame()
            current_time = datetime.now().strftime("%H:%M:%S")
            f.write("%s\tQuest Failed\r\n"%current_time)
            # return 0
    else:
        if counts[1].isdigit() is not True:
            counts = counts[0]
        elif counts[-1].isdigit() is not True:
            counts = counts[:-1]
        
        counts = int(counts)
        battle_count = counts
        
    back_town = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/input')
    back_town.click()
    driver.switch_to.parent_frame()
    driver.execute_script("window.scrollTo(0, 550)")
    time.sleep(2)


# In[ ]:


while True:
    print("Starting Driver")

        #proxy = '211.21.92.211:4145'
        #chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--proxy-server=http://' + proxy)
        
    #options = webdriver.ChromeOptions()
    #prefs = {"profile.default_content_setting_values.notifications" : 2}
    #options.add_experimental_option("prefs",prefs)
    #options.add_argument("--disable-popup-blocking")
    #options.add_argument("--disable-notifications")
    
    driver = webdriver.Chrome(r'./chromedriver.exe')
    
    driver.execute_script("window.onbeforeunload = function() {};")
    
    driver.get('https://badgameshow.com')


    login_box = driver.find_element_by_xpath('//*[@id="left"]/ul[1]/li/input[2]')

    login_box.click()

    account = 'tsubasa'
    password = 'hane0423'


    acc_box = driver.find_element_by_xpath('//*[@id="right"]/div[2]/table/tbody/tr[1]/td/div/input')
    pass_box = driver.find_element_by_xpath('//*[@id="right"]/div[2]/table/tbody/tr[2]/td/div/input')

    acc_box.send_keys(account)
    pass_box.send_keys(password)

    submit_box = driver.find_element_by_xpath('//*[@id="right"]/div[2]/div/input[1]')
    submit_box.click()

    submit_confirm = driver.find_element_by_xpath('//*[@id="right"]/div[2]/div/input[4]')
    submit_confirm.click()


    time.sleep(3)
    
    try:
        alert = driver.switch_to.alert
        alert.accept()
        print("alert accepted")
    except:
        pass
    
    driver.execute_script("window.scrollTo(0, 550)")

    battle_loc_id = 4
    
    
    
    origin_battles = driver.find_element_by_xpath('//*[@id="ext_today_total"]')
    origin_battles = origin_battles.text[5:-1]
    origin_battles = int(origin_battles)
    
    get_battle_count()
    try:
        print("count : %d"%battle_count)
    except:
        continue

    restart_cnt = 0    
    
    while True:
        if restart_cnt > 5:
            break
        try:
            try:
                alert = driver.switch_to.alert
                alert.accept()
                print("alert accepted")
                sleep(1)
            except:
                pass
    
            progress = driver.find_element_by_xpath('//*[@id="tok"]')
            if progress.text[0] != '剩' and progress.text[0] != '行':
                box = driver.find_element_by_xpath('//*[@id="autoattack"]')
                if box.is_selected() is True:
                    continue
            
            
            current = driver.find_element_by_xpath('//*[@id="ext_today_total"]')
            current = int(current.text[5:-1])
            print("current : %d"%current)
            if current < origin_battles:
                origin_battles = current
                print("date changed")
            elif current >= origin_battles + battle_count:
                break
                quest()
                origin_battles = current
                print("Quest Done, battle count : %d"%battle_count)

            time.sleep(1.5)
            check_balance()
            check_health()
            auto_attack(battle_loc_id)

            current_time = datetime.now().strftime("%H:%M:%S")
            f.write("%s\tWorking\r\n"%current_time)
            
            restart_cnt = 0
            # if quest_finished >= 5:
            #     print("restarting driver")
            #     break
        except:
            current_time = datetime.now().strftime("%H:%M:%S")
            f.write("%s\tRestarting\r\n"%current_time)
            #driver.switch_to.parent_frame()
            driver.back()
            try:
                driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@name='actionframe']"))
                back_town = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/input')
                back_town.click()
                driver.switch_to.parent_frame()
                time.sleep(1)
            except:
                driver.forward()
            restart_cnt += 1
            time.sleep(2)

    driver.quit()
    time.sleep(1)

f.close()


# In[ ]:





# In[ ]:




