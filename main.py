import re
import jieba
import math
from utils.tools import *


if __name__ == "__main__":
    stop_file = 'data/cn_stopwords.txt'
    data_path = 'data/'

    stopwords = stopworks_get(stop_file)  
    corpus = corpus_get(data_path, stopwords)

    freq1 = {}
    freq2 = {}
    freq3 = {}
    c1, c2, c3 = result_to_get(corpus, 'char')  
    length = get_length(corpus, 'char')
    c = entropy_get(length, freq1, freq2, freq3)

    freq1 = {}  
    freq2 = {}
    freq3 = {}
    w1, w2, w3 = result_to_get(corpus, 'word')
    length = get_length(corpus, 'word')
    w = entropy_get(length, freq1, freq2, freq3)
    print(c1, c2, c3, w1, w2, w3)
    print(c, w)

    with open('result.txt', 'w') as f:
        f.write("按照字统计：" + '\n')
        f.write(str(c1) + '\n')
        f.write(str(c2) + '\n')
        f.write(str(c3) + '\n')
        f.write("按照词统计：" + '\n')
        f.write(str(w1) + '\n')
        f.write(str(w2) + '\n')
        f.write(str(w3) + '\n')
        f.write("全文按字统计：" + '\n')
        f.write(str(c) + '\n')
        f.write("全文按词统计：" + '\n')
        f.write(str(w) + '\n')
