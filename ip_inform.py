#!/usr/bin/python
# -*- coding: UTF-8 -*-
from add_cacti import *
import sys
class Login_Back(Login_Web):
    def __init__(self,web = 'http://idc.uqee.com/Login/index.html',userName = '??',userPass = '??'):
        self.userName = userName
        self.userPass = userPass
        self.web = web

    def login_page(self):
        self._simulate_display()
        self.driver.find_element_by_name('userName').send_keys(self.userName)
        self.driver.find_element_by_name('userPass').send_keys(self.userPass)
        self.driver.find_element_by_name('image').click()

    def searchip(self,ip):
        self.driver.find_element_by_id('q_contnet').send_keys('%s'%ip)
        self.driver.find_element_by_name('submit').click()
        self.driver.find_element_by_id('q_contnet').clear()
        self.driver.switch_to.frame("pageContent")
        self.driver.find_element_by_link_text('%s'%ip).click()
        try:
            if self.driver.find_element_by_id('showIsHost1').text == '':
                raise
        except:
            print ip + "   " + self.driver.find_element_by_name('remark').get_attribute("value")
            self.sub_ip()
            self.driver.switch_to.default_content()
        else:
            print "    " + ip + "   " + self.driver.find_element_by_name('remark').get_attribute("value"),
            print self.driver.find_element_by_id('showIsHost1').text
            self.driver.switch_to.default_content()

    def sub_ip(self):
        try:
            self.driver.find_element_by_id('virHostList')
        except:
            pass
        else:
            ip_list = []
            descript_list = []
            for i in self.driver.find_elements_by_xpath('//table[@id="vir_list_2"]/tbody/tr/td[3]'):
                ip_list.append(i.text)
            for i in self.driver.find_elements_by_xpath('//table[@id="vir_list_2"]/tbody/tr/td[12]'):
                descript_list.append(i.text)
            ip_list.pop(0)
            descript_list.pop(0)
            for i,j in zip(ip_list,descript_list):
                print "    " + i + "    " + j

    def main(self,iplist):
        self.login_page()
        btime = int(time.time())
        try:
            for i in iplist:
                self.searchip(i)
            print self.notify("consumed time:%d s" % (int(time.time()) - btime,))
        except:
            print 'stop search'
        finally:
            self.driver.close()
            self.display.stop()

if __name__=='__main__':
    go_search = Login_Back()
    try:
        text = sys.argv[1]
    except:
        text = raw_input("input listip text: ")
    iplist = []
    with open(text,"r") as f1:
        for i in f1.readlines():
            iplist.append(i.split('\n')[0])
    go_search.main(iplist)
