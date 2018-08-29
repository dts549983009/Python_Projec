#!/usr/bin/env python3
#coding=utf-8
from socket import *
import sys
import getpass


#实现各种功能请求
class TftpClient(object):
    def __init__(self,sockfd):
        self.sockfd = sockfd
        self.name = ''


    def do_register(self):
        while True:
            self.name = input("用户名：")
            password1 = getpass.getpass("请输入6位密码：")
            password2 = getpass.getpass("请再次输入6位密码：")
            if len(password1.strip())!= 6:
                print("密码错误，请重新输入")
            elif (' ' in self.name) or (' ' in password1):
                print("用户名和密码不允许有空格")
            elif password1 != password2:
                print("两次输入密码不一致")
            else:
                msg = 'R ' + self.name + ' ' + password1
                #发送请求类型
                self.sockfd.send(msg.encode())
                #接收服务器回应
                data = self.sockfd.recv(1024).decode()
                if data == "OK":
                    print("您注册成功！")
                    return password1
                else:
                    #请求失败原因
                    print(data)

    def do_login(self, password=''):
        while True:
            if not password:
                self.name = input("用户名：")
                password = getpass.getpass("请输入6位密码：")
            msg = 'L ' + self.name + ' ' + password
            #发送请求类型
            self.sockfd.send(msg.encode())
            #接收服务器回应
            data = self.sockfd.recv(1024).decode()
            if data == "OK":
                print("您登录成功！")
                self.select_option()
                msg = 'out ' + self.name
                self.sockfd.send(msg.encode())
                break
            #请求失败原因
            elif data == "ERROR":
                print("您输入的密码错误，请重新输入")
                password=''
                continue

            elif data == "EXISTS":
                print("您输入的账号不存在，请进行注册")
                break

    def do_search(self):
        while True:
            word = input("请输入查询单词：")
            if not word:
                break
            msg = 'S ' + self.name + ' ' + word
            self.sockfd.send(msg.encode())
            data = self.sockfd.recv(1024).decode()
            if data == "OK":
                interpreter = self.sockfd.recv(1024).decode()
                print('【%s】释义: ' % word + interpreter)
            else:
                print(data)

    def do_history(self):
        L = []
        msg = 'H ' + self.name
        self.sockfd.send(msg.encode())
        data = self.sockfd.recv(1024).decode()
        if data == "OK":
            with open('recode.txt', 'w') as f1:
                while True:
                    recode_text = self.sockfd.recv(4096).decode()
                    if len(recode_text) <= 4096:
                        f1.write(recode_text)
                        break
                    f1.write(recode_text)
            with open('recode.txt') as f2:
                recode_text = f2.read()
            # recode_text = self.sockfd.recv(4096).decode()
            recode_list = recode_text.split("#")
            del recode_list[-1]
            for recode in recode_list:
                a = recode.split(" ")
                b = [a[0], ' '.join(a[1:-5]), ' '.join(a[-5:-1])]
                L.append(b)
                print(b)
            print("【历史记录】展示完毕")
        else:
            # 请求失败原因发过来
            print(data)

    def select_option(self):
        while True:
            print("")
            print("==========二级界面==========")
            print("1.search  2.history  3.logout")
            print("===========================")
            cmd = input("输入命令>>")

            if cmd.strip() == "1":
                self.do_search()
            elif cmd.strip() == "2":
                self.do_history()
            elif cmd.strip() == "3":
                print("注销成功，请选择其他操作")
                break
            else:
                print("请输入正确命令！")
                sys.stdin.flush() # 清除输入
#创建套接字建立连接
def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)
    sockfd = socket()
    sockfd.connect(ADDR)
    tftp = TftpClient(sockfd)   #__init__是否需要传参
    while True:
        print("")
        print("==========一级界面==========")
        print("1.login  2.register  3.quit")
        print("===========================")

        cmd = input("输入命令>>")

        if cmd.strip() == "1":
            tftp.do_login()
        elif cmd.strip() == "2":
            password = tftp.do_register()
            tftp.do_login(password)
        elif cmd.strip() == "3":
            sockfd.send(b'Q')
            sockfd.close()
            sys.exit("欢迎再次使用")
        else:
            print("请输入正确命令！")
            sys.stdin.flush() # 清除输入


if __name__ == "__main__":
    main()