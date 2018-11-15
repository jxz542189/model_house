#-*- coding:utf-8 -*-
import jieba
#jieba.load_userdict("./cu.txt")
dic=['换个地方','园小园','没问题','小豆芽']
jieba.load_userdict(dic)
word_list = jieba.cut("今天去远足吗？要不咱们换个地方吧！园小园怎么样?没问题小豆芽")
print ("|".join(word_list))


