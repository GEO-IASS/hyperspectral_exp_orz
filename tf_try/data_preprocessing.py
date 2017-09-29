# coding: utf-8
"""Preprocessing original dataset:
    extract single-pixel or 4-neighbors or 8-neighbors sample data sets;
    divide original data set into trian-dataset and test-dataset.
"""

import scipy.io as sio
import numpy as np
from random import shuffle
import tensorflow as tf
import original_cnn as oc

def extract_data(data_file, labels_file, neighbor):
    """The original data will be convert into n-neighbors label with all its bands information(value).
    
    Args:
        data_file: File of the original data
        labels_file: File of the original labels
        neighbor: Three use neighborhood information, 0 - single pixel, 4 - four neighbors, 8 - eight neighbors
        
    Return:
        data_list: Useful data set for build model and test, while the [index + 1] repersent its corresponging label
    """
    
    data = sio.loadmat(data_file)
    label = sio.loadmat(labels_file)
    data_o = data['DataSet']
    labels = label['ClsID']
    classes = np.max(labels)
    print('there are ' + str(classes) + 'class in the data set.')
    rows, cols = labels.shape()
    
    data_list = []
    for mark in range(classes):
        data_list.append([])
    
    for i in range(rows):
        for j in range(cols):
            label = labels[i, j]
            if label != 0:
                data_temp = data_o[i,j]
                if neighbor > 0:
                    center_data = data_temp
                    ##################################
                    #The neighbors-structer:
                    #  data1      data2      data3
                    #  data4   center_data   data5
                    #  data6      data7      data8
                    ##################################
                    data1 = []
                    data2 = []
                    data3 = []
                    data4 = []
                    data5 = []
                    data6 = []
                    data7 = []
                    data8 = []
                    
                    #judgment standard, how to choose neighbors' coordinates
                    lessThan = lambda x : x - 1 if x > 0 else 0
                    greaterThan_row = lambda x : x + 1 if x < rows - 1 else rows - 1
                    greaterThan_col = lambda x : x + 1 if x <cols - 1 else cols - 1
                    
                    if neighbor == 4:
                        data2 = data_o[lessThan(i), j]
                        data4 = data_o[i, lessThan(j)]
                        data5 = data_o[i, greaterThan_col(j)]
                        data7 = data_o[greaterThan_row(i), j]
                        data_1 = np.append(data2, data4)
                        data_2 = np.append(data_1, center_data)
                        data_3 = np.append(data5, data7)
                        data_temp = np.append(data_2, data_3)
                        
                    if neighbor == 8:
                        data1 = data_o[lessThan(i), lessThan(j)]
                        data2 = data_o[lessThan(i), j]
                        data3 = data_o[lessThan(i), greaterThan_col(j)]
                        data4 = data_o[i, lessThan(j)]
                        data5 = data_o[i, greaterThan_col(j)]
                        data6 = data_o[greaterThan_row(i), lessThan(j)]
                        data7 = data_o[greaterThan_row(i), j]
                        data8 = data_o[greaterThan_row(i), greaterThan_col(j)]
                        data_1 = np.append(data1, data2)
                        data_2 = np.append(data3, data4)
                        data_3 = np.append(data_1, data_2)
                        data_4 = np.append(data_3, center_data)
                        data_5 = np.appemd(data5, data6)
                        data_6 = np.append(data7, data8)
                        data_7 = np.append(data_4, data_5)
                        data_temp = np.append(data_7, data_6)
                
                data_list[label - 1].append(data_temp)
                
    return data_list

def onehotlabel(labels):
    """To transfer labels into one-hot values.
    
    Arg:
        labels: Original label set.
    
    Return:
        onehot_labels: One-hot labels to fit in network.
    """
    data_size = tf.size(labels)
    labels = tf.expand_dims(labels, 1)
    indices = tf.expand_dims(tf.range(0, data_size), 1)
    concated = tf.concat(1, [indices, labels])
    onehot_labels = tf.sparse_to_dense(concated, tf.pack([data_size, oc.NUM_CLASSES]), 1.0, 0.0)
    return onehot_labels

def shuffling(data_set):
    """Rewrite the shuffle function.
    
    Args:
         data_set: Original data set, from extract_data().
   
    Return:
         data_set: Shuffled data.
    """
    for eachclass in data_set:
        shuffle(eachlist)
    return data_set
    
def load_data(dataset, ratio):
    """Load percific train data set and test data set according to ratio.
    
    Args：
        dataset: Including data and label, from extract_data()
        ratio: Hundred times of Train data's ratio in the whole data set, real_ratio = ratio / 100
    
    Return:
        train_data: Numpy darray, train data set value
        train_label: Numpy darray, train label
        test_data: Numpy darray, train data set value
        test_label: Numpy darray, test label
    """
    data_num = 0
    for eachclass in dataset:
        data_num += len(eachclass)
    
    #transform int label into one-hot values
    