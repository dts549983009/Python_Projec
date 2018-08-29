#!/usr/bin/env python3
#coding=utf-8
'''
name:Levi
date:2015-5-30
email:lvze@tedu.cn
modules:python3.5 mysql pymysql
This is a dict project for AID
'''
from socket import *
import os
import signal
import sys
import time
import pymysql
from hashlib import sha1

#链接mysql
db = pymysql.connect('localhost', 'root', '123456', 'dict')


#实现功能模块
class TftpServer(object):
    def __init__(self,connfd, db):
        self.connfd = connfd


    def do_login(self, name, password):
        #  用sha1给pwd加密
        s1 = sha1() #创建sha1加密对象
        s1.update(password.encode("utf8")) #指定编码
        pwd2 = s1.hexdigest() # 返回16进制加密结果
        sql_select = "select password from user where name='%s';" % name
        cursor = db.cursor()
        cursor.execute(sql_select)
        result = cursor.fetchone()
        if result:
            if result[0] == pwd2:
                print("%s登录成功" % name)
                self.connfd.send(b"OK")
            # 您输入的密码错误，请重新输入
            else:
                self.connfd.send(b"ERROR")
        # 您输入的账号不存在，请进行注册
        else:
            self.connfd.send(b"EXISTS")

    def do_register(self, name, password):
        #　用sha1给pwd加密
        s1 = sha1() #创建sha1加密对象
        s1.update(password.encode("utf8")) #指定编码
        pwd2 = s1.hexdigest() # 返回16进制加密结果
        sql_select = "select name from user where name='%s';" % name
        cursor = db.cursor()
        cursor.execute(sql_select)
        result = cursor.fetchone()
        if result:
            self.connfd.send("用户名已存在，请重新输入".encode())
        else:
            try:
                sql_insert = '''insert into user(name, password) values("%s", "%s");''' % (name, pwd2)
                cursor.execute(sql_insert)
                print("%s注册成功" % name)
                self.connfd.send("OK".encode())
                db.commit()
            except:
                db.rollback()
                return
        cursor.close()
        
    def do_search(self, name, word):
        sql_select = "select interpreter from word where word='%s';" % word
        cursor = db.cursor()
        cursor.execute(sql_select)
        result = cursor.fetchone()
        # 查询到该单词
        if result:
            try:
                self.connfd.send(b'OK')
                time.sleep(0.1)
                self.connfd.send(result[0].encode())
                print("【%s】查询成功" % word)
                sql_insert = '''insert into hist(name, word, time) values("%s", "%s", "%s");''' % (name, word, time.ctime())
                cursor.execute(sql_insert)
                print("【%s】记录添加成功" % word)
                db.commit()
            except:
                db.rollback()
                return
        else:
            self.connfd.send("无该单词".encode())
        cursor.close()

    def do_history(self, name):
        sql_select = "select * from hist where name='%s';" % name
        cursor = db.cursor()
        cursor.execute(sql_select)
        result = cursor.fetchall()
        # 查询到该单词
        if result:
            self.connfd.send(b'OK')
            time.sleep(0.1)
            result_text = ''
            for i in result:
                result_text = result_text + i[1] + ' ' + i[2] + ' ' + i[3]+ '#'
            self.connfd.send(result_text.encode())
            print("记录发送成功")
        else:
            msg = "您无历史查询记录" % name
            self.connfd.send(msg.encode())
        db.commit()
        cursor.close()
        
#流程控制，创建套接字，创建并发，方法调用
def main():
    HOST = '0.0.0.0'
    PORT = 8888
    ADDR = (HOST,PORT)

    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(ADDR)
    sockfd.listen(5)

    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            connfd,addr = sockfd.accept()
            print("客户端登录:",addr)
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue

        #创建父子进程
        pid = os.fork()

        if pid == 0:
            sockfd.close()
            tftp = TftpServer(connfd, db)  # __init__传参
            while True:
                data = connfd.recv(1024).decode()
                print("Request:", data)
                msg = data.split(' ')
                if (not data) or (msg[0] == 'Q'):
                    print("客户端退出")
                    connfd.close()
                    sys.exit(0)
                elif msg[0] == "L":
                    tftp.do_login(msg[1], msg[2])
                elif msg[0] == 'R':
                    tftp.do_register(msg[1], msg[2])
                elif msg[0] == 'S':
                    tftp.do_search(msg[1], ' '.join(msg[2:]))
                elif msg[0] == 'H':
                    tftp.do_history(msg[1])
                elif msg[0] == 'out':
                    print("%s用户已注销登录" % msg[1])
                else:
                    print("客户端发送错误指令")
        else:
            connfd.close()
            continue


if __name__ == "__main__":
    main()
    db.close()
