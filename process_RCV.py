import zipfile
import StringIO
from zipfile import ZipFile
from bs4 import BeautifulSoup
from cStringIO import StringIO
import re,string
from nltk import word_tokenize
import os, sys
import collections
import numpy as np

regex_punc = re.compile(r'[%s\n\t]' % re.escape(string.punctuation))
regex_digit = re.compile('[\d]')


def build_dataset_alighwith_nitish(words):
    #     f_nitish = open("/Users/yin.zheng/ml_datasets/uai2013_data/20news/vocab.txt", 'r')
    f_nitish = open(os.path.join(path_uai, 'reuters', 'vocab_rcv2.txt'), 'r')
    dictionary = {}
    for nitish_word_id, nitish_word in enumerate(f_nitish):
        dictionary[nitish_word.rstrip()] = nitish_word_id
    f_nitish.close()

    count = [['UNK', -1]]
    count.extend([[k, v] for (k, v) in collections.Counter(words).items() if v > 5])
    for w, _ in count:
        if w not in dictionary:
            dictionary[w] = len(dictionary)
    data = list()
    unk_count = 0
    for word in words:
        if word in dictionary:
            index = dictionary[word]
        else:
            index = dictionary['UNK']
            unk_count += 1
        data.append(index)
    count[0][1] = unk_count
    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    sorted_count = sorted(count, key=lambda (x, y): -y)
    return data, sorted_count, dictionary, reverse_dictionary

def foo(x):
    if regex_digit.search(x) is not None:
        return "NUM"
    else:
        return x

def extract_RCV1(input_zip):
    texts = []
    cnt = 0
    with ZipFile(input_zip, 'r') as zf:
        for name in zf.namelist():
            if name.endswith('/'):
                continue
            if len(name) == 21 and name[-3:]=='zip':
                with ZipFile(StringIO(zf.read(name)), 'r') as sub_zf:
                    for sub_name in sub_zf.namelist():
                        if sub_name[-3:] == 'xml':
                            f = sub_zf.open(sub_name, 'r')
                            soup = BeautifulSoup(f, 'xml')
                            text = soup.findAll('text')[0].text
                            textNoPunc = re.sub(regex_punc, ' ', text)
                            texts.append(textNoPunc)
                            cnt += 1
                            if np.mod(cnt, 500) ==0:
                                print cnt
    print "%d Documents In the ZIP"%(cnt)
    return texts



if __name__ == "__main__":

    sys.argv.pop(0)
    cd1_path = sys.argv[0]
    cd2_path = sys.argv[1]
    path_uai = sys.argv[3]
    cd1 = extract_RCV1(cd1_path)
    cd2 = extract_RCV1(cd2_path)

    chunk = ' '.join(cd1+cd2)
    print len(chunk)

    tokens = word_tokenize(chunk.lower())
    print len(tokens)
    words1 = filter(lambda x: len(x) < 15, tokens)
    print len(words1)
    words = map(foo, words1)
    print  len(words)

    f = open('RCV.txt', 'w')
    f.write(' '.join(words))
    f.close()

    data, count, dictionary, reverse_dictionary = build_dataset_alighwith_nitish(words)
    count_dict = dict(count)
    f = open("RCV1_dict.txt", 'w')
    for k, v in sorted(dictionary.items(), key=lambda (k, v): v):
        if k in count_dict:
            line = "%s\t%d\n" % (k, count_dict[k])
        else:
            line = "%s\t%d\n" % (k, 0)
        f.write(line)
    f.close()



    print 123

    # # a = extract_zip("/Users/yin.zheng/Downloads/RCV/rcv1_cd1.zip")
    # input_zip = ZipFile("/Users/yin.zheng/Downloads/RCV/rcv1_cd1.zip", 'r')
    # # a = input_zip.read(input_zip.namelist()[1])
    # # f = input_zip.open(input_zip.namelist()[1])
    # # soup = BeautifulSoup(f, "xml")
    # # text = soup.findAll('text')[0].text
    # # print text
    # # print  123
    #
    # zfiledata = StringIO(input_zip.read(input_zip.namelist()[1]))
    # with ZipFile(zfiledata, 'r') as zfile2:
    #     f = zfile2.open(zfile2.namelist()[1], 'r')
    #     soup = BeautifulSoup(f, "xml")
    # print 123