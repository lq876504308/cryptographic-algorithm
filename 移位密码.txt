import string
text=""
letter_index_table = []
letter_table = []

symbol_table = []
symbol_index_table = []
letter_dict=dict((key,value) for key,value in zip(letter_index_table,letter_table))
symbol_dict=dict((key,value) for key,value in zip(symbol_index_table,symbol_table))

disposed_letter_text=""


def letter_select(text):

    for i in range(len(text)):
        if(text[i].isalpha()):
            letter_index_table.append(i)
            letter_table.append(text[i])
        else:
            symbol_index_table.append(i)
            symbol_table.append(text[i])

    letter_text="".join(letter_table)
    return letter_text


def symbol_select(text):

    for i in range(len(text)):
        if(text[i].isalpha()):
            letter_index_table.append(i)
            letter_table.append(text[i])
        else:
            symbol_index_table.append(i)
            symbol_table.append(text[i])

    symbol_text="".join(letter_table)
    return symbol_text


def combine():
    combined_text=""
    for i in range(len(text)):
        if(i in letter_index_table):
            combined_text=combined_text+letter_dict[i]
        elif(i in symbol_index_table ):
            combined_text = combined_text+symbol_dict[i]

    return combined_text



plaintext_ = string.ascii_lowercase
ciphertext_ = string.ascii_uppercase
button=input("请决定进行加密1 or 解密2:")

keya=int(input("请输入密钥a"))
keyb=int(input("请输入密钥b"))
while(1):
    if(type(keya)==int and type(keyb)==int):
        break
    else:
        print("密钥设置错误，请都设置成整数:")
        keya = int(input("请输入密钥a"))
        keyb = int(input("请输入密钥b"))


def encryption(plaintext):
    cipherarr = [0 for i in range(len(plaintext))]
    plaintext_list = list(plaintext)

    j = 0
    for plaintext_item in plaintext_list:
        for i in range(len(plaintext_)):
            if plaintext_item == plaintext_[i]:
                ciphertext = (keya*i+keyb)%26
                cipherarr[j] = ciphertext_[ciphertext]
                j = j+1

    cipher = ''.join(cipherarr)
    return cipher


def niyuan():
    for i in range(26):
        if ((i*keya) % 26 == 1):
            return i


keyc=niyuan()

keyd=(-1*keyc*keyb)%26

def decryption(ciphertext):
    plaintext_arr = [0 for i in range(len(ciphertext))]
    cipherlist = list(ciphertext)

    j = 0
    for cipheritem in cipherlist:
        for i in range(len(ciphertext_)):
            if cipheritem == ciphertext_[i]:
                plaintext = (keyc*i+keyd)%26
                plaintext_arr[j] = plaintext_[plaintext]
                j = j+1

    plain = ''.join(plaintext_arr)
    return plain

if(button=='1'):
    plaintext = input('请输入明文：')
    cipher = encryption(plaintext)
    print('密文是:', cipher)
if(button=='2'):

    ciphertext =input('请输入密文：')
    plain = decryption(ciphertext)
    print('明文输出为：', plain)
#请输入密钥5
#请输入密钥2
#请输入明文：shee
#密文是: OLWW