from django.db import models

# Create your models here.


class UserProfile(models.Model):

    gender = (
        ('male', '男'),
        ('female', '女')
    )

    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        # 元数据里定义用户按创建时间的反序排列，也就是最近的最先显示
        ordering = ['-c_time']
        verbose_name = "管理员信息表"
        verbose_name_plural = verbose_name


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('UserProfile', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + self.code

    class Meta:
        ordering = ['-c_time']
        verbose_name = '邮箱确认码'
        verbose_name_plural = verbose_name



