from django.db import models

class User(models.Model):  #用户表
    account=models.CharField(max_length = 20,primary_key=True)#账号
    user_password=models.CharField(max_length = 20)#用户密码
    user_identity=models.CharField(max_length = 20)#用户身份


class Student(models.Model):  #学生信息表
    student_id=models.CharField(max_length = 20,primary_key=True)#学号 主键
    student_name=models.CharField(max_length=20)#姓名
    student_tel=models.CharField(max_length = 20)#电话
    student_major=models.CharField(max_length = 20)#院系
    student_email=models.CharField(max_length = 50)#邮箱


class Manager(models.Model):  #图书管理员信息表
    manager_id=models.CharField(max_length = 20,primary_key=True)#工号 主键
    manager_name=models.CharField(max_length=20)#姓名
    manager_tel=models.CharField(max_length = 20)#电话
    manager_email=models.CharField(max_length = 50)#邮箱
    manager_stack=models.CharField(max_length = 20)#管理书库


class Type(models.Model):#书籍类型表
    type_id= models.CharField(max_length=20,primary_key=True)  # 类型编号，主键
    type_name = models.CharField(max_length=20)  # 类型名称


class Book(models.Model):#书本信息表
    ISBN= models.CharField(max_length = 20,primary_key=True)  # 国际标准书号 主键
    book_name = models.CharField(max_length=20)  # 书名
    book_author = models.CharField(max_length=20)  # 作者
    book_publisher = models.CharField(max_length=20)  # 出版社
    book_version = models.CharField(max_length=20)  # 版本
    book_price = models.CharField(max_length=20)  # 价格
    book_number = models.IntegerField()  # 总库存数(馆藏数）
    book_rest = models.IntegerField()  # 可借数
    book_place = models.CharField(max_length=20)  # 所属书库
    book_type = models.ForeignKey(Type, on_delete=models.CASCADE)#书籍类型


class Borrow(models.Model):#借阅表
    student_id= models.CharField(max_length=20)  # 借书人学号
    student_name = models.CharField(max_length=20)  # 借书人姓名
    student_tel = models.CharField(max_length=20)  # 借书人联系方式
    book_id = models.CharField(max_length=20)  # 书籍编号
    book_name = models.CharField(max_length=20)  # 书名
    borrow_time = models.CharField(max_length=20)  # 借书时间
    rest_time = models.IntegerField()  # 剩余天数


