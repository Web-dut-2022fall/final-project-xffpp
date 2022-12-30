#不能修改的内容后面添加禁止图表
#天数相减
import datetime



# print(type(datetime.datetime.now().year))
# print(datetime.datetime.now().month)
# print(datetime.datetime.now().day)
#

name = "2019-9-30 11:40"
       #012345678910
# print (name[0:4])
# print (name[5:7])
# print (name[8:10])
str1 = name.split(' ')	# 用逗号分割str字符串，并保存到列表
str2 = str1[0].split('-')

d1 = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month,datetime.datetime.now().day)#当前日期
d2 = datetime.date(int(str2[0]),int(str2[1]), int(str2[2]))
print((d1 - d2).days)
# print(int(str2[0]))
# print(type(int(str2[0])))
# print(str2[1])
# print(str2[2])