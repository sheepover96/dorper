import pandas as pd
import numpy as np
import pickle


class BaseFeature():
    feature_name = ''
    feature_type = ''

    def __init__(self, *args, **kwargs):
        pass

    def extract_feature(self):
        pass

    def get_feature(self):
        pass

    def save(self, file_name=None):
        save_file_name = self.feature_name + '.pkl'
        if file_name: save_file_name = file_name

        with open(save_file_name, 'wb') as f:
            pickle.dump(self.__dict__, f)

    def load(self, file_name=None):
        load_file_name = self.feature_name + '.pkl'
        if file_name: load_file_name = file_name
        with open(load_file_name, 'rb') as f:
            tmp_obj = pickle.load(f)
            self.__dict__.update(tmp_obj)

#hogehoge
