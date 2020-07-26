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



button=input("请选择解密1 or 加密2：")
while True:
    key=input("输入密钥：").split(" ")
    key2=[str(i) for i in key]
    key3=''.join(key2)
    if(key3.isnumeric()==1):
        print("密钥设置成功")
        break
    else:
        print("密钥设置错误，请重新设置：")


keylen=len(key)
m=input("输入text对象:").upper()
mlen=len(m)
if mlen%keylen:
    m+=' '*(keylen-mlen%keylen)
c=list(' '*mlen)
if(button=="2"):
    for i in range(int(mlen/keylen)):
        for j in range(keylen):
            c[i*keylen+int(key[j])-1]=m[i*keylen+int(key[(j+1)%keylen])-1]
    c = ''.join(c)
    print(c)
elif(button=="1"):
    for i in range(int(mlen/keylen)):
        for j in range(keylen):
            c[i*keylen+int(key[(j+1)%keylen])-1]=m[i*keylen+int(key[j])-1].lower()
    c = ''.join(c)
    print(c)
#2
#3 5 1 6 4 2