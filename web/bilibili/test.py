# -*- coding:utf-8 -*-
# import sys
#
# if len(sys.argv) == 1:
#     sys.argv.append('--help')
# print(sys.argv[1:])
#
# import os
# import re
#
# print(os.path.expanduser('~'))
# print(os.path.join('video', 'a.txt'))
# print(os.path.realpath(os.path.join('video', 'a.txt')))
# print(os.path.isabs('E:\t\r\n\a\b'))
# print(os.path.exists(r'E:\P\p\s\t\r\n\a\b\c'))
# print(os.path.isdir(r'E:\P\p\s\t\r\n\a\b\c'))
#
# path = r'E:\Python\project'
# os .rename(os.path.join(path, '新建.txt'), os.path.join(path, '这是测试.xml'))
#
# def a(path):
#     if not os.path.exists(path):
#         directory = re.sub(r'[|<>"*\?]', '_', path)
#         os.makedirs(directory)
#
#
# a(r'E:\a|A\b>B\c<C\t\n"N\r?R')

# import re
#
#
# class Bili:
#     def __init__(self):
#         self.b = r'Q?W|E>R<T\Y/U:I"P*F'
#
#     def c(self):
#         self.b = re.sub(r'[\\/|<>:"*\?]', '-', self.b)
#         print(self.b)
#
#
# obj = Bili()
# obj.c()
