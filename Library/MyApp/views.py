import datetime
from django.shortcuts import render
from MyApp.models import *
account=""
global_sname=""
def login(request):#登录
    return render(request, 'login.html')
def student_register(request):  # 学生注册
    name = request.POST.get("student_name")  # 获取学生输入的姓名
    id = request.POST.get("student_id")  # 获取学生输入的学号
    major = request.POST.get("student_major")  # 获取学生输入的学院
    email = request.POST.get("student_email")  # 获取学生输入的邮箱
    telephone = request.POST.get("student_telephone")
    password = request.POST.get("student_password")
    result1 = User.objects.filter(account=telephone)  # 在用户表中搜索该用户名的记录
    result2 = Student.objects.filter(student_id=id)  # 在学生表中搜索该学号的记录
    context = {}
    if len(result1) == 1:  # 判断该账户是否存在(即判断是否注册过)，如果后台存在记录，则返回相应的提示语句
        context["info"] = "该账户已注册！！！"
        context["status"] = 0  #零表示注册失败
        return render(request, 'login.html', context=context)
    else:  #该账户是新用户
        if len(result2) == 1:#判断该学号是否有学生已使用
            context["info"] = "该学号已占用！！！"
            context["status"] = 4
            return render(request, 'login.html', context=context)
        else:
            User.objects.create(account=telephone, user_password=password,user_identity='学生')#用create为user表添加一条记录
            Student.objects.create(student_name=name,student_id=id,student_major=major,student_tel=telephone,student_email=email)#用create为student表添加一条记录
            context["info"] = "注册成功！"
            context["status"] = 1  #1表示注册成功
            return render(request, 'login.html', context=context)
def manager_register(request):  # 管理员注册
    name = request.POST.get("manager_name")  # 获取管理员输入的姓名
    id = request.POST.get("manager_id")  # 获取管理员输入的工号
    stack = request.POST.get("manager_stack")  # 获取管理员输入的书库
    email = request.POST.get("manager_email")  # 获取管理员输入的邮箱
    telephone = request.POST.get("manager_telephone")
    password = request.POST.get("manager_password")
    result1 = User.objects.filter(account=telephone)  # 在用户表中搜索该用户名的记录
    result2 = Manager.objects.filter(manager_id=id)  # 在管理员表中搜索该工号的使用记录
    context = {}
    if len(result1) == 1:  # 判断该账户是否存在(即判断是否注册过)，如果后台存在记录，则返回相应的提示语句
        context["info"] = "该账户已注册！！！"
        context["status"] = 0  #零表示注册失败
        return render(request, 'login.html', context=context)
    else:  #该账户是新用户
        if len(result2) == 1:#判断该工号号是否有管理员已使用
            context["info"] = "该工号已占用！！！"
            context["status"] = 5
            return render(request, 'login.html', context=context)
        else:
            User.objects.create(account=telephone, user_password=password,user_identity='管理员')#用create为user表添加一条记录
            Manager.objects.create(manager_name=name, manager_id=id, manager_stack=stack, manager_tel=telephone,manager_email=email)#用create为manager表添加一条记录
            context["info"] = "注册成功！"
            context["status"] = 1  #1表示注册成功
            return render(request, 'login.html', context=context)
def login_judge(request):#登入判定
    global account ,global_sname,global_mname #定义全局变量account,存储该用户的账户，global_sname保存一下该学生的姓名,global_mname保存一下该学生的姓名
    account = request.POST.get("telephone")#获取前端输入的账户（手机号）
    user_password = request.POST.get("password")
    result1 = User.objects.filter(account=account)#在user表里检索是否存在该账户
    if len(result1) == 1:  # 判断后台是否存在该用户，有则进一步判断密码是否正确
        password = result1[0].user_password  # 获取后台的密码
        identity = result1[0].user_identity  # 获取该账户的身份信息
        if user_password == password:  # 将用户输入的密码和后台密码进行比对,如何正确，判断该账户身份
            if identity == '学生':
                result2 = Student.objects.filter(student_tel=account)
                global_sname = result2[0].student_name  # 用全局变量保存一下该学生的姓名
                context={
                    "name":result2[0].student_name,
                    "id":result2[0].student_id,
                    "major":result2[0].student_major,
                    "telephone":result2[0].student_tel,
                    "email":result2[0].student_email,
                }
                return render(request, 'student/student_information.html',context)  # 跳转到学生主页界面
            else:
                result = Manager.objects.filter(manager_tel=account)  # account为全局变量
                global_mname = result[0].manager_name  # 用全局变量保存一下该管理员的姓名
                context = {
                    "name": result[0].manager_name,
                    "id": result[0].manager_id,
                    "stack": result[0].manager_stack,
                    "telephone": result[0].manager_tel,
                    "email": result[0].manager_email,
                }
                return render(request, 'manager/manager_information.html',context)  # 跳转到管理员主页界面
        else:  # 如果不一致则返回相应提示语句
            context = {
                "info": "密码错误！！！",
                "status": 2
            }
            return render(request, 'login.html', context=context)  # 密码错误回到登入界面
    else:  # 如果不存在该用户则返回相应的提示语句
        context = {
            "info": "该账户不存在！！！",
            "status": 3
        }
        return render(request, 'login.html', context=context)  # 账户不存在则继续回到登入界面
def student_information(request):#个人信息
    if request.method == "GET":  #此部分是当每次点击侧边导航栏的“个人信息”选项时，都重新显示该用户的个人资料
        result = Student.objects.filter(student_tel=account)  #account为全局变量
        context = {
            "name": result[0].student_name,
            "id": result[0].student_id,
            "major": result[0].student_major,
            "telephone": result[0].student_tel,
            "email": result[0].student_email,
        }
        return render(request, 'student/student_information.html', context)#将该用户的个人信息再次传到前端页面
    else:  #在student_information.html页面的第44行中通过post方式的“保存”按钮跳转到此处，即完成更新数据操作（保存）
        email = request.POST.get("email")  # 获取邮箱
        Student.objects.filter(student_tel=account).update(student_email=email)#更新数据
        result = Student.objects.filter(student_tel=account)  # account为全局变量   此处再次传值到前端
        context = {
            "name": result[0].student_name,
            "id": result[0].student_id,
            "major": result[0].student_major,
            "telephone": result[0].student_tel,
            "email": result[0].student_email,
        }
        return render(request, 'student/student_information.html', context)  # 将该用户的个人信息再次传到前端页面
def search_book(request):#查找书籍
    if request.method == "GET":#此部分是当用户每次点击侧边导航栏的“查找书籍”选项时，都要显示出所有书籍资料
        books = Book.objects.all()
        types = Type.objects.all()
        return render(request, 'student/search_book.html',context={"books": books,"types":types,"name":global_sname })  # 向前端传递所有查找到的书籍信息的集合
    else:#student/search_book.html页面的第56行中通过post方式的“搜索”按钮跳转到此处，即完成搜索操作
        book_name = request.POST.get("book_name")
        type_id = request.POST.get("type_id")
        types = Type.objects.all()
        if book_name:#如果书名非空，则按书名查找
            book_result = Book.objects.filter(book_name=book_name)
            if book_result:#如果找到的结果集非空，则输出
                return render(request,'student/search_book.html',context={"books":book_result,"types":types,"name":global_sname})
            else:#若搜索的结果集为0，那么输出未找到该本书！
                book_result = Book.objects.all()
                return render(request, 'student/search_book.html',context={"books": book_result, "types": types, "name": global_sname, "status": 0})
        else:
            if type_id:#如果获取的类型输入框内容不为空，则按类型查找
                book_result = Book.objects.filter(book_type=type_id)
                if book_result:#如果找到的结果集非空，则输出
                    return render(request, 'student/search_book.html', context={"books": book_result,"types":types,"name":global_sname})
                else:#若搜索的结果集为0，那么输出未找到类型的书！
                    book_result = Book.objects.all()
                    return render(request, 'student/search_book.html',context={"books": book_result, "types": types, "name": global_sname,"status":1})
            else:#都为空，则显示空列表
                return render(request, 'student/search_book.html')
def borrow_book(request):
    book_ISBN = request.GET.get("book_ISBN")
    result = Book.objects.filter(ISBN=book_ISBN).first()
    books = Book.objects.all()
    types = Type.objects.all()
    if result.book_rest:#如果可借数不为0，则进行book_rest--
        rest = result.book_rest-1
        Book.objects.filter(ISBN=book_ISBN).update(book_rest=rest)
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")#获取当前借书的系统时间
        student = Student.objects.filter(student_tel=account).first()
        Borrow.objects.create(student_id=student.student_id,student_name=student.student_name,student_tel=account,book_id=book_ISBN,book_name=result.book_name,borrow_time=now_time,rest_time=60)
        return render(request, 'student/search_book.html',context={"books": books, "types": types, "name": global_sname})  # 向前端传递所有查找到的书籍信息的集合
    else:#可借数为0，则不予借出
        return render(request, 'student/search_book.html',context={"books": books, "types": types, "name": global_sname})  # 向前端传递所有查找到的书籍信息的集合
def borrow_record(request):#借书记录
    if request.method == "GET":
        records = Borrow.objects.filter(student_tel=account)#把当前用户的借阅记录搜索出来
        #计算剩余天数
        for record in records:
            borrow_t = record.borrow_time  #获取借阅时间如：2019-11-1 11:40
            print(borrow_t)
            str1 = borrow_t.split(' ')  # 先用空格分割该时间字符串，并保存到列表，str1[0]='2019-11-1' ,str1[1]='11:40'
            str2 = str1[0].split('-')  #再讲时间按'-'分割开，得到str2,str2[0]='2019',str2[1]='11',str2[2]='1'
            borrow_time = datetime.date(int(str2[0]), int(str2[1]), int(str2[2]))#利用date函数得到相对应的借阅时间
            now_time = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month,
                               datetime.datetime.now().day)  # 获取当前日期
            rest_day = 60 - (now_time - borrow_time).days  #最多借阅60天
            print(rest_day)
            if rest_day>=0:
                Borrow.objects.filter(borrow_time = record.borrow_time).update(rest_time = rest_day)
            else:
                Borrow.objects.filter(borrow_time = record.borrow_time).update(rest_time = 0)
        return render(request,'student/borrow_record.html',context={"records":records,"name":global_sname})
def return_book(request):#还书操作，在borrow_record.html页面中点击还书按钮后跳转到此处
    borrow_id = request.GET.get("borrow_id")
    result1 = Borrow.objects.filter(id = borrow_id).first()
    result2 = Book.objects.filter(ISBN = result1.book_id).first()
    rest =  result2.book_rest+1 #还书后库存+1
    Book.objects.filter(ISBN = result2.ISBN).update(book_rest = rest)
    Borrow.objects.filter(id=borrow_id).delete()  # 当点击还书按钮后，删除该用户的借阅记录
    records = Borrow.objects.filter(student_tel=account)  # 把当前用户的借阅记录搜索出来
    return render(request, 'student/borrow_record.html', context={"records": records, "name": global_sname})
def change_password(request):#修改密码
    result = User.objects.filter(account=account).first()
    password = result.user_password
    if request.method == "GET": #此部分是当每次点击侧边导航栏的“修改密码”选项时，显示该界面
        return render(request,'student/change_password.html',context={"password":password,"name":global_sname})
    else:#此部分是在change_password.html页面中点击保存按钮时完成修改密码的操作
        oldPassword = request.POST.get("oldPassword")
        newPassword = request.POST.get("newPassword")
        reNewPassword = request.POST.get("reNewPassword")#以下是先判断输入的旧密码是否正确，并且两次输入的密码是否一致且都不为空
        if password == oldPassword and newPassword == reNewPassword and newPassword and reNewPassword:
            User.objects.filter(account=account).update(user_password = newPassword)#更新该用户的密码
            password = newPassword
        return render(request, 'student/change_password.html', context={"password": password, "name": global_sname})

#管理员界面
def manager_information(request):#个人信息
    if request.method == "GET":  #此部分是当每次点击侧边导航栏的“个人信息”选项时，都重新显示该管理员的个人资料
        result = Manager.objects.filter(manager_tel=account)  #account为全局变量
        context = {
            "name": result[0].manager_name,
            "id": result[0].manager_id,
            "stack": result[0].manager_stack,
            "telephone": result[0].manager_tel,
            "email": result[0].manager_email,
        }
        return render(request, 'manager/manager_information.html', context)#将该用户的个人信息再次传到前端页面
    else:  #在manager_information.html页面的第44行中通过post方式的“保存”按钮跳转到此处，即完成更新数据操作（保存）
        stack = request.POST.get("stack")  # 获取书库信息
        email = request.POST.get("email")  # 获取邮箱
        Manager.objects.filter(manager_tel=account).update(manager_email=email,manager_stack=stack)#更新数据
        result = Manager.objects.filter(manager_tel=account)  # account为全局变量   此处再次传值到前端
        context = {
            "name": result[0].manager_name,
            "id": result[0].manager_id,
            "stack": result[0].manager_stack,
            "telephone": result[0].manager_tel,
            "email": result[0].manager_email,
        }
        return render(request, 'manager/manager_information.html', context)  # 将该用户的个人信息再次传到前端页面

def manage_book(request):#管理书籍
    if request.method == "GET":  # 此部分是当用户每次点击侧边导航栏的“管理书籍”选项时，都要显示出所有书籍资料
        books = Book.objects.all()
        types = Type.objects.all()
        return render(request, 'manager/manage_book.html',context={"books": books, "types": types, "name": global_mname})  # 向前端传递所有查找到的书籍信息的集合
    else:  # 在manager/manage_bok.html页面中通过post方式的“搜索”按钮跳转到此处，即完成搜索操作
        book_name = request.POST.get("book_name")
        type_id = request.POST.get("type_id")
        types = Type.objects.all()
        if book_name:  # 如果书名非空，则按书名查找
            book_result = Book.objects.filter(book_name=book_name)
            if book_result:  # 如果找到的结果集非空，则输出
                return render(request, 'manager/manage_book.html',context={"books": book_result, "types": types, "name": global_mname})
            else:  # 若搜索的结果集为0，那么输出未找到该本书！
                book_result = Book.objects.all()
                return render(request, 'manager/manage_book.html',
                              context={"books": book_result, "types": types, "name": global_mname, "status": 0})
        else:
            if type_id:  # 如果获取的类型输入框内容不为空，则按类型查找
                book_result = Book.objects.filter(book_type=type_id)
                if book_result:  # 如果找到的结果集非空，则输出
                    return render(request, 'manager/manage_book.html',
                                  context={"books": book_result, "types": types, "name": global_mname})
                else:  # 若搜索的结果集为0，那么输出未找到类型的书！
                    book_result = Book.objects.all()
                    return render(request, 'manager/manage_book.html',
                                  context={"books": book_result, "types": types, "name": global_mname, "status": 1})
            else:  # 都为空，则显示空列表
                return render(request, 'manager/manage_book.html')
def add_book(request):#增加书籍的馆藏数量
    if request.method == "GET":
        ISBN = request.GET.get("book_ISBN1")
        result = Book.objects.filter(ISBN=ISBN).first()
        number = result.book_number+1 #让该书本的馆藏数量和可借数++
        rest = result.book_rest+1
        Book.objects.filter(ISBN=ISBN).update(book_number = number,book_rest = rest)
        books = Book.objects.all()
        types = Type.objects.all()
        return render(request, 'manager/manage_book.html',context={"books": books, "types": types, "name": global_mname})  # 向前端传递所有查找到的书籍信息的集合
def reduce_book(request):#减少书籍的馆藏数量
    if request.method == "GET":
        ISBN = request.GET.get("book_ISBN2")
        result = Book.objects.filter(ISBN=ISBN).first()
        number = result.book_number - 1  #让该书本的馆藏数量和可借数--
        rest = result.book_rest -1
        Book.objects.filter(ISBN=ISBN).update(book_number = number,book_rest = rest)
        books = Book.objects.all()
        types = Type.objects.all()
        return render(request, 'manager/manage_book.html',context={"books": books, "types": types, "name": global_mname})  # 向前端传递所有查找到的书籍信息的集合
def delete_book(request):#清空该书籍
    if request.method == "GET":
        ISBN = request.GET.get("ISBN")
        print(ISBN)
        Book.objects.filter(ISBN = ISBN).delete()#在book表里删除该条记录
        books = Book.objects.all()
        types = Type.objects.all()
        return render(request, 'manager/manage_book.html',context={"books": books, "types": types, "name": global_mname})  # 向前端传递所有查找到的书籍信息的集合
def alter_book(request):#修改书本详情
    types = Type.objects.all()
    if request.method == "GET":#此部分是当用户在manage_book.html页面中点击修改书籍是执行，目的是显示当前书本的信息
        ISBN = request.GET.get("book_ISBN3")
        result = Book.objects.filter(ISBN=ISBN).first()
        context={
            "ISBN": result.ISBN,
            "book_name": result.book_name,
            "book_author": result.book_author,
            "book_publisher": result.book_publisher,
            "book_version": result.book_version,
            "book_price": result.book_price,
            "book_number": result.book_number,
            "book_rest": result.book_rest,
            "book_place": result.book_place,
            "type_name": result.book_type.type_name,
            "name": global_sname,
            "types": types
        }
        return render(request, 'manager/alter_book.html',context)  # 向前端传递该书籍的所有信息
    else:#此部分是当用户在alter_book.html页面中点击保存按钮后重新更新用户修改后的信息
        ISBN = request.POST.get("ISBN")
        book_name = request.POST.get("book_name")
        book_author = request.POST.get("book_author")
        book_publisher = request.POST.get("book_publisher")
        book_version = request.POST.get("book_version")
        book_price = request.POST.get("book_price")
        book_number = request.POST.get("book_number")
        book_rest = request.POST.get("book_rest")
        book_place = request.POST.get("book_place")
        type_name = request.POST.get("type_name")
        if book_number.isdigit() and book_rest.isdigit():  # 判断输入的馆藏数和可借数是否为数字
            type = Type.objects.filter(type_name=type_name).first()  # 书籍类型是外键
            Book.objects.filter(ISBN=ISBN).update( book_name=book_name, book_author=book_author, book_publisher=book_publisher,
                                                   book_version = book_version,
                                                   book_price = book_price, book_number=book_number, book_rest=book_rest,
                                                   book_place = book_place, book_type=type)  # 在book表里更新刚才修改的书本信息
            context = {       #把修改后的内容显示出来
                "ISBN": ISBN,
                "book_name": book_name,
                "book_author": book_author,
                "book_publisher": book_publisher,
                "book_version": book_version,
                "book_price": book_price,
                "book_number": book_number,
                "book_rest": book_rest,
                "book_place": book_place,
                "type_name": type_name,
                "name": global_sname,
                "types": types
            }
            return render(request, 'manager/alter_book.html',context)  # 重新向前端传递该书籍的所有信息
        else:
            result = Book.objects.filter(ISBN=ISBN).first()
            context = {
                "ISBN": result.ISBN,
                "book_name": result.book_name,
                "book_author": result.book_author,
                "book_publisher": result.book_publisher,
                "book_version": result.book_version,
                "book_price": result.book_price,
                "book_number": result.book_number,
                "book_rest": result.book_rest,
                "book_place": result.book_place,
                "type_name": result.book_type.type_name,
                "name": global_sname,
                "types": types
            }
            return render(request, 'manager/alter_book.html', context)  # 向前端传递该书籍的所有信息
def change_manager_password(request):#修改管理员的密码
    result = User.objects.filter(account=account).first()
    password = result.user_password
    if request.method == "GET":#此部分是当每次点击侧边导航栏的“修改密码”选项时，显示该界面
        return render(request,'manager/change_manager_password.html',context={"password":password,"name":global_mname})
    else:#此部分是在change_manager_password.html页面中点击保存按钮时完成修改密码的操作
        oldPassword = request.POST.get("oldPassword")
        newPassword = request.POST.get("newPassword")
        reNewPassword = request.POST.get("reNewPassword")#以下是先判断输入的旧密码是否正确，并且两次输入的密码是否一致且都不为空
        if password == oldPassword and newPassword == reNewPassword and newPassword and reNewPassword:
            User.objects.filter(account=account).update(user_password = newPassword)#更新该用户的密码
            password = newPassword
        return render(request, 'manager/change_manager_password.html', context={"password": password, "name": global_mname})
def add_new_book(request):#添加新书籍
    types = Type.objects.all()
    if request.method == "GET":#此部分是当每次点击侧边导航栏的“采购书籍”选项时，显示该界面
        return render(request, 'manager/add_new_book.html', context={ "name": global_mname,"types":types})
    else:#此部分是在add_new_book.html页面中点击确认按钮后完成的添加书籍操作
        ISBN = request.POST.get("ISBN")#获取用户在前端输入框中的数据
        book_name = request.POST.get("book_name")
        book_author = request.POST.get("book_author")
        book_publisher = request.POST.get("book_publisher")
        book_version = request.POST.get("book_version")
        book_price = request.POST.get("book_price")
        book_number = request.POST.get("book_number")
        book_rest = request.POST.get("book_rest")
        book_place = request.POST.get("book_place")
        type_name = request.POST.get("type_name")
        if book_number.isdigit() and book_rest.isdigit():#判断输入的馆藏数和可借数是否为数字
            type = Type.objects.filter(type_name = type_name).first()#书籍类型是外键
            Book.objects.create(ISBN=ISBN,book_name=book_name,book_author=book_author,book_publisher=book_publisher,book_version=book_version,
                                book_price=book_price,book_number=book_number,book_rest=book_rest,book_place=book_place,book_type=type)#在book表里添加新记录
            return render(request, 'manager/add_new_book.html', context={ "name": global_mname,"types":types})
        else:
            return render(request, 'manager/add_new_book.html', context={ "name": global_mname,"types":types})
