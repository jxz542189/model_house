+ tf-estimator-tutorial
+ https://zhuanlan.zhihu.com/p/38421397   解析特殊格式的文本文件，有时候我们的训练数据可能有特殊的格式，比如CVS文件其中某些字段是JSON格式的字符串，我们要把JSON字符串的内容也解析出来，这个时候tf.decode_csv函数就不够用了。
是时候请万能函数tf.py_func上场了，tf.py_func函数能够把一个任意的python函数封装成tensorflow的op，提供了极大的灵活性