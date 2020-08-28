#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('conda activate web_surf')


# In[2]:


import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select


# In[3]:


driver = webdriver.Chrome(r'./chromedriver.exe')

driver.get('https://badgameshow.com')


# In[4]:


login_box = driver.find_element_by_xpath('//*[@id="left"]/ul[1]/li/input[2]')

login_box.click()


# In[5]:


account = '<ACCOUNT>'
password = '<PASSWORD>'


# In[6]:


acc_box = driver.find_element_by_xpath('//*[@id="right"]/div[2]/table/tbody/tr[1]/td/div/input')
pass_box = driver.find_element_by_xpath('//*[@id="right"]/div[2]/table/tbody/tr[2]/td/div/input')

acc_box.send_keys(account)
pass_box.send_keys(password)


# In[7]:


submit_box = driver.find_element_by_xpath('//*[@id="right"]/div[2]/div/input[1]')
submit_box.click()

submit_confirm = driver.find_element_by_xpath('//*[@id="right"]/div[2]/div/input[4]')
submit_confirm.click()


# In[8]:


time.sleep(3)


# In[9]:


def check_health():
    health_bar = driver.find_element_by_xpath('//*[@id="mhp"]')
    health = health_bar.text.split('/')
    
    if int(health[0]) < 400:
        town_facilities = Select(driver.find_element_by_xpath('//*[@id="townf"]/select'))
        town_facilities.select_by_value('inn')
        exec_box = driver.find_element_by_xpath('//*[@id="townbutton"]')
        exec_box.click()
        time.sleep(1)
        
        driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@name='actionframe']"))
        back_town = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/input')
        back_town.click()
        driver.switch_to.parent_frame()
        time.sleep(5)


# In[10]:


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
        time.sleep(3)


# In[11]:


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


# In[12]:


def quest():
    town_facilities = Select(driver.find_element_by_xpath('//*[@id="townf"]/select'))
    town_facilities.select_by_value('quest')
    exec_box = driver.find_element_by_xpath('//*[@id="townbutton"]')
    exec_box.click()
    time.sleep(1)
    
    try:
        driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@name='actionframe']"))
        finish_quest = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/form[1]/input[6]')
        finish_quest.click()
        driver.switch_to.parent_frame()
        
        finish_quest = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/form/input[5]')
        finish_quest.click()
        driver.switch_to.parent_frame()
        
        driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@name='actionframe']"))
        get_quest = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/form[1]/input[6]')
        get_quest.click()
        driver.switch_to.parent_frame()
        
        
        driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@name='actionframe']"))
        
        text = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td')
        counts = text.text[66:69]
        if counts[-1].isdigit() == False:
            counts = counts[:-1]
        counts = int(counts)
        battle_count = counts + 5
        
        back_town = driver.find_element_by_xpath('/html/body/table/tbody/tr[3]/td/input')
        back_town.click()
        driver.switch_to.parent_frame()
        time.sleep(1)
        print("quest done")
    except:
        print("finish quest failed")


# In[13]:


battle_loc_id = 3
battle_count = 100


# In[14]:


while True:
    try:
        progress = driver.find_element_by_xpath('//*[@id="tok"]')
        if progress.text[0] != '剩' and progress.text[0] != '行':
            continue
        if progress.text[0] == '剩':
            battle_count -= 1
            if battle_count == 0:
                quest()
        time.sleep(3)
        check_balance()
        check_health()
        auto_attack(battle_loc_id)
    except:
        print("Restarting")
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
        time.sleep(2)


# In[15]:


battle_count


# In[18]:


progress = driver.find_element_by_xpath('//*[@id="tok"]')
if progress.text[0] != '剩' and progress.text[0] != '行':
    pass
if progress.text[0] == '剩':
    battle_count -= 1
    if battle_count == 0:
        quest()
time.sleep(3)
check_balance()
check_health()
auto_attack(battle_loc_id)


# In[ ]:




