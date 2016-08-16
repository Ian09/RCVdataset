import zipfile
import StringIO
from zipfile import ZipFile
from bs4 import BeautifulSoup
from cStringIO import StringIO
import re,string
from nltk import word_tokenize
import os, sys

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
    print "%d Documents In the ZIP"%(cnt)
    return texts



if __name__ == "__main__":

    sys.argv.pop(0)
    cd1_path = sys.argv[0]
    cd2_path = sys.argv[1]
    cd1 = extract_RCV1(cd1_path)
    cd2 = extract_RCV1(cd2_path)

    chunk = ' '.join(cd1+cd2)
    print len(chunk)

    tokens = word_tokenize(unicode(chunk, errors='ignore').lower())
    print len(tokens)
    words1 = filter(lambda x: len(x) < 15, tokens)
    print len(words1)
    words = map(foo, words1)
    print  len(words)

    f = open('RCV.txt', 'w')
    f.write(' '.join(words))
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