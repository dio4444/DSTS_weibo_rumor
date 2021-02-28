import json


def City(province, city):
    if province is 31:
        return 1
    elif province is 11:
        return 1
    elif province is 12:
        return 1
    elif province is 50:
        return 1
    elif province is 81:
        return 1
    elif province is 44:
        if city in [1, 3, 5, 6, 13, 19]:
            return 1
        else:
            return 0
    elif province is 51:
        if city in [1, 3, 5, 7, 13, 15]:
            return 1
        else:
            return 0
    elif province is 32:
        if city in [1, 2, 3, 4, 5, 6, 8, 9, 10]:
            return 1
        else:
            return 0
    elif province is 42:
        if city in [1, 6]:
            return 1
        else:
            return 0
    elif province is 61:
        if city is 1:
            return 1
        else:
            return 0
    elif province is 21:
        if city in [1, 2, 3, 4]:
            return 1
        else:
            return 0
    elif province is 23:
        if city in [1, 2, 6]:
            return 1
        else:
            return 0
    elif province is 37:
        if city in [1, 2, 3, 6, 7, 8, 13]:
            return 1
        else:
            return 0
    elif province is 53:
        if city is 1:
            return 1
        else:
            return 0
    elif province is 33:
        if city in [1, 2, 3, 6, 10]:
            return 1
        else:
            return 0
    elif province is 43:
        if city in [1, 2]:
            return 1
        else:
            return 0
    elif province is 41:
        if city in [1, 3, 13]:
            return 1
        else:
            return 0
    elif province is 22:
        if city in [1, 2]:
            return 1
        else:
            return 0
    elif province is 14:
        if city in [1, 2]:
            return 1
        else:
            return 0
    elif province is 13:
        if city in [1, 2, 3, 4, 6, 7]:
            return 1
        else:
            return 0
    elif province is 36:
        if city in [1, 7]:
            return 1
        else:
            return 0
    elif province is 45:
        if city in [1, 2]:
            return 1
        else:
            return 0
    elif province is 35:
        if city in [1, 2, 5]:
            return 1
        else:
            return 0
    elif province is 34:
        if city in [1, 2, 4]:
            return 1
        else:
            return 0
    elif province is 65:
        if city is 1:
            return 1
        else:
            return 0
    elif province is 52:
        if city in [1, 3]:
            return 1
        else:
            return 0
    elif province is 62:
        if city is 1:
            return 1
        else:
            return 0
    elif province is 15:
        if city in [1, 2]:
            return 1
        else:
            return 0
    elif province is 63:
        if city is 1:
            return 1
        else:
            return 0
    elif province is 46:
        if city is 1:
            return 1
        else:
            return 0
    elif province is 64:
        if city is 1:
            return 1
        else:
            return 0
    else:
        return 0


if __name__ == '__main__':
    with open('4010312877.json', 'r', encoding='UTF-8')as f:
        weibo_centent = f.read()
        weibo_dict = json.loads(weibo_centent)  # 将 JSON 对象转换为 Python 字典
        item = weibo_dict[121]
        # print(type(item['province']),type(item['city']))
        # print(item['province'],item['city'])
        # print(type(City(int(item['province']), int(item['city']))))
        print(item)