# -*- coding: utf-8 -*-
"""
   作者：	钱艳
   日期：	2018年9月11日
   文件名：	demo.py
   功能：	新词查找入口函数
"""

import xlsxwriter
import config
from data_read import data_read


def result_output(file_read, file_out, sheet1_name, sheet2_name, is_save=config.is_save, N=config.N):
    '''
    新词查找结果写入到excel
    :param file_read: 数据集路径
    :param file_out: 结果输出文件名
    :param sheet1_name: 第一个sheet名字(记录topN新词)
    :param sheet2_name: 第二个sheet名字(记录所有可能的新词)
    :param is_save 树模型模型是否保存
    :param N 定义取TOPN个
    :return:
    '''
    # 加载停用词
    data_read.Load_stopword(config.stopword_path)
    # 加载字典树
    root = data_read.load_dic_tree(config.jieba_dic_path, is_save)
    # 加载数据集
    data = data_read.load_date(file_read)
    if len(data)==0:
        print('数据集为空请查看数据集文件！')
        return 0
    # 插入数据集节点
    root = data_read.insert_node(root, data)
    # 查找新词
    result, add_word ,PMI_min,PMI_max= root.wordFind(N)

    add_word_sort = sorted(add_word.items(), key=lambda x: x[1], reverse=True)
    print('增加了%d个新词, 词语和得分分别为' % len(add_word))
    print('#############################')
    for i in range(len(add_word_sort)):
        print(add_word_sort[i][0] + ' ---->  ', add_word_sort[i][1])
    print('#############################')

    # 写入文件
    # 打开存储文件
    write_file = xlsxwriter.Workbook(file_out)
    excel_sheet1 = write_file.add_worksheet(sheet1_name)
    HW = 0  # 行数标记
    excel_sheet1.write(HW, 0, "新词")  # 新词
    excel_sheet1.write(HW, 1, "得分")  # 得分

    for i in range(len(add_word_sort)):
        HW = HW + 1
        excel_sheet1.write(HW, 0, add_word_sort[i][0])  # 新词
        excel_sheet1.write(HW, 1, add_word_sort[i][1])  # 得分
    # 写所有可能新词及得分到下一页
    excel_sheet2 = write_file.add_worksheet(sheet2_name)
    HW = 0  # 行数标记
    excel_sheet2.write(HW, 0, "新词")  # 新词
    excel_sheet2.write(HW, 1, "得分")  # 得分
    for i in range(len(result)):
        HW = HW + 1
        excel_sheet2.write(HW, 0, result[i][0])  # 新词
        excel_sheet2.write(HW, 1, result[i][1])  # 得分


if __name__ == '__main__':
    # 数据文件txt
    fr = './data/Questioning_HZRQ.txt'
    fo = 'result.xlsx'
    # 保存excel的sheet页名称
    sheet1_name = '新词'
    sheet2_name = '所有二元词词'
    is_save=False
    N=2
    result_output(fr, fo, sheet1_name, sheet2_name,N=N,is_save=is_save)
