from django.db import models


class Menu(models.Model):
    """
    一级菜单
    """
    title = models.CharField(max_length=32, verbose_name='一级标题')
    icon = models.CharField(max_length=64, verbose_name='图标', default='fa-connectdevelop')
    weight = models.IntegerField(default=1,verbose_name='权重')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "菜单表"
        verbose_name_plural = verbose_name


class Permission(models.Model):
    """
    权限表
    有menu_id     二级菜单
    没有menu_id   普通权限

    有parent_id   子权限
    没有parent_id  父权限  二级菜单

    """
    url = models.CharField(max_length=200, verbose_name='权限')
    title = models.CharField(max_length=32, verbose_name='标题')
    name = models.CharField(max_length=32, verbose_name='url的别名',unique=True)
    menu = models.ForeignKey('Menu', blank=True, null=True)
    parent = models.ForeignKey('Permission', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "权限表"
        verbose_name_plural = verbose_name


class Role(models.Model):
    name = models.CharField(max_length=32, verbose_name="角色名")
    permissions = models.ManyToManyField('Permission', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "角色表"
        verbose_name_plural = verbose_name


class User(models.Model):
    # username = models.CharField(max_length=32, verbose_name="用户名")
    # password = models.CharField(max_length=32, verbose_name="密码")
    roles = models.ManyToManyField(Role, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
        abstract = True   # 数据库迁移时 不会生成表  当做基类
