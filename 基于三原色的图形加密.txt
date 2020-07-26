from PIL import Image, ImageDraw
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64, os, sys, math, random, hashlib,time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]

def isPrime(n):
    if n == 2 or n == 3:
        return 1
    if n % 6 != 1 and n % 6 != 5 or n <= 1:
        return 0
    n_sqrt = int(math.sqrt(n))
    for i in range(5, n_sqrt, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return 0
    return 1


def Find_Big_Prime(n):
    for i in range(n, 2, -1):
        if (isPrime(i)):
            return (i)
            break


def dec2bin(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num, rem = divmod(num, 2)
        mid.append(base[rem])
    return ''.join([str(x) for x in mid[::-1]])


def hex2dec(string_num):
    return str(int(string_num.upper(), 16))


def hex2bin(string_num):
    if string_num == '0':
        return '0000'
    else:
        return dec2bin(hex2dec(string_num))


def change_4(b):
    new_b = ''
    for i in range(0, 32):
        new_0 = ''
        if len(hex2bin(b[i])) == 4:
            new_b = new_b + hex2bin(b[i])
            i = i + 1
        else:
            temp = hex2bin(b[i])
            for j in range(0, 4 - len(hex2bin(b[i]))):
                new_0 = '0'
                temp = new_0 + temp
                if (len(temp) == 4):
                    new_b = new_b + temp
                    i = i + 1
                j = j + 1
    return new_b


def judge_prime(n):
    if n < 2: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


# 用辗转相除求最大公因子
def gcd(a, b):
    r = a % b
    while (r != 0):
        a = b
        b = r
        r = a % b
    return b


# 欧拉函数-暴力循环版
def euler(a):
    count = 0
    for i in range(1, a):
        if gcd(a, i) == 1:
            count += 1
    return count


def order(a, n, b):
    #   输出b在mod(a)中的阶
    #   n是mod(a)群的阶
    p = 1
    while (p <= n and (b ** p % a != 1)):
        p += 1
    if p <= n:
        return p
    else:
        return -1


# 求n以内的素数的算术基本定理
def get_n_prime(n):
    prime = [2]
    for i in range(2, n + 1):
        for x in prime:
            if i % x == 0:
                break
        else:
            prime.append(i)
    return prime


# 求任意数原根
def primitive_root(x):
    g = []
    a = get_n_prime(x - 1)
    for i in range(2, x - 1):
        for j in range(0, x - 1):
            p = i * i;
        for k in range(0, len(a)):
            if p / a[k] == 1:
                break
    g.append(k)
    return g


# A，B得到交换计算数后的密钥
def get_key(m, n, e):
    n = bin(int(n))
    n = n.replace('0b', '')
    n = n[::-1]
    a = [1]
    b = [int(e)]
    m = int(m)

    cum = 0
    for i in n:
        if int(i) > 0:
            a.append(a[cum] * b[cum] % m)
        else:
            a.append(a[cum] % m)
        if cum < len(n):
            b.append(b[cum] * b[cum] % m)
            cum = cum + 1

    return (a[cum])


# 得到A和B的计算数
def get_calculation(m, n, e):
    n = bin(int(n))
    n = n.replace('0b', '')
    n = n[::-1]
    a = [1]
    b = [int(e)]
    m = int(m)

    cum = 0
    for i in n:
        if int(i) > 0:
            a.append(a[cum] * b[cum] % m)
        else:
            a.append(a[cum] % m)
        if cum < len(n):
            b.append(b[cum] * b[cum] % m)
            cum = cum + 1

    return (a[cum])


def secure_choosing_DH(t):
    if (t == '1'):  # 1536bit
        # a='''FFFFFFEF FFFFEFFE C9OEDAA2 2168C234 C4C6628B 80DC1CD1
        # 29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
        # EF9519B3 CD3A431B 302BOA6D F25F1437 4FE1356D 6D51C245
        # E485B576 625E7EC6 F44C42E9 A637ED6B OBFF5CB6 F406B7ED
        # EE386BEB 5A899FA5 AE9F24117C4B1FE6 49286651 ECE45B3D
        # C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
        # 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
        # 670C354E 4ABC9804 F1746C08 CA237327 FFFFFFFF FFFFFFFF'''
        a = 15864720269471500066421819624320759754896918315270219474035301005726752607951306989892853823944064739351507258911816100359606806529013488491289801823450615180585072707998794248002947231808608183132078624300709793418024342523302360163283978820634175694878329908185809711839075537594225953284878490356008795379026808555314103436576648768122472417180863877863526905870001270482199327033290542704837805667003695417772390598466162232747707394142277499042530555537441115271229927373932054765285069869793045510885400752024936706473983


    elif t == '2':  # 2048bit
        # a='''FFFFFFFF FFFFFFFE C9OFDAA2 2168C234 C4C6628B 80DC1CD1
        # 29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
        # EF9519B3 CD3A431B 302BOA6D F25F1437 4FE1356D 6D51C245
        # E485B576 625E7EC6 F44C42E9 A637ED6B OBFF5CB6 F406B7ED
        # EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
        # C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
        # 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
        # 670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
        # E39E772C 180E8603 9B2783A2 ECO7A28F B5C55DFO 6F4C52C9
        # DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
        # 15728E5A 8AACAA68 FFFFFFFF FFFFFFFF'''
        a = 257151968747472970634992226157329817121433500859604021211384974006453780501294173343258143801950281261153382940273680386664602600007084137323573179626569375846317953948765748547252816646279212979378740657876457908247608968728267732234786094476301374307306416069308883243040536381178737345262405977617302628800507906510832849336350261987977442693379677867403046386291072809159867901553435538674972685537952140601300025670640512493824457024382863835825560683409816064486693135177102194972895738905725847480068158922533953204494327384146475740909767488124341145798022917286452588229750884517349956829371420392208546895210929578101974699280385274328344973602110869224955208995034333696941205490891249718132735

    elif t == '3':
        # a='''FFFFFFEF FEFFFFFF C9OFDAA2 2168C234 C4C6628B 80DC1CD1
        # 29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
        # EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
        # E485B576 625E7EC6 F44C42E9 A637ED6B OBFF5CB6 F406B7ED
        # EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
        # C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
        # 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
        # 670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
        # E39E772C 180E8603 9B2783A2 EC07A28F B5C55DFO 6F4C52C9
        # DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
        # 15728E5A 8AAAC42D AD33170D 04507A33 A85521AB DF1CBA64
        # ECFB8504 58DBEFOA 8AEA7157 5D060C7D B3970F85 A6E1E4C7
        # ABF5AE8C DB0933D7 1E8C94E0 4A25619D CEE3D226 1AD2EE6B
        # F12FFA06 D98A0864 D8760273 3EC86A64 521F2B18 177B200C
        # BBE11757 7A615D6C 770988C0 BAD946E2 08E24FAO 74E5AB31
        # 43DB5BFC EOFD108E 4B82D120 A93AD2CA FFFFFFFF FFFFFFFF '''
        a = 4427765874552548916718915711087138254237776221956000356423124492926359799431504338782769229976459476194630151214911078404910630628004367848372282996620804998843384778883902451315246059612786254969174196467783060328515774605063105607079801338909871745421921948003124170982035034532632095926101976533699380699608723092597531279636350636634677580839538374171282389311620203694449060957531398172810323505633943896819348910779219914733127722954279287760011996516781345210632956765332034194978425086676512269394080966366811582325505725808741471853866602829493285030180114461625791218629014481140475413035881463424688557133765820728870581465665150570788234815841516269044181082808464972471621461817209551066768197904805748008316107279447592832928362714100094188956191659539672299659522934870219389291519342216107642251711211485487708812759830809574706119760712049836750338302108256632143746782549084813043023997739921257982131849075434562061800266417432454890774274941702476120954786269757683588219298489877796846594477098129841423485373672292123295461167508000841524051967

    elif t == '4':
        # a='''FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
        # 29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
        # EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
        # E485B576 625E7EC6 F44C42E9 A637ED6B OBFF5CB6 F406B7ED
        # EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
        # C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
        # 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
        # 670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
        # E39E772C 180E8603 9B2783A2 ECO7A28F B5C55DFO 6F4C52C9
        # DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
        # 15728E5A 8AAAC42D AD33170D 04507A33 A85521AB DF1CBA64
        # ECFB8504 58DBEFOA 8AEA7157 5D060C7D B3970F85 A6E1E4C7
        # ABF5AE8C DB0933D7 1E8C94E0 4A25619D CEE3D226 1AD2EE6B
        # F12FFA06 D98A0864 D8760273 3EC86A64 521F2B18 177B200C
        # BBE11757 7A615D6C 770988CO BAD946E2 08E24FAO 74E5AB31
        # 43DB5BFC EOFD108E 4B82D120 A9210801 1A723C12 A787E6D7
        # 88719A10 BDBA5B26 99C32718 6AF4E23C 1A946834 B6150BDA
        # 2583E9CA 2AD44CE8 DBBBC2DB 04DE8EF9 2E8EFC14 1FBECAA6
        # 287C5947 4E6BC05D 99B2964F A090C3A2 233BA186 515BE7ED
        # 1F612970 CEE2D7AF B81BDD76 2170481C D0069127 D5B05AA9
        # 93B4EA98 8D8FDDC1 86FFB7DC 90A6C08F 4DF435C9 34063199
        # FFFFFFFF FFFFFEFE'''
        a = 19517285384367914576113091518317284657200455101421404594671310450522081375392212135692103289789620860590522005757928249450086836790832511167583720380705910797659595794833117955042503417554454816612202641733018926610359277544950627295102960960254712856111854470748997337541858405797418805404653205659091955672648825609007293644813454509707711246069326577455774800501799269537193907712831907288060681427099385179894305185917185694769077880188466150693050544375288936050218787462220020930845807846096108468801577729100239183764567765153734078002351779726772198634958723910703489237162471717163722163919056892693738098107187605532921608816482942037275062583257238397350840841139061102961237186261392429870700544560845761342513539828337826406494098047370838142251141485289721055604668817774600300305375320223071735914367085291497138142118680657878678693966004842128912604723884498789110353019946489192753279685056489042782661702901393280883437628031189937771692106928823724680583353462788762660110215763070630722275882157774407788553868164222513688057946674308874030529010548484933882786742106048166801070905269383067439318463901677215600908695181150400215294243322681536514841311681089900407179241824083969739074517856098011121361996909022734944722405201299850466791636324140876529116245462589443762275691129385462747454415711329317052986709254517582692291277841653617349608806920045683138658919932403482912429887883738114196544421630

    return a

def toimg(c,name='./首密.png'):
    #将密文按顺序填充进三原色元组，并转化成对应色填充进图
    l = int(1 + int((len(c) / 3) ** 0.5))
    w = int((len(c) / 3) // l + 1)
    #print(l,w)
    im=Image.new('RGB',(l,w),(0,0,0))#背景设为黑
    dr=ImageDraw.Draw(im)
    for i in range(len(c)//3):
        #print(c[3*i])
        dr.point((i%l,i//l),(c[3*i],c[3*i+1],c[3*i+2]))
    #im.show()
    im.save(name)
    #print('文件目录为',name)

def imgread(name='./首密.png'):
    im=Image.open(name)
    (l,w)=im.size
    #print(l,w)
    c=[]
    for j in range(w):#逐个读取色块信息
        for i in range(l):
            data=im.getpixel((i,j))
            c.append(data[0])
            c.append(data[1])
            c.append(data[2])
    #print(c)
    while c[len(c)-1]==0:
        c.pop()
    while len(c)%48!=0:#还原密文长度
        c.append(0)
    #print(len(c))
    return bytes(c)

class Combo(QComboBox):  # 拖拽框的初始类，可以读取拖拽图片的url，并且储存在text里

    def __init__(self, title, parent):
        super(Combo, self).__init__(parent)
        self.setAcceptDrops(True)
        self.text=''

    def dragEnterEvent(self, e):
        #print(e)
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.text = e.mimeData().text().lstrip('file:///')
        self.addItem(self.text)
        #print(self.text)

    def showtext(self):
        return self.text

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("端到端图像加密系统")
        MainWindow.resize(800, 320)
        MainWindow.setStyleSheet("background-color: rgb(248, 248, 255);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton.setGeometry(QtCore.QRect(140, 40, 93, 28))
        self.pushButton.setGeometry(QtCore.QRect(0, 190, 113, 21))  # 设置好了
        self.pushButton.setStyleSheet("background-color: rgb(119,136,153);""color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.showDialog3)
        self.pushButton.hide()

        # self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton.setGeometry(QtCore.QRect(140, 40, 93, 28))
        # self.pushButton_7.setGeometry(QtCore.QRect(0, 0, 93, 28))  # 设置好了
        # self.pushButton_7.setStyleSheet("background-color: rgb(119,136,153);""color: rgb(255, 255, 255);")
        # self.pushButton_7.setObjectName("pushButton7")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(400, 10, 210, 16))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 56, 120, 30))
        self.label_2.setObjectName("label2")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(300, 26, 500, 245))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("./背景.png"))
        # H:\study comes first\big 2  down\现代密码学\我的懒鬼程序\QTdesigner\u=2947666120,1511358037&fm=26&gp=0.jpg
        self.label_4.setObjectName("label_4")

        self.labe5 = QtWidgets.QLabel(self.centralwidget)
        self.labe5.setGeometry(QtCore.QRect(0, 378, 400, 28))
        self.labe5.setObjectName("label5")  # 如果不能手动设置，那就拖拽！
        self.labe5.hide()

        self.le2 = QLineEdit(self)
        self.le2.setGeometry(QtCore.QRect(113, 190, 113, 21))
        self.le2.hide()  # 第一个横框

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 86, 90, 30))  # 设置好了
        self.pushButton_2.setStyleSheet("background-color: rgb(119,136,153);""color: rgb(255, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.showDialog2)
        self.pushButton_2.hide()

        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(0, 150, 120, 30))  # 设置好了
        self.pushButton_10.setStyleSheet("background-color: rgb(119,136,153);""color: rgb(255, 255, 255);")
        self.pushButton_10.setObjectName("pushButton_2")
        self.pushButton_10.clicked.connect(self.showDialog4)
        self.pushButton_10.hide()

        self.le1 = QLineEdit(self)
        self.le1.setGeometry(QtCore.QRect(90, 86, 210, 30))
        # 第密钥横框
        self.le1.hide()

        self.le3 = QLineEdit(self)
        self.le3.setGeometry(QtCore.QRect(120, 150, 120, 30))
        # 第密钥横框
        self.le3.hide()

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)  ##设置message
        self.pushButton_3.setGeometry(QtCore.QRect(93, 0, 200, 28))
        self.pushButton_3.setStyleSheet("background-color: rgb(119,136,153);""color: rgb(255, 255, 255);")
        self.pushButton_3.setObjectName("pushButton_3")
        # self.pushButton_3.clicked.connect(self.showDialog1)

        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)  ##设置message
        self.pushButton_6.setGeometry(QtCore.QRect(650, 384, 170, 28))
        self.pushButton_6.setStyleSheet("background-color: rgb(119,136,153);""color: rgb(255, 255, 255);")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.hide()
        # self.pushButton_6.clicked.connect(self.showDialog1)

        self.le = QLineEdit(self)
        self.le.setGeometry(QtCore.QRect(93, 356, 800, 28))
        self.le.hide()
        # 第三个横框
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(0, 0, 90, 30))
        self.comboBox.setStyleSheet("background-color: rgb(119,136,153);""color: rgb(255, 255, 255);")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(120, 56, 90, 30))
        self.comboBox_2.setStyleSheet("background-color: rgb(119,136,153);""color: rgb(255, 255, 255);")
        self.comboBox_2.setObjectName("comboBox")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")

        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton.setGeometry(QtCore.QRect(140, 40, 93, 28))
        self.pushButton_9.setGeometry(QtCore.QRect(210, 55, 90, 30))  # 设置好了
        self.pushButton_9.setStyleSheet("background-color: rgb(119,136,153);""color: rgb(255, 255, 255);")
        self.pushButton_9.setObjectName("pushButton9")
        self.pushButton_9.clicked.connect(self.test1)

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(110, 120, 190, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.hide()

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(0, 120, 113, 21))
        self.pushButton_4.setStyleSheet("background-color: rgb(119,136,153);""color: rgb(255, 255, 255);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.hide()
        self.pushButton_4.clicked.connect(self.jisuan)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(0, 240, 90, 30))
        self.pushButton_5.setStyleSheet("\n"
                                        "background-color: rgb(119,136,153);""color: rgb(255, 255, 255);")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.crypt)
        self.pushButton_5.hide()
        # self.pushButton_5.clicked.connect(start)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        edit = QLineEdit()
        edit.setDragEnabled(True)
        self.com = Combo("Button", self)
        self.com.setGeometry(QtCore.QRect(0, 28, 300, 28))

        self.timelabel = QtWidgets.QLabel(self.centralwidget)
        self.timelabel.setGeometry(QtCore.QRect(0, 270, 300, 30))
        self.timelabel.setObjectName("timelabel")
        self.timelabel.hide()



    def retranslateUi(self, MainWindow):  # 按钮对应表~然后可以设置按钮名字
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "端到端图像加密系统"))
        self.label.setText(_translate("project", "欢迎使用端到端图像加解密系统！"))
        self.label_2.setText(_translate("project", "请设置安全强度！"))
        self.labe5.setText(_translate("project", "如果不能手动设置处理对象，请拖拽至右侧下拉框！"))
        self.pushButton.setText(_translate("MainWindow", "设置储存名称"))
        self.pushButton_2.setText(_translate("MainWindow", "点击生成私钥"))
        self.pushButton_3.setText(_translate("MainWindow", "拖拽图片至下方设置处理对象"))
        self.pushButton_6.setText(_translate("MainWindow", "确定处理对象"))
        self.pushButton_9.setText(_translate("MainWindow", "确定"))
        self.pushButton_10.setText(_translate("MainWindow", "设置对方计算数"))
        # self.pushButton_7.setText(_translate("MainWindow", "加密"))
        self.comboBox.setItemText(1, _translate("MainWindow", "解密"))
        self.comboBox.setItemText(0, _translate("MainWindow", "加密"))

        self.comboBox_2.setItemText(3, _translate("MainWindow", "4096 bits"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "3072 bits"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "2048 bits"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "1536 bits"))
        # print(self.comboBox.currentText())
        self.pushButton_4.setText(_translate("MainWindow", "点击生成计算数"))
        #self.pushButton_5.setText(_translate("MainWindow", "查看生成密钥"))
        self.lineEdit.setText(_translate("MainWindow", "这里是你的计算数"))

    def showDialog2(self):  # 设置私钥的弹出框
        self.le1.show()
        self.le1.setText(str(self.XA))
        self.lineEdit.show()
        self.pushButton_4.show()

    def showDialog4(self):  # 设置对方计算数的弹出框~
        text, ok = QInputDialog.getText(self, 'other_key', 'other_key:')
        self.le3.setText(str(text))
        self.le3.show()
        self.YB = int(text)
        self.pushButton.show()

    def showDialog3(self):  # 设置存储地址的弹出框
        text, ok = QInputDialog.getText(self, 'url', '名称:')
        self.le2.setText(str(text))
        self.name = './'+str(text)+'.png'
        #print(url)
        self.le2.show()  # 意思是在填写完弹出框并且确定以后，包含了url的水平框才浮现出来
        self.pushButton_5.show()


    def test(self):  # 点击了绑定了test的按钮之后，pushbutton_2才显现
        self.pushButton_2.show()

    def test1(self):  # 道理差不多
        level=self.comboBox_2.currentText()
        self.p = secure_choosing_DH(str(level[0]))
        self.XA = random.randint(0,self.p - 1)
        self.YA = get_calculation(self.p, self.XA, 2)
        self.pushButton_2.show()
        #self.le1.show()

    def crypt(self):
        _translate = QtCore.QCoreApplication.translate
        choice=self.comboBox.currentText()
        img=self.com.showtext()
        if choice == '加密':
            beg=time.time()
            #print(beg)
            with open(img, 'rb') as im:
                m = list(im.read())  # 读取需要加密的图,由于信息都是由2进制数组成的，即可以转化为一连串的bytes流，故此处将bytes转化为int列表形式
            while len(m) % 48 != 0:
                m.append(0)  # 保证数据为16和3的倍数
            # print(len(m))
            m = bytes(m)  # 加密所需的信息均为bytes形式
            key = get_key(self.p, self.XA, self.YB)
            md5 = hashlib.md5()
            data = str(key)
            md5.update(data.encode('utf-8'))
            k = md5.hexdigest()
            key = []
            for i in range(0, len(k), 2):
                key.append(int(k[i:i + 2], 16))
            key = bytes(key)
            mode = AES.MODE_CBC
            cryptos = AES.new(key, mode, iv = b'qqqqqqqqqqqqqqqq')
            c = list(cryptos.encrypt(m))
            toimg(c,self.name)
            end=time.time()
            #print(end)
            st='加密用时'+str(end-beg)+'秒'
            #print(st)
            self.timelabel.setText(_translate('project',st))
            self.timelabel.show()
        elif choice == '解密':
            beg = time.time()
            key = get_key(self.p, self.XA, self.YB)
            md5 = hashlib.md5()
            data = str(key)
            md5.update(data.encode('utf-8'))
            k = md5.hexdigest()
            key = []
            for i in range(0, len(k), 2):
                key.append(int(k[i:i + 2], 16))
            key = bytes(key)
            m = imgread(img)
            mode = AES.MODE_CBC
            cryptos = AES.new(key, mode, iv = b'qqqqqqqqqqqqqqqq')
            c = cryptos.decrypt(m)
            with open(self.name,'wb') as f:
                f.write(c)
            end = time.time()
            st = '解密用时' + str(end - beg) + '秒'
            # print(st)
            self.timelabel.setText(_translate('project', st))
            self.timelabel.show()
    def jisuan(self):  # 道理差不多
        _translate = QtCore.QCoreApplication.translate
        self.pushButton_5.setText(_translate("MainWindow", self.comboBox.currentText()))
        #self.pushButton_5.show()
        self.lineEdit.setText(str(self.YA))
        self.pushButton_10.show()



class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):  # 必要的类
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    sys.exit(app.exec_())
