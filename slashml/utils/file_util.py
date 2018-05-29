"""

"""

import csv
import os
import pickle
import zipfile
import shutil


class FileUtil(object):
    """ File Utilities for read and write file
    """

    @staticmethod
    def read_file(filename, file_extension):
        """ Read file

            return
                dataset as list
        """

        _data_matrix = []
        if file_extension == 'CSV':
            _data_matrix = FileUtil.load_csv(filename)

        return _data_matrix

    @staticmethod
    def load_csv(filename):
        """ Read data from csv file.
        """

        file_obj = open(filename, "rU")
        file_csv = csv.reader(file_obj)
        _dataset = list(file_csv)
        for index, subset in enumerate(_dataset):
            _dataset[index] = [float(x) for x in subset]

        file_obj.close()

        return _dataset

    @staticmethod
    def load_csv_np(filename):
        """ Load data from a text file

        When spaces are used as delimiters, or when no delimiter has been given as input\
        , there should not be any missing data between two fields.
        When the variables are named (either by a flexible dtype or with names\
        , there must not be any header in the file (else a ValueError exception is raised).
        Individual values are not stripped of spaces by default. When using a custom converter
        , make sure the function does remove spaces
        """

        from numpy import genfromtxt

        # Data read from the text file. If usemask is True, this is a masked array.
        _dataset = genfromtxt(filename, delimiter=',')

        return _dataset

    @staticmethod
    def dataset_path(config, filename):
        """ path to file
        """

        path = os.path.join(config['root'], config['model_dataset'], filename)

        return path

    @staticmethod
    def path_to_file(config, dirname, filename):
        """ path to file
        """

        path = os.path.join(config['root'], dirname, filename)

        return path

    @staticmethod
    def join_path(config, dirname):
        """ path to file
        """

        path = os.path.join(config['root'], dirname)

        return path

    @staticmethod
    def save_pickle_dataset(config, pickle_filename, dataset):
        """ The pickle module implements binary protocols
        for serializing and de-serializing a Python object structure.

        """

        path_to_pickle = os.path.join(config['root'], pickle_filename)
        with open(path_to_pickle, 'wb') as handle:
            pickle.dump(dataset, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return True

    @staticmethod
    def save_model(config, model):
        """ The pickle module implements binary protocols
        for serializing and de-serializing a Python object structure.

        """

        #s_model = {'hello': 'world'}
        path_to_pickle = os.path.join(config['root'], config['train_model'])
        try:
            with open(path_to_pickle, 'wb') as handle:
                pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)
        except pickle.PickleError as error:
            raise Exception(error)
        else:
            return True

    @staticmethod
    def load_model(config):
        """ Read .pickle file
        """

        path_to_pickle = os.path.join(config['root'], config['train_model'])
        try:
            with open(path_to_pickle, 'rb') as handle:
                model = pickle.load(handle)
        except pickle.UnpicklingError as error:
            raise Exception(error)
        else:
            return model

    @staticmethod
    def extract_zipfile(path_to_zipefile, dest_path):
        """ Extract zipfile sent from client
        Store temporarily in server
        """

        try:
            with zipfile.ZipFile(path_to_zipefile) as opened_rar:
                opened_rar.extractall(dest_path)
            #opened_rar = zipfile.ZipFile(path_to_zipefile)
        except OSError as error:
            raise Exception(error)
        else:
            return True

    @staticmethod
    def move_file(source, destination):
        """ This function is used to move file from source to destination
        """

        try:
            shutil.move(source, destination)
        except OSError as error:
            print('error %s' % error)
            return False

        return True

    @staticmethod
    def remove_file(path, ignore_errors=False, onerror=None):
        """ Delete an entire directory tree; path must point to a directory \
        (but not a symbolic link to a directory). If ignore_errors is true, errors \
        resulting from failed removals will be ignored; if false or omitted, \
        such errors are handled by calling a handler specified by onerror or, \
        if that is omitted, they raise an exception.
        """

        ## check if a file exists on disk ##
        ## if exists, delete it else show message on screen ##
        if os.path.exists(path):
            if os.path.isfile(path):
                try:
                    os.remove(path)
                except OSError as error:
                    print("Error: %s - %s." % (error.filename, error.strerror))
            else:
                try:
                    shutil.rmtree(path, ignore_errors, onerror)
                except OSError as error:
                    print('error %s' % error)
                    return False
        else:
            print("Sorry, I can not find %s file." % path)
            return False

        return True

if __name__ == "__main__":

    config = {
        'root': '/Users/lion/Documents/py-workspare/slash-ml/slashml',
        'model_dataset': 'data/dataset',
        'dataset': 'db.khmer.json',
        'train_model': 'data/naive_bayes_model.pickle',
        'train_dataset': 'data/train_dataset.pickle',
        'test_dataset': 'data/test_dataset.pickle',
        'text_dir': 'data/dataset/text',
        'archive_dir': 'data/dataset/temp',
        'mode': 'unicode'
    }

    text_file = 'data.zip'
    text_file = '.DS_Store'

    #path_to_zipfile = FileUtil.path_to_file(config, 'data/dataset/text', text_file)
    #path_to_tempdir = FileUtil.path_to_file(config, config['archive_dir'], text_file)
    #is_success = FileUtil.move_file(path_to_zipfile, path_to_tempdir)
    path_to_tempdir = FileUtil.path_to_file(config, config['text_dir'], text_file)
    is_removed = FileUtil.remove_file(path_to_tempdir)

    #csv_filename = 'feature16_13.csv'
    #abspath_file = FileUtil.dataset_path(config_, csv_filename)

    #print('Filename %s' % abspath_file)

    #dataset = FileUtil.read_file(abspath_file, "CSV")
    #print('file csv ', dataset)