key=(input("请输入密钥:")+'abcdefghijklmnopqrstuvwxyz').upper().replace("J",'I').replace(" ","")
keylen=len(key)
num=keylen
book={}
while num:
    num-=1
    book[key[num]]=num

book=sorted(zip(book.values(),book.keys()))
array=[]
for i in range(5):
    line=[]
    for j in range(5):
        line.append(book[5*i+j][1])
    array.append(line)

print(array)
button=input("请选择1加密 or 2解密")
if button=="1":
    ciphertext=[]
    plaintext=input("请输入明文:")
    plainlen=len(plaintext)
    for i in range(int(len(plaintext)/2)):
        for onearray in array:
            if(plaintext[i] in onearray and plaintext[i+1] in onearray):
                print()

