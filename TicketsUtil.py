# -*- coding: utf-8 -*-

from splinter.browser import Browser
from time import sleep

class TicketsUtil(object):
    
    def __init__(self):
        self.loadBasicInfo()
        
    def loadBasicInfo(self):
        # 登录的url
        self.loginUrl = 'https://kyfw.12306.cn/otn/login/init'
        #登录成功后的url
        self.myUrl = 'https://kyfw.12306.cn/otn/index/initMy12306'
        #余票查询页面
        self.ticketUrl = 'https://kyfw.12306.cn/otn/leftTicket/init'
        # 初始化驱动
        self.driver=Browser(driver_name='chrome',executable_path='/Users/xxx/Downloads/chromedriver')
        # 初始化浏览器窗口大小
        self.driver.driver.set_window_size(1400, 1000)

    def login(self):
        print("开始登录...")
        # 登录
        self.driver.visit(self.loginUrl)
        
        self.username = input("\n请输入用户名，输入按回车...")
        #合法性判断
        while True:   
            if self.username == '':
                self.username = input("\n请输入用户名，输入按回车...")
            else:
                break

        self.password = input("\n请输入密码，输入按回车...")
        #合法性判断
        while True:   
            if self.password == '':
                self.password = input("\n请输入密码，输入按回车...")
            else:
                break

        # 自动填充用户名
        self.driver.fill("loginUserDTO.user_name", self.username)
        # 自动填充密码
        self.driver.fill("userDTO.password", self.password)
            

        print(u"等待验证码，自行输入...")

        # 验证码需要自行输入，程序自旋等待，直到验证码通过，点击登录
        while True:
            if self.driver.url != self.myUrl:
                sleep(1)
            else:
                break
        
        print(u"登录成功...")
                
    def query(self):
        self.source = input("\n请输入出发地（格式为：北京,BJP），输入按回车...")
        #合法性判断
        while True:   
            if self.source == '':
                self.source = input("\n请输入出发地（格式为：北京,BJP），输入按回车...")
            else:
                break
                
        self.destination = input("\n请输入目的地（格式为：深圳,SZQ），输入按回车...")
        while True:   
            if self.destination == '':
                self.destination = input("\n请输入目的地（格式为：深圳,SZQ），输入按回车...")
            else:
                break
                
        self.date = input("\n请输入出发日期（格式为：2018-02-14），输入按回车...")
        while True:   
            if self.date == '':
                self.date = input("\n请输入出发日期，输入按回车...")
            else:
                break
        #转换输入的出发地成"武汉,WHN"，再进行编码
        self.source = self.source.encode('unicode_escape').decode("utf-8").replace("\\u", "%u").replace(",", "%2c")
        #转换输入的目的地
        self.destination = self.destination.encode('unicode_escape').decode("utf-8").replace("\\u", "%u").replace(",", "%2c")
                  
        # 加载出发地
        self.driver.cookies.add({"_jc_save_fromStation": self.source})
        # 加载目的地
        self.driver.cookies.add({"_jc_save_toStation": self.destination})
        # 加载出发日
        self.driver.cookies.add({"_jc_save_fromDate": self.date})
        
        # 带着查询条件，重新加载页面
        self.driver.reload()
        # 查询余票
        self.driver.find_by_text(u"查询").click()
        sleep(0.1)
        # 查询余票
        self.driver.find_by_text(u"查询").click()
        
        print('查询成功')

    """入口函数"""
    def start(self):
        self.loadBasicInfo()

        # 登录，自动填充用户名、密码，自旋等待输入验证码，输入完验证码，点登录后，访问 tick_url（余票查询页面）
        self.login()

        # 登录成功，访问余票查询页面
        self.driver.visit(self.ticketUrl)
        
        self.query()

if __name__ == '__main__':
    print(u"===========自动查票开启===========")
    ticketsUtil = TicketsUtil()
    ticketsUtil.start()

