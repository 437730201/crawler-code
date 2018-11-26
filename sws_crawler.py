# -*- coding:utf-8 -*-
# from text import six
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
# from selenium import sendkeys
# from pywinauto.application import Application

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--proxy-server=http://ip:port')

driver=webdriver.Chrome(chrome_options = chromeOptions)
# driver = webdriver.PhantomJS(executable_path=r'E:\Pa\chromedriver.exe')

driver.implicitly_wait(30)

print(driver.get_cookie())

url = 'http://10.175.69.174/SWS/Login.aspx'
name = 'F1230997'
passwd = 'password'

class write_sws():

    user_xpath = '//*[@id="txtUserId"]'
    pw_xpath = '//*[@id="txtPassword"]'
    login_btn_xpath = '//*[@id="BtnLogin"]'
    mainfram = 'mainFrame'
    btnAdd_xpath = '//*[@id="btnAdd"]'

    pattern_choice_xpath = '//*[@id="ctl00_cphContent_ddlJob"]'
    case_choice_xpath = '//*[@id="ctl00_cphContent_ucSelectProjectInfo_ddlProject"]'

    product_choice_xpath = '//*[@id="ctl00_cphContent_ucSelectProjectInfo_ddlProductPhase"]'
    product_process_choice_xpath = '//*[@id="ctl00_cphContent_ucSelectProjectInfo_ddlProductPhase"]'
    product_type_xpath = '//*[@id="ctl00_cphContent_DDLTaxPro"]'

    word_describe_xpath =  '//*[@id="ctl00_cphContent_txtDescription"]'
    hour_xpath = '//*[@id="ctl00_cphContent_ddlHours"]'
    save_xpath = '//*[@id="ctl00_cphContent_btnSave"]'

    end_xpath = '//*[@id="ctl00_cphContent_gvList"]/tbody/tr[2]/td[1]'

    return_main_xpath = '//*[@id="aBulletin"]'

    start_date_xpath = '//*[@id="txtWorkDate"]'
    end_date_xpath = '//*[@id="txtEndate"]'

    end_save_xpath = '//*[@id="btnSave"]'

    btn_over_write_xpath = '//*[@id="WriteAll"]'
    btn_including_Saturday_xpath = '//*[@id="CheckSatur"]'

    process_text_dict = {
        1 : 'ALL',
        2 : 'CARRIER',
        3 : 'DVT',
        4 : 'EVT',
        5 : 'Pre PRO',
        6 : 'PRO1',
        7 : 'PRO2',
        8 : 'PRQ',
        9 : 'PVT',
        10: 'PVTE',
    }


    def __init__(self,user_name,url = url,user_pw = 'password',process_value = 6,word_describe = 'word harder.',word_hours = 8):

        self.login_html(url,user_name,user_pw)
        self.adjust_fram(write_sws.mainfram)
        self.come_into_middle()
        # 判断是否已经填写了内容
        flag = self.is_element_exist(write_sws.end_xpath)
        # flag = False
        print('flag',flag)

        self.process_value = process_value
        self.word_describe = word_describe
        self.word_hours = word_hours

        self.get_info(write_sws.user_xpath)
        self.main_func(flag)

    def main_func(self,flag):

        if flag is False:
            print('内容为空')
            #select_pattern
            self.select_choice(write_sws.pattern_choice_xpath,value=2)
            #select case
            self.select_choice(write_sws.case_choice_xpath,value=2)
            #select product
            self.select_choice(write_sws.product_choice_xpath,value=1)
            #select product process
            self.select_choice(write_sws.product_process_choice_xpath, value= self.process_value)
            # self.select_choice_by_text_value(write_sws.hour_xpath, value=write_sws.process_text_dict[process_value])
            # self.select_choice_by_text_value(write_sws.hour_xpath, value= process_value)
            #select product type
            self.select_choice(write_sws.product_type_xpath, value=2)

            self.fill_word_describe(self.word_describe)
            # select hour
            # self.select_choice_by_text_value(write_sws.hour_xpath,value= word_hours)
            self.select_choice(write_sws.hour_xpath,value= self.word_hours)
            # time.sleep(1)
            # driver.find_element_by_xpath(write_sws.btn_over_write_xpath).click()
            #保存
            self.click_btn(write_sws.save_xpath)
        else:
            print('内容不为空')
            # time.sleep(3)

        #回到主页面
        driver.back()
        self.adjust_fram(write_sws.mainfram)
        try:
            #点击保存
            self.reset_date_range()
            self.click_btn(write_sws.end_save_xpath)

            al = driver.switch_to.alert()
            al.accept()
        except:
            pass

        finally:
            # self.close_web()
            driver.quit()
            print('that is all.')


    def login_html(self,url,name,passwd):
        driver.get(url)
        print('Before login......')
        driver.maximize_window()

        title = driver.title
        print(title)
        driver.find_element_by_xpath(write_sws.user_xpath).clear()
        driver.find_element_by_xpath(write_sws.user_xpath).send_keys(name)
        driver.find_element_by_xpath(write_sws.pw_xpath).clear()
        driver.find_element_by_xpath(write_sws.pw_xpath).send_keys(passwd)
        self.click_btn(write_sws.login_btn_xpath)

    def get_info(self,xpath_value):

        obj = driver.find_element_by_xpath(xpath_value)

        if hasattr(obj,'size'):
            print(obj.size)

        if hasattr(obj,'text'):
            print(obj.text)

        if hasattr(obj,'type'):
            print(obj.get_attribute('type'))

        # size = driver.find_element_by_xpath(xpath_value).size
        # print(size)
        # text = driver.find_element_by_xpath(xpath_value).text
        # print(text)
        #   id  name type
        # attribute = driver.find_element_by_xpath(xpath_value).get_attribute('type')
        # print(attribute)
        # result = driver.find_element_by_xpath(xpath_value).is_displayed()
        # print(result)

    def adjust_fram(self,fram):
        # time.sleep(1)
        driver.switch_to.frame(driver.find_element_by_name(fram))

    def come_into_middle(self):
        driver.find_element_by_xpath(write_sws.btnAdd_xpath).click()

    def select_choice(self,choice_xpath,value = 2):
        option = choice_xpath + '/option[%s]'%(value)
        driver.find_element_by_xpath(choice_xpath).click()
        driver.find_element_by_xpath(option).click()

    def select_choice_by_text_value(self,choice_xpath,value):
        # select_by_value
        # option = choice_xpath + '/option[%s]' % (value)
        # pos = driver.find_element_by_xpath(choice_xpath)
        s1 = Select(driver.find_element_by_xpath(choice_xpath))
        s1.select_by_visible_text(value)

    def fill_word_describe(self,word_describe):
       driver.find_element_by_xpath(write_sws.word_describe_xpath).click()
       driver.find_element_by_xpath(write_sws.word_describe_xpath).send_keys(word_describe)

    def click_btn(self,xpath):
        driver.find_element_by_xpath(xpath).click()

    def is_element_exist(self, element):
        flag = True

        try:
            driver.find_element_by_xpath(element)
            return flag

        except:
            flag = False
            return flag

    def close_web(self):
        print('Finish')
        driver.close()

    def select_datetime(self,xpath,datetime):
        """

        :param xpath:
        :param datetime: 'xxxx/xx/xx'
        :return:
        """
        # js = "%s.attr('readonly','')"%(driver.find_element_by_xpath(xpath))
        # driver.execute_script(js)

        driver.find_element_by_xpath(xpath).clear()
        driver.find_element_by_xpath(xpath).click()
        driver.find_element_by_xpath(xpath).send_keys(datetime)

    def reset_date_range(self):
        import datetime
        today = datetime.datetime.now()
        weekday = today.weekday()

        first_date = today + datetime.timedelta(-weekday)
        last_date = today + datetime.timedelta(-weekday + 5)

        first_date_ = first_date.strftime('%Y/%m/%d')
        last_date_ = last_date.strftime('%Y/%m/%d')

        self.select_datetime(write_sws.start_date_xpath,first_date_)
        # time.sleep(0.5)
        self.select_datetime(write_sws.end_date_xpath,last_date_)
        # time.sleep(1)

if __name__ == '__main__':
    ws = write_sws(user_name = name,
                   word_describe='data analyse and AI support.',
                   process_value = 7,
                   word_hours = 9)
    #driver.forward()
    #driver.back()
    #driver.refresh()
