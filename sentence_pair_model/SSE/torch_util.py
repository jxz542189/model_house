from __future__ import division
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
import os
import sys
import math
import config
from numpy import linalg as LA


def pearson(x, y):
    x = np.array(x)
    y = np.array(y)
    x = x - np.mean(x)
    y = y - np.mean(y)
    return x.dot(y) / (LA.norm(x) * LA.norm(y))


def URL_maxF1_eval(predict_result,test_data_label):
    test_data_label=[item>=1 for item in test_data_label]
    counter = 0
    tp = 0.0
    fp = 0.0
    fn = 0.0
    tn = 0.0
    for i, t in enumerate(predict_result):

        if t>0.5:
            guess=True
        else:
            guess=False
        label = test_data_label[i]
        if guess == True and label == False:
            fp += 1.0
        elif guess == False and label == True:
            fn += 1.0
        elif guess == True and label == True:
            tp += 1.0
        elif guess == False and label == False:
            tn += 1.0
        if label == guess:
            counter += 1.0
    try:
        P = tp / (tp + fp)
        R = tp / (tp + fn)
        F = 2 * P * R / (P + R)
    except:
        P=0
        R=0
        F=0

    accuracy=counter/len(predict_result)
    maxF1=0
    P_maxF1=0
    R_maxF1=0
    probs = predict_result
    sortedindex = sorted(range(len(probs)), key=probs.__getitem__)
    sortedindex.reverse()

    truepos=0
    falsepos=0
    for sortedi in sortedindex:
        if test_data_label[sortedi]==True:
            truepos+=1
        elif test_data_label[sortedi]==False:
            falsepos+=1
        precision=0
        if truepos+falsepos>0:
            precision=truepos/(truepos+falsepos)

        recall=truepos/(tp+fn)
        f1=0
        if precision+recall>0:
            f1=2*precision*recall/(precision+recall)
            if f1>maxF1:
                #print probs[sortedi]
                maxF1=f1
                P_maxF1=precision
                R_maxF1=recall
    print("PRECISION: %s, RECALL: %s, max_F1: %s" % (P_maxF1, R_maxF1, maxF1))
    return accuracy, maxF1


def pad(t, length):
    if length == t.size(0):
        return t
    else:
        return torch.cat([t, Variable(t.data.new(length - t.size(0), *t.size()[1:]).zero_())])


def pack_list_sequence(inputs, l):
    batch_list = []
    max_l = max(list(l))
    batch_size = len(inputs)

    for b_i in range(batch_size):
        batch_list.append(pad(inputs[b_i], max_l))
    pack_batch_list = torch.stack(batch_list, dim=1)
    return pack_batch_list


def pack_for_rnn_seq(inputs, lengths):
    _, sorted_indices = lengths.sort()
    r_index = reversed(list(sorted_indices))

    s_inputs_list = []
    lengths_list = []
    reverse_indices = np.zeros(lengths.size(0), dtype=np.int64)

    for j, i in enumerate(r_index):
        s_inputs_list.append(inputs[:, i, :].unsqueeze(1))
        lengths_list.append(lengths[i])
        reverse_indices[i] = j

    reverse_indices = list(reverse_indices)

    s_inputs = torch.cat(s_inputs_list, 1)
    packed_seq = nn.utils.rnn.pack_padded_sequence(s_inputs,
                                                   lengths_list)
    return packed_seq, reverse_indices


def unpack_from_rnn_seq(packed_seq, reverse_indices):
    unpacked_seq, _ = nn.utils.rnn.pad_packed_sequence(packed_seq)
    s_input_list = []

    for i in reverse_indices:
        s_input_list.append(unpacked_seq[:, i, :].unsqueeze(1))
    return torch.cat(s_input_list, 1)


def auto_rnn_bilstm(lstm=nn.LSTM, seqs=None, lengths=None):
    batch_size = seqs.size(1)
    state_shape = lstm.num_layers * 2, batch_size, lstm.hidden_size
    h0 = c0 = Variable(seqs.data.new(*state_shape).zero_())
    packed_pinputs, r_index = pack_for_rnn_seq(seqs, lengths)
    output, (hn, cn) = lstm(packed_pinputs, (h0, c0))
    output = unpack_from_rnn_seq(output, r_index)
    return output


def auto_rnn_bigru(gru=nn.GRU, seqs=None, lengths=None):
    batch_size = seqs.size(1)
    state_shape = gru.num_layers * 2, batch_size, gru.hidden_size
    h0 = Variable(seqs.data.new(*state_shape).zero_())
    packed_pinputs, r_index = pack_for_rnn_seq(seqs, lengths)
    output, hn = gru(packed_pinputs, h0)
    output = unpack_from_rnn_seq(output, r_index)
    return output


def select_last(inputs, lengths, hidden_size):
    batch_size = inputs.size(1)
    batch_out_list = []
    for b in range(batch_size):
        batch_out_list.append(torch.cat((inputs[lengths[b] - 1, b, :hidden_size],inputs[0, b, hidden_size:])))
    out = torch.stack(batch_out_list)
    return out


def max_along_time(inputs, lengths):
    ls = list(lengths)
    b_seq_max_list = []
    for i, l in enumerate(ls):
        seq_i = inputs[:l, i, :]
        seq_i_max, _ = seq_i.max(dim=0)
        seq_i_max = seq_i_max.squeeze()
        b_seq_max_list.append(seq_i_max)
    return torch.stack(b_seq_max_list)
