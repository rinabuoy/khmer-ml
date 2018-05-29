"""
    This script aims at reading the articles from the folders    
"""

import os
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from slashml.utils.file_util import FileUtil

class ReadContent(object):
    """"
        This is the main class
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def load_content(self, dname):
        """ Below scripts are to get content from all files in each folders """
        _stemmer = LancasterStemmer()
        _ignore_words = ['?', '$', '-']
        _save_path = os.getcwd()
        _directory_name = FileUtil.join_path(self.kwargs, dname)
        # Directory containing the files
        #path_to_dataset = FileUtil.dataset_path(config, filename)
        _words_all_articles = []
        for folder in os.listdir(_directory_name):
            _words_each_articles = []   # List for storing all words in articles
            for files in os.listdir(_directory_name+'/'+folder):
                if files.endswith(".txt"):
                    _read_text = open(_directory_name+'/'+folder+'/'+files, "rU", encoding="utf-8", errors="surrogateescape")\
                    # Open file for reading
                    _lines = _read_text.read()# Read content from file

                    #import io
                    #_slash_dir = _directory_name+'/'+folder+'/'+files
                    # with io.open(_slash_dir, "r", encoding="utf-8") as my_file:
                    #_lines = my_file.read()

                    # Open file for reading
                    #_lines = _read_text.read()# Read content from file
                    _stop_words = set(stopwords.words('english'))\
                    # Stop words from English language
                    _new_words = [i for i in _lines.lower().split()\
                                    if i not in _stop_words]# Remove stop words
                    _words = [_stemmer.stem(w.lower()) for w in _new_words \
                                if w not in _ignore_words]# Stemming the words
                    _words_each_articles.append(_words)# Adding list to list

            _words_all_articles.append(_words_each_articles)
            os.chdir(_save_path)  # Moving directory to the saved path
        _all_words = self.merge_list_content(_words_all_articles)

        return _words_all_articles, _all_words

    def merge_list_content(self, list_of_list):
        """ This method is for merging list contents in list into one list """
        _all_words = []
        for counter in list_of_list:
            for innercounter in counter:
                _all_words = _all_words + innercounter

        return list(set(_all_words))

if __name__ == "__main__":

    CONFIG = {
        'root': 'D:/ML_text_classification/slash-ml/slashml',
        'model_dataset': 'examples/dataset',
        'dataset': 'db.khmer.json',
        'model': 'data/naive_bayes_model.pickle',
        'mode': 'unicode'
    }

    test = ReadContent(**CONFIG)
    worlds_articles, all_words = test.load_content('data/dataset/text')
    print(worlds_articles)
    print(all_words)