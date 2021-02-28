import os

files = os.listdir('./stopwords-master')
with open('Stopword.txt', 'r+', encoding='UTF-8') as f:
    dictionary = []
    for word in f.readlines():
        dictionary.append(word)
    for file in files:
        with open('./stopwords-master/' + file, encoding='UTF-8')as f1:
            for line in f1.readlines():
                if line not in dictionary:
                    f.write(line)
                    dictionary.append(line)

