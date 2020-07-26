
def lfsr(ai, t):
    array_init = ai  # 255 #多项式
    tap_init = t  # "101110000"#抽头
    tap = tap_init[1:]
    array_init_bin = '{:08b}'.format(array_init)#转化成8位二进制

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

    print("二进制是：",array_new)  # 二进制


    print("十进制是:",int(array_new, 2))  # 十进制
    print("十六进制是：",hex(int(array_new, 2)))  # 十六进制
    with open('test.txt', 'a+') as f:  # 写入txt
        f.write(str(hex(int(array_new, 2))) + '\n')
    return int(array_new, 2)

if __name__=="__main__":
    init = 255
    tap = "101110000"
    for i in range(1):
        init = lfsr(init, tap)