# -*- coding: utf-8 -*-
# Author:0verWatch


import re
import base64

from PyQt5.QtCore import QCoreApplication

from 密码学.des算法.DES_destruct import PC_1, IP_re_table, IP_table, SHIFT, E, PC_2, P, S
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
                             QInputDialog, QApplication)
import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QInputDialog
key=""
message=""


def write_in_file(str_mess):
    try:
        f = open('DES.txt','w',encoding='utf-8')
        f.write(str_mess)
        f.close()
        print("文件输出成功！")
    except IOError:
        print('文件加解密出错！！！')#将生成结果写进去

def read_out_file():
    try:
        f = open('DES.txt','r',encoding = 'utf-8')
        mess = f.read()
        f.close()
        print("文件读取成功！")
        return mess
    except IOError:
        print('文件加解密出错！！！')#读取文件


#字符串转化为二进制
def str2bin(message):
    res = ""
    for i in message:
        tmp = bin(ord(i))[2:]  #bin() 返回一个整数 int 或者长整数 long int 的二进制表示。
        #ord() 函数是 chr() 函数（对于8位的ASCII字符串）或 unichr() 函数（对于Unicode对象）的配对函数
        # 它以一个字符（长度为1的字符串）作为参数，返回对应的 ASCII 数值，或者 Unicode 数值，如果所给的 Unicode 字符超出了你的 Python 定义范围，则会引发一个 TypeError 的异常。
        for j in range(0,8-len(tmp)):
            tmp = '0'+ tmp   #把输出的b给去掉
        res += tmp
    return res


#二进制转化为字符串
def bin2str(bin_str):
    res = ""
    tmp = re.findall(r'.{8}',bin_str)
    for i in tmp:
        res += chr(int(i,2))
    return res
    # print("未经过编码的加密结果:"+res)
    # print("经过base64编码:"+str(base64.b64encode(res.encode('utf-8')),'utf-8'))


#IP盒处理
def ip_change(bin_str):
    res = ""
    for i in IP_table:
        res += bin_str[i-1]     #数组下标i-1
    print("IP处理后：",res)
    return res


#IP逆盒处理
def ip_re_change(bin_str):
    res = ""
    for i in IP_re_table:
        res += bin_str[i-1]
    print("IP逆处理后：",res)
    return res

#E盒置换
def e_key(bin_str):
    res = ""
    for i in E:
        res += bin_str[i-1]
    print("E盒置换后:",res)
    return res


#字符串异或操作
def str_xor(my_str1,my_str2):
    res = ""
    for i in range(0,len(my_str1)):
        xor_res = int(my_str1[i],10)^int(my_str2[i],10) #变成10进制是转化成字符串 2进制与10进制异或结果一样，都是1,0
        if xor_res == 1:
            res += '1'
        if xor_res == 0:
            res += '0'
    print("字符串异或后为:",res)
    return res


#循环左移操作
def left_turn(my_str,num):
    left_res = my_str[num:len(my_str)]
    left_res = my_str[0:num]+left_res
    print("循环左移后为:",left_res)
    return left_res


#秘钥的PC-1置换
def change_key1(my_key):
    res = ""
    for i in PC_1:
        res += my_key[i-1]
    print("PC1置换后的密钥为:",res)
    return res

#秘钥的PC-2置换
def change_key2(my_key):
    res  = ""
    for i in PC_2:
        res += my_key[i-1]
    print("PC2置换后的密钥为:",res)
    return res


# S盒过程
def s_box(my_str):
    res = ""
    c = 0
    for i in range(0,len(my_str),6):
        now_str = my_str[i:i+6]
        row = int(now_str[0]+now_str[5],2)
        col = int(now_str[1:5],2)
        num = bin(S[c][row*16 + col])[2:]   #利用了bin输出有可能不是4位str类型的值，所以才有下面的循环并且加上字符0
        for gz in range(0,4-len(num)):
            num = '0'+ num
        res += num
        c  += 1
    return res


#P盒置换
def p_box(bin_str):
    res = ""
    for i in  P:
        res += bin_str[i-1]
    return res



# F函数的实现
def fun_f(bin_str,key):
    first_output = e_key(bin_str)  #E盒置换
    second_output = str_xor(first_output,key) #字符串异或
    third_output = s_box(second_output) #S盒
    last_output = p_box(third_output) #P盒
    return last_output


def gen_key(key):
    key_list = []
    divide_output = change_key1(key)
    key_C0 = divide_output[0:28]
    key_D0 = divide_output[28:]
    for i in SHIFT:
        key_c = left_turn(key_C0,i) #循环左移
        key_d = left_turn(key_D0,i) #循环左移
        key_output = change_key2(key_c + key_d)  #密钥PC——2置换
        key_list.append(key_output)
    return key_list




def des_encrypt_one(bin_message,bin_key): #64位二进制加密的测试
    #bin_message = deal_mess(str2bin(message))
    mes_ip_bin = ip_change(bin_message)
    #bin_key = input_key_judge(str2bin(key))
    key_lst = gen_key(bin_key)
    mes_left = mes_ip_bin[0:32]
    mes_right = mes_ip_bin[32:]
    for i in range(0,15):
        mes_tmp = mes_right
        f_result = fun_f(mes_tmp,key_lst[i])
        mes_right = str_xor(f_result,mes_left)
        mes_left = mes_tmp
    f_result = fun_f(mes_right,key_lst[15])
    mes_fin_left = str_xor(mes_left,f_result)
    mes_fin_right = mes_right
    fin_message = ip_re_change(mes_fin_left + mes_fin_right)
    return fin_message

##64位二进制解密的测试,注意秘钥反过来了，不要写错了
def des_decrypt_one(bin_mess,bin_key):
    mes_ip_bin = ip_change(bin_mess)
    #bin_key = input_key_judge(str2bin(key))
    key_lst = gen_key(bin_key)
    lst = range(1,16)
    cipher_left = mes_ip_bin[0:32]
    cipher_right = mes_ip_bin[32:]
    for i in lst[::-1]:
        mes_tmp = cipher_right
        cipher_right = str_xor(cipher_left,fun_f(cipher_right,key_lst[i]))
        cipher_left = mes_tmp
    fin_left = str_xor(cipher_left,fun_f(cipher_right,key_lst[0]))
    fin_right = cipher_right
    fin_output  = fin_left + fin_right
    bin_plain = ip_re_change(fin_output)
    res = bin2str(bin_plain)
    return res


#简单判断以及处理信息分组
def deal_mess(bin_mess):
    """
    :param bin_mess: 二进制的信息流
    :return: 补充的64位信息流
    """
    ans = len(bin_mess)
    if ans % 64 != 0:
        for i in range( 64 - (ans%64)):           #不够64位补充0
            bin_mess += '0'
    return bin_mess


#查看秘钥是否为64位
def input_key_judge(bin_key):
    """
    全部秘钥以补0的方式实现长度不满足64位的
    :param bin_key:
    """
    ans = len(bin_key)
    if len(bin_key) < 64:
        if ans % 64 != 0:
            for i in range(64 - (ans % 64)):  # 不够64位补充0
                bin_key += '0'
    # else:
    #     bin_key = bin_key[0:64]    #秘钥超过64位的情况默认就是应该跟密文一样长 直接将密钥变为跟明文一样的长度，虽然安全性会有所下降
    return bin_key


def all_message_encrypt(message,key):
        bin_mess = deal_mess(str2bin(message))
        res = ""
        bin_key = input_key_judge(str2bin(key))
        tmp = re.findall(r'.{64}',bin_mess)
        for i in tmp:
            res += des_encrypt_one(i,bin_key)
        return res



def all_message_decrypt(message,key):
    bin_mess = deal_mess(str2bin(message))
    res = ""
    bin_key = input_key_judge(str2bin(key))
    tmp = re.findall(r'.{64}',bin_mess)
    for i in tmp:
        res += des_decrypt_one(i,bin_key)
    return res


def get_mode():
    print("1.加密")
    print("2.解密")
    mode = input()
    if mode == '1':
        print("请输入信息输入字符串不能为空：")
        message = input().replace(' ','')
        print("请输入你的秘钥：")
        key = input().replace(' ','')
        s = all_message_encrypt(message,key)
        out_mess = bin2str(s)
        print("加密过后的内容:"+ out_mess)
        write_in_file(out_mess)
        print(key)

        #print(type(out_mess))
        # base_out_mess = base64.b64encode(out_mess.encode('utf-8'))
        # print("Base64编码过后:"+ base_out_mess.decode())
    elif mode == '2':
        # print("请输入信息输入字符串不能为空：")
        # message = input().replace(' ', '')
        print("请输入你的秘钥：")
        key = input().replace(' ', '')
        message = read_out_file()
        s = all_message_decrypt(message, key)
        #out_mess = bin2str(s)
        print("解密后的信息："+ s)

    else:
        print("请重新输入！")

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):


        self.btn1 = QPushButton("加密", self)
        self.btn1.clicked.connect(self.initUI)
        self.btn1.move(30, 50)

        self.btn2 = QPushButton("解密", self)
        self.btn2.clicked.connect(self.initUI)
        self.btn2.move(150, 50)

        self.btn3 = QPushButton('message', self)
        self.btn3.move(200, 200)
        self.btn3.clicked.connect(self.showDialog1)
        self.le = QLineEdit(self)
        self.le.move(300, 200)

        self.btn4 = QPushButton('key', self)
        self.btn4.move(200, 300)
        self.btn4.clicked.connect(self.showDialog2)
        self.le1= QLineEdit(self)
        self.le1.move(300, 300)

        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(300, 400)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Quit button')
        self.show()


        self.btn1.clicked.connect(self.buttonClicked)
        self.btn2.clicked.connect(self.buttonClicked)

        self.statusBar()

        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle('操作界面')
        self.show()










    def showDialog1(self):
        global message
        text, ok = QInputDialog.getText(self, 'message','message:')


        self.le.setText(str(text))
        message=text
        print(message)

    def showDialog2(self):

        text, ok = QInputDialog.getText(self, 'key','key:')

        global key
        self.le1.setText(str(text))
        key=text
        print(key)

    def buttonClicked(self):

        sender = self.sender()
        if(sender.text()=="加密"):
            s = all_message_encrypt(message,key)
            out_mess = bin2str(s)
            print("加密过后的内容:" + out_mess)
            write_in_file(out_mess)
        elif(sender.text()=="解密"):
            s = all_message_decrypt(message,key)
            # out_mess = bin2str(s)
            print("解密后的信息：" + s)

        else:
            print("出现错误")

        self.statusBar().showMessage(sender.text() + '选择成功')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

#message=10
#key=des12345
