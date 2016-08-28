import  collections
import os, sys
from scipy.sparse import csr_matrix
import numpy as np


def LoadSparse(inputfile, verbose=False):
  """Loads a sparse matrix stored as npz file."""
  npzfile = np.load(inputfile)
  mat = csr_matrix((npzfile['data'], npzfile['indices'],
                       npzfile['indptr']),
                      shape=tuple(list(npzfile['shape'])))
  if verbose:
    print 'Loaded sparse matrix from %s of shape %s' % (inputfile,
                                                        mat.shape.__str__())
  return mat

def build_dataset_alighwith_nitish(words, path_uai):
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