#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sys,time
from optparse import OptionParser
from selenium import webdriver
from pyvirtualdisplay import Display

class Login_Web(object):
    def __init__(self,describe,hostname,web = "http://??/cacti.com",username = '??',password = '??'):
        self.web = web
        self.username = username
        self.password = password
        self.describe = describe
        self.hostname = hostname
        self.description = self.describe+'_'+self.hostname

    def shut_down_image(self):
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.stylesheet', 2)
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        return firefox_profile

    def _simulate_display(self):
        firefox_profile = self.shut_down_image()
        self.display = Display(visible = 0, size = (1300,600))
        self.display.start()
        driver = webdriver.Firefox(firefox_profile)
        self.driver = driver
        self.driver.implicitly_wait(20)
        self.driver.get(self.web)

    def login_page(self):
        self._simulate_display()
        self.driver.find_element_by_name('login_username').send_keys(self.username)
        self.driver.find_element_by_name('login_password').send_keys(self.password)
        self.driver.find_element_by_xpath("//*[@type = 'submit']").click()

    def main_page(self):
        self.login_page()
        self.driver.find_element_by_link_text('Devices').click()
        self.driver.find_element_by_link_text('Add').click()
        self.driver.find_element_by_name('description').send_keys(self.description)
        self.driver.find_element_by_name('hostname').send_keys(self.hostname)
        self.driver.find_element_by_xpath("//*[@id = 'host_template_id']/*[@value = '3']").click()
        self.driver.find_element_by_xpath("//*[@value = 'Create' and @type = 'submit']").click()

    def add_graph(self):
        self.main_page()
        self.driver.find_element_by_link_text('Create Graphs for this Host').click()
        self.driver.find_element_by_name('all_cg').click()
        eth0_state = self.driver.find_element_by_id('text1_c81e728d9d4c2f636f067f89cc14862c_1').text
        if eth0_state != 'Down':
            self.driver.find_element_by_name('sg_1_c81e728d9d4c2f636f067f89cc14862c').click()
        self.driver.find_element_by_name('sg_1_eccbc87e4b5ce2fe28308fd9f2a7baf3').click()
        self.driver.find_element_by_name('sg_2_c4ca4238a0b923820dcc509a6f75849b').click()
        self.driver.find_element_by_name('sg_2_45c48cce2e2d7fbdea1afc51c7c6ad26').click()
        self.driver.find_element_by_xpath("//*[@value = 'Create' and @type = 'submit']").click()

    def get_loop(self):
        host_list = self.driver.find_elements_by_xpath('//a[@class = "linkEditMain"]')
        host_zip = zip(range(len(host_list)),host_list)
        for i,j in host_zip:
            print str(i)+':'+j.get_attribute("text")
        try:
            host_select = int(sys.argv[3])
        except:
            host_select = int(raw_input("select net(num):"))
        value = host_zip[host_select][1].get_attribute("text")
        print value + ' was selected'
        self.driver.find_element_by_link_text(value).click()

    def get_drag_add(self):
        get_strong = self.driver.find_elements_by_xpath("//a[strong]")
        get_strong_add = self.driver.find_elements_by_xpath("//a[3]")
        get_all = zip(range(len(get_strong)),get_strong,get_strong_add)
        for a,b,c in get_all:
            print str(a)+":"+b.get_attribute('text')
        try:
            host_add = int(sys.argv[4])
        except:
            host_add = int(raw_input("select netadd(num):"))
        get_all[host_add][2].click()

    def get_single_add(self):
        self.driver.find_element_by_link_text('Add').click()

    def final_common(self):
        self.driver.find_element_by_xpath("//select[@name = 'type_select']/option[text() = 'Graph']").click()
        eth0 = self.description + ' - Traffic - eth0'
        eth1 = self.description + ' - Traffic - eth1'
        try:
            self.driver.find_element_by_xpath('//select[@name = "local_graph_id"]/option[text() = "%s"]'%eth0).click()
        except:
            print 'no eth0'
        else:
            self.driver.find_element_by_xpath("//*[@value = 'Create' and @type = 'submit']").click()
            self.driver.back()
        try:
            self.driver.find_element_by_xpath('//select[@name = "local_graph_id"]/option[text() = "%s"]'%eth1).click()
        except:
            print 'no eth1'
        else:
            self.driver.find_element_by_xpath("//*[@value = 'Create' and @type ='submit']").click()


    def get_main(self):
        self.driver.find_element_by_link_text('Graph Trees').click()
        self.get_loop()
        try:
            self.driver.find_element_by_xpath("//*[@value = 'Collapse All' and @title = 'Collapse All Trees']").click()
            self.driver.find_element_by_xpath("//img[@src = 'images/show.gif']")
        except:
            self.get_single_add()
        else:
            self.get_drag_add()
        finally:
            self.final_common()
            self.driver.close()
            self.display.stop()
            print self.description + ' was successfully added'

    def notify(self,msg,cl=32):
        return "\033[{0}m{1}\033[0m".format(cl,msg)

    def main(self):
        btime = int(time.time())
        try:
            self.add_graph()
            self.get_main()
            print self.notify("consumed time:%d s" % (int(time.time()) - btime,))
        except:
            self.driver.close()
            self.display.stop()

if __name__=='__main__':
    webna = {'example1' : 'http://??/cacti/',
            'example2' : 'http://???/cacti/',
            'example3' : 'http://????/cacti/',
            'example4' : 'http://?????/cacti'}
    optParse = OptionParser()
    optParse.add_option('-w','--web',dest='web',help="verify url to access".decode("utf-8"))
    try:
        (option,args) = optParse.parse_args()
        if option.web == None:
            raise
    except:
        web = Login_Web(describe = sys.argv[1],hostname = sys.argv[2])
    else:
        print webna[option.web]
        web = Login_Web(describe = sys.argv[1],hostname = sys.argv[2],web = webna[option.web])
    web.main()
