import re
import jieba
import math


def stopworks_get(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f.readlines()]
        return stopwords


def corpus_get(path, stopwords):
    with open(path + 'inf.txt', encoding='gbk') as _index:
        _index = _index.readline()
        books = _index.strip().split(',')

    corpus_list = []
    for book in books:
        with open(path + book + '.txt', encoding='gbk', errors='ignore') as f:
            text = f.read()
            corpus = Corpus(book, text, stopwords)
            corpus_list.append(corpus)

    return corpus_list


def result_to_get(corpus, mode='char'):
    result1 = []
    result2 = []
    result3 = []
    for book in corpus:
        entropy_c1, entropy_c2, entropy_c3 = book.get_entropy(mode)
        result1.append(entropy_c1)
        result2.append(entropy_c2)
        result3.append(entropy_c3)
    return r1, r2, r3


def dict_sum(a, b):
    temp = dict()
    for key in a.keys() | b.keys():
        temp[key] = sum([d.get(key, 0) for d in (a, b)])
    return temp


def entropy_get(length, freq_dic_1, freq_dic_2, freq_dic_3):
    # 1-gram
    entropy_1 = []
    for word in freq_dic_1.keys():
        freq = freq_dic_1[word]
        entropy_1.append(-(freq / length) * math.log2(freq / length))
    entropy_1 = round(sum(entropy_1), 5)

    # 2-gram
    entropy_2 = []
    length -= 1
    for word in freq_dic_2.keys():
        freq_xy = freq_dic_2[word] / length  # 联合概率
        freq_x_y = freq_dic_2[word] / freq_dic_1[word[0]]  # 条件概率
        entropy_2.append(-freq_xy * math.log2(freq_x_y))
    entropy_2 = round(sum(entropy_2), 5)

    # 3-gram
    entropy_3 = []
    length -= 1
    for word in freq_dic_3.keys():
        freq_xyz = freq_dic_3[word] / length  # 联合概率
        freq_x_yz = freq_dic_3[word] / freq_dic_2[word[0:-1]]  # 条件概率
        entropy_3.append(-freq_xyz * math.log2(freq_x_yz))
    entropy_3 = round(sum(entropy_3), 5)
    return entropy_1, entropy_2, entropy_3


def get_length(corpus, mode='char'):
    length = 0
    for book in corpus:
        if mode == 'char':
            length += len(book.text)
        elif mode == 'word':
            length += len(book.words)
        else:
            raise ValueError('错误！')
    return length


class Corpus:
    def __init__(self, name, text, stopwords):
        self.name = name
        self.stopwords = stopwords
        self.text = self.filter(text)
        self.words = self.get_words()

    def filter(self, text):
        return re.sub(u'[\\sa-zA-Z0-9’!"#$%&\'()（）*+,-./:：;<=>?@，。「」★、…【】《》？“”‘‘！[\\]^_`{|}~]+', '', text)

    def get_words(self):
        words = jieba.cut(self.text)
        return [word for word in words if word not in self.stopwords]

    def get_freq(self, n, mode='char'):
        if mode == 'char':
            data = self.text
        elif mode == 'word':
            data = self.words
        else:
            raise ValueError('错误！')
        length = len(data)
        if not (isinstance(n, int) and 0 < n < length):
            raise ValueError('False n in n-gram model')

        freq_dic = {}
        if n == 1:
            for content in data:
                freq_dic[content] = freq_dic.get(content, 0) + 1
        else:
            for i in range(length - (n - 1)):
                n_gram = []
                for j in range(n):
                    n_gram.append(data[i + j])
                n_gram = tuple(n_gram)
                freq_dic[n_gram] = freq_dic.get(n_gram, 0) + 1
        return freq_dic

    def get_entropy(self, mode='char'):
        if mode == 'char':
            length = len(self.text)
        elif mode == 'word':
            length = len(self.words)
        else:
            raise ValueError('错误！')

        global freq1, freq2, freq3
        freq_dic_1 = self.get_freq(1, mode)
        freq_dic_2 = self.get_freq(2, mode)
        freq_dic_3 = self.get_freq(3, mode)
        freq1 = dict_sum(freq1, freq_dic_1)
        freq2 = dict_sum(freq2, freq_dic_2)
        freq3 = dict_sum(freq3, freq_dic_3)
        return entropy_get(length, freq_dic_1, freq_dic_2, freq_dic_3)