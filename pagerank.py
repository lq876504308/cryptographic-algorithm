
import numpy as np

if __name__ == '__main__':
    # 读入有向图，存储边
    f = open('data','r')
    edges = [line.strip('\n').split(' ') for line in f] #将读取内容逐行遍历,用空格符分离,统统用一个列表存起来。把首位的换行符全部消掉
    print("这是读入图edge：",edges) #把这个列表打印出来，这是读入的有向边表达
    # 根据边获取节点的集合
    nodes = []
    for edge in edges:
        if edge[0] not in nodes:
            nodes.append(edge[0])
        if edge[1] not in nodes:
            nodes.append(edge[1])
    print("有向图去重节点nodes：",nodes)  #获得一个不重复的节点列表

    N = len(nodes)

    # 将节点符号（字母），映射成阿拉伯数字，便于后面生成A矩阵/S矩阵
    i = 0
    NodeNum = {}  #利用集合特性不重复
    for node in nodes:
        NodeNum[node] = i #用value当计数器
        i += 1
    for edge in edges:
        edge[0] = NodeNum[edge[0]]
        edge[1] = NodeNum[edge[1]]
    print("有向图映射结果edges：",edges)  #将edges进行映射

    # 生成初步的S矩阵
    S = np.zeros([N, N])#先生成一个N行N列的0矩阵
    for edge in edges:
        S[edge[1], edge[0]] = 1
    print("生成初步矩阵S：",S)

    # 计算比例：即一个网页对其他网页的PageRank值的贡献，即进行列的归一化处理
    for j in range(N):
        ColNum = sum(S[:, j])
        for i in range(N):
            S[i, j] /= ColNum
    print("计算比例S：",S)

    # 计算矩阵A
    q = 0.85
    A = q * S + (1 - q) / N * np.ones([N, N])
    print("计算矩阵A",A)

    # 生成初始的PageRank值，记录在result中，result和result1均用于迭代
    result = np.ones(N) / N  #最终结果
    result1 = np.zeros(N)  #迭代工具人

    e = 100000  # 误差初始化
    k = 0  # 记录迭代次数
    print('loop...')

    while e > 0.00000001:  # 开始迭代
        result1 = np.dot(A, result)  # 迭代公式
        e = result1 - result
        e = max(map(abs, e))  # 计算误差
        result = result1
        k += 1
        print('Iteration %s:' % str(k), result1)

    print('FinalResult:', result)
