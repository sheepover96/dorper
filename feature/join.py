import pickle
import numpy as np


class Join:
    feature_name = 'join'

    def __init__(self, id_list=None, group_features_dic_list=None, single_feature_dic_list=None):
        self.id_list = id_list
        self.group_features_dic_list = group_features_dic_list
        self.single_features_dic_list = single_feature_dic_list
        self.feature_dic = {}

    def join_feature(self):
        self.feature_dic = {}
        for _id in self.id_list:
            if self.group_features_dic_list:
                group_feature_list = []
                for group_features_dic in self.group_features_dic_list:
                    feature = None
                    if _id in group_features_dic:
                        feature = group_features_dic[_id]
                    group_feature_list.append(feature)
                if None in group_feature_list:
                    continue
                feature_concatenated = np.stack(group_feature_list, axis=1).reshape(1,-1)

            if self.single_features_dic_list:
                single_feature_list = []
                for single_features_dic in self.single_features_dic_list:
                    feature = None
                    if _id in single_features_dic:
                        feature = single_features_dic[_id]
                    single_feature_list.append(feature)
                if None in single_feature_list:
                    continue
                feature_concatenated = np.concatenate([feature_concatenated, np.array(single_feature_list)])

            if self.group_features_dic_list or self.single_features_dic_list:
                self.feature_dic[_id] = feature_concatenated[0]

    def get_feature_dic(self):
        return self.feature_dic

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
