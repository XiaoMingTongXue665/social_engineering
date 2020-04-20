from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect,reverse
from django.conf import settings
from django.utils import timezone
from login.utils import send_mail


from login.models import UserProfile, ConfirmString
from . import forms
import hashlib
import datetime
import uuid


def hash_code(s, salt = settings.SECRET_KEY): # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode()) # update方法只接收bytes类型
    return h.hexdigest()


# 创建确认码对象的方法
def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    ConfirmString.objects.create(code=code, user=user)
    return code


# /user/login
# 用户登陆视图
def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect(reverse('social:index'))
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = UserProfile.objects.get(username=username)
            except :
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if not user.has_confirmed:
                message = '该用户还未经过邮件确认！'
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                return redirect(reverse('social:index'))
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    # 对于非POST方法发送数据时，比如GET方法请求页面，返回空的表单，让用户可以填入数据
    login_form = forms.UserForm()
    # 这里使用了一个小技巧，Python内置了一个locals()函数，它返回当前所有的本地变量字典，我们可以偷懒的将这作
    # 为render函数的数据字典参数值，就不用费劲去构造一个形如{'message':message, 'login_form':login_form}的字典了。
    return render(request, 'login/login.html', locals())


# /user/register
# 用户注册视图
def register(request):
    if request.session.get('is_login', None):
        return redirect(reverse('social:index'))

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = UserProfile.objects.filter(username=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = UserProfile.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())

                new_user = UserProfile()
                new_user.username = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                a = send_mail(email, code)
                print(a)


                message = '请前往邮箱进行确认！'
                return render(request, 'login/confirm.html', locals())
        else:
            return render(request, 'login/register.html', locals())

    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


# /user/logout
# 用户注销视图
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect(reverse("user:login"))

    # flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患
    request.session.flush()
    # del request.session['is_login']
    return redirect(reverse("user:login"))


# # /user/forget_pwd
# # 忘记密码界面视图
# def forget_password(request):
#     if request.method == 'GET':
#         # 使用CaptchaTestForm渲染页面
#         form = CaptchaTestForm()
#         return render(request, 'user/forget_pwd.html', context={'form': form})
#
#     else:
#         # 获取提交的邮箱，发送邮件，通过发送的邮箱链接设置新的密码
#         email = request.POST.get('email')
#         # 给此邮箱地址发送邮件
#         user = UserProfile.objects.filter(email=email).first()
#         # 使用uuid生成随机值
#         ran_code = uuid.uuid4()
#         ran_code = str(ran_code)
#         ran_code = ran_code.replace('-', '')
#         # 将uuid的随机值保存到session中
#         request.session[ran_code] = user.id
#         viewname = 'update_pwd'
#         result = send_mail(email, viewname, request)
#         return HttpResponse(result)
#
#
# # /user/update_pwd
# # 更新修改密码视图
# def update_pwd(request):
#     if request.method == 'GET':
#         # 获取用户的uuid，就是url后的字符串
#         c = request.GET.get('c')
#         # 跳转到主页面
#         return render(request, 'user/update_pwd.html', context={'c': c})
#     else:
#         # 获取用户提交的uuid
#         code = request.POST.get('code')
#         # 从session取出对应的用户uid
#         uid = request.session.get(code)
#         # 在数据库中取出uid对应的用户
#         user = UserProfile.objects.get(pk=uid)
#
#         # 获取用户提交的密码
#         pwd = request.POST.get('password')
#         repwd = request.POST.get('repassword')
#         if pwd ==repwd:
#             # 将密码加密
#             pwd = hash_code(pwd)
#             # 修改并保存密码
#             user.password = pwd
#             user.save()
#             return render(request, 'user/update_pwd.html', context={'msg':'用户密码更新成功'})
#         else:
#             return render(request, 'user/update_pwd.html', context={'msg':'更新失败'})
#


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''

    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求！'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = timezone.now()
    # now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.username.delete()
        message = '您的邮件已经过期！请重新注册！'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())




