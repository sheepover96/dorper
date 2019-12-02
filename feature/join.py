import pickle
import numpy as np


class Join:
    feature_name = ''

    def __init__(self, id_list, group_features_dic_list, single_feature_dic_list):
        self.id_list = id_list
        self.group_features_dic_list = group_features_dic_list
        self.single_features_dic_list = single_feature_dic_list
        self.feature_list = []

    def join_feature(self):
        self.feature_list = []
        for _id in self.id_list:
            group_feature_list = []
            for group_features_dic in self.group_features_dic_list:
                group_feature_list.append(group_features_dic[_id])
            feature_flatten = np.stack(group_feature_list, axis=1).reshape(1,-1)

            single_feature_list = []
            for single_features_dic in self.single_features_dic_list:
                single_feature_list.append(single_features_dic[_id])
            feature_concatenated = np.concatenate([feature_flatten, np.array(single_feature_list)])

            self.feature_list.append(feature_concatenated)

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