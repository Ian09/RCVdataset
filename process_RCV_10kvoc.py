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
from Utilities import *

regex_punc = re.compile(r'[%s\n\t]' % re.escape(string.punctuation))
regex_digit = re.compile('[\d]')




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
    path_uai = sys.argv[2]
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

    f = open('RCV_10k.txt', 'w')
    unicode_words = ' '.join(words)
    utf8_words = unicode_words.encode('utf-8')
    f.write(utf8_words)
    f.close()

    data, count, dictionary, reverse_dictionary = build_dataset_with_nitishRCV2(utf8_words.split(), path_uai)
    count_dict = dict(count)
    f = open("RCV1_10k_dict.txt", 'w')
    for k, v in sorted(dictionary.items(), key=lambda (k, v): v):
        if k in count_dict:
            line = "%s\t%d\n" % (k, count_dict[k])
        else:
            line = "%s\t%d\n" % (k, 0)
        f.write(line)
    f.close()



    print 123
