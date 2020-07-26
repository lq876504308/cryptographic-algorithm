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
n = 0
tap1 = 0
back1 = 0
tap2 = 0
back2 = 0
tap3 = 0
back3 = 0

import re
def change_to_64(text,n):
    if(len(text)%n):
        need=n-(len(text)%n)
        text=text+"0"*need
    return text



def lfsr(array_init, t):

    tap = str(bin(int(t)))[2:]
    array_init_bin = str(bin(int(array_init)))[2:]#转化成对应二进制

    array_new = '0' * len(array_init_bin)
    array_new = list(array_new)

    for i in range(len(array_init_bin)):
        j = i + 1
        if (i == (len(array_init_bin) - 1)):
            j = 0
        if (tap[i] == '1'):
            array_new[i] = str(int(array_init_bin[j]) ^ int(array_init_bin[0]))
        else:
            array_new[i] = str(array_init_bin[j])

    array_new = ''.join(array_new)
    return array_new


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):


        self.btn1 = QPushButton("加密", self)
        self.btn1.clicked.connect(self.buttonClicked)
        self.btn1.move(100, 50)



        self.btn3 = QPushButton('message', self)
        self.btn3.move(200, 200)
        self.btn3.clicked.connect(self.showDialog1)
        self.le = QLineEdit(self)
        self.le.move(300, 200)

        self.btn4 = QPushButton('lfsr级数', self)
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

        self.statusBar()

        self.btn5 = QPushButton('lsf1', self)
        self.btn5.move(0,0)
        self.btn5.clicked.connect(self.showDialog5)
        self.btn5.show()

        self.btn6 = QPushButton('lsf2', self)
        self.btn6.move(0, 60)
        self.btn6.clicked.connect(self.showDialog6)
        self.btn6.show()

        self.btn7 = QPushButton('lsf3', self)
        self.btn7.move(0, 120)
        self.btn7.clicked.connect(self.showDialog7)
        self.btn7.show()

        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle('操作界面')
        self.show()








    def showDialog5(self):
        global tap1,back1
        text1, ok = QInputDialog.getText(self, 'lfsr1初始密钥','lfsr1初始密钥:')
        text2, ok = QInputDialog.getText(self, 'lfsr1反馈密钥', 'lfsr1反馈密钥:')
        tap1=int(text1)
        back1=int(text2)
        print(tap1,back1)
    def showDialog6(self):
        global tap2,back2
        text1, ok = QInputDialog.getText(self, 'lfsr2初始密钥','lfsr2初始密钥:')
        text2, ok = QInputDialog.getText(self, 'lfsr2反馈密钥', 'lfsr2反馈密钥:')
        tap2=int(text1)
        back2=int(text2)
        print(tap2,back2)
    def showDialog7(self):
        global tap3,back3
        text1, ok = QInputDialog.getText(self, 'lfsr3初始密钥','lfsr3初始密钥:')
        text2, ok = QInputDialog.getText(self, 'lfsr3反馈密钥', 'lfsr3反馈密钥:')
        tap3=int(text1)
        back3=int(text2)
        print(tap3,back3)
    def showDialog1(self):
        global message
        text, ok = QInputDialog.getText(self, 'message','message:')


        self.le.setText(str(text))
        message=text
        print(message)

    def showDialog2(self):

        text, ok = QInputDialog.getText(self, 'lfsr级数','lfsr级数:')

        global n
        self.le1.setText(str(text))
        n=int(text)
        print(n)

    def buttonClicked(self):
        global n, tap1, back1, tap2, back2, tap3, back3, message
        print(message)
        print(n)
        print(tap1)
        print(back1)
        print(tap2)
        print(back2)
        print(tap3)
        print(back3)
        x1 = lfsr(back1, tap1)
        x2 = lfsr(back2, tap2)
        x3 = lfsr(back3, tap3)
        finalx = ""
        for i in range(n):
            if (x2[i] == "0"):
                finalx = finalx + x3[i]
            else:
                finalx = finalx + x1[i]
        print("geffe生成器的结果是：", finalx)


        plain = ""
        for i in range(len(message)):
            print(plain)
            plain = plain + str(bin(ord(message[i])))
        print(plain)
        plain = re.sub('b', '', plain)
        print("刚刚做完替换", plain)
        plain = change_to_64(plain, n)
        print("n是：", n)
        print("刚刚做完延长", plain)
        turn = int(len(plain)/n)
        result = ""
        for i in range(turn):
            for j in range(n):
                result = result + str(int(finalx[j]) ^ int(plain[i * n + j]))

        print("结果为：", result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


