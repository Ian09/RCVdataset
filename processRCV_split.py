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
from numpy import linalg as LA

regex_punc = re.compile(r'[%s\n\t]' % re.escape(string.punctuation))
regex_digit = re.compile('[\d]')




def foo(x):
    if regex_digit.search(x) is not None:
        return "NUM"
    else:
        return x

def text_to_hist(text, dictionary):
    count = collections.Counter(text)
    voc_size = len(dictionary)
    hist = np.zeros((voc_size,))
    for word, col_id in dictionary.items():
        if word in count:
            hist[col_id] = count[word]
    return hist


def extract_RCV1_trainset(input_zip, trainset_hist, trainset_hist_norm, dictionary):
    texts = []
    cnt = 0
    cnt_skip = 0
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

                            hist = text_to_hist(word_tokenize(textNoPunc.lower()), dictionary).astype('float32')
                            hist_normed = csr_matrix(hist/(LA.norm(hist, ord=2)+0.001))
                            # import pdb
                            # pdb.set_trace()
                            sim = np.squeeze(hist_normed.dot(trainset_hist.T).toarray())/trainset_hist_norm
                            max_sim = sim.max()
                            # max_id = sim.argmax()
                            # sim = np.dot(hist_normed, trainset_hist.T)

                            if max_sim>0.5:
                                texts.append(textNoPunc)

                                cnt += 1
                                if np.mod(cnt, 500) ==0:
                                    print cnt
                            else:
                                cnt_skip+=1
                                print "max sim is %f, skip! %d docs in, %d docs skipped\n"%(max_sim, cnt, cnt_skip)

    print "%d Documents In the ZIP"%(cnt)
    return texts



if __name__ == "__main__":

    sys.argv.pop(0)
    cd1_path = sys.argv[0]
    cd2_path = sys.argv[1]
    path_uai = sys.argv[2]
    #Load RCV trainset
    trainset_hist = LoadSparse(os.path.join(path_uai, 'reuters', 'train_data.npz')).astype(np.float32)
    trainset_hist_norm = np.squeeze(np.asarray(np.sqrt((trainset_hist.multiply(trainset_hist)).sum(axis=1)+0.0001)))
    f_nitish = open(os.path.join(path_uai, 'reuters', 'vocab_rcv2.txt'), 'r')
    dictionary = {}
    for nitish_word_id, nitish_word in enumerate(f_nitish):
        dictionary[nitish_word.rstrip()] = nitish_word_id
    f_nitish.close()

    cd1 = extract_RCV1_trainset(cd1_path, trainset_hist, trainset_hist_norm, dictionary)
    cd2 = extract_RCV1_trainset(cd2_path, trainset_hist, trainset_hist_norm, dictionary)

    chunk = ' '.join(cd1+cd2)
    print len(chunk)

    tokens = word_tokenize(chunk.lower())
    print len(tokens)
    words1 = filter(lambda x: len(x) < 15, tokens)
    print len(words1)
    words = map(foo, words1)
    print  len(words)

    f = open('RCV_trainset.txt', 'w')
    unicode_words = ' '.join(words)
    utf8_words = unicode_words.encode('utf-8')
    f.write(utf8_words)
    f.close()

    data, count, dictionary, reverse_dictionary = build_dataset_alighwith_nitish(utf8_words.split(), path_uai)
    count_dict = dict(count)
    f = open("RCV1_trainset_dict.txt", 'w')
    for k, v in sorted(dictionary.items(), key=lambda (k, v): v):
        if k in count_dict:
            line = "%s\t%d\n" % (k, count_dict[k])
        else:
            line = "%s\t%d\n" % (k, 0)
        f.write(line)
    f.close()



    print 123
