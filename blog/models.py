from django.db import models


# Create your models here.
class Blog(models.Model):
    title = models.CharField(u'标题', max_length=64)
    content = models.TextField(u'内容', default="")
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    pub_date = models.DateField(u'发布时间')
    author = models.CharField(u'作者', max_length=64, default=None)

    # update_time.editable = True
    # 列表中显示的内容
    def __str__(self):
        return "标题:{},字数:{},概要:{}".format(self.title, len(self.content), self.content[:18])


class Spider(models.Model):
    # 自定义主键
    # id = models.CharField(primary_key=True)
    date = models.DateField(u'日期')
    open = models.DecimalField(u'开盘价', max_digits=8, decimal_places=2)
    close = models.DecimalField(u'收盘价', max_digits=8, decimal_places=2)
    height = models.DecimalField(u'最高价', max_digits=8, decimal_places=2)
    low = models.DecimalField(u'最低价', max_digits=8, decimal_places=2)
    updownd = models.DecimalField(u'涨跌幅度', max_digits=8, decimal_places=2)
    turnrate = models.DecimalField(u'换手率', max_digits=8, decimal_places=2)
    count = models.DecimalField(u'总价', max_digits=8, decimal_places=2)
