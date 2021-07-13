from django.contrib import admin

# Register your models here.
from django.contrib import admin
from blog.models import Blog, Spider


class ContactAdmin(admin.ModelAdmin):
    # 增加内容时，将登陆人的账号存入指定的字段中，models中要预留这个字段，这里是author
    def save_model(self, request, obj, form, change):
        if change:  # 更新操作返回true
            obj.save()
        else:  # 否则是新增
            obj.author = request.user
            obj.save()

    # 设置作者字段只读
    readonly_fields = ("author",)

    # 过滤，只能查看操作登陆人自己创建的内容
    def get_queryset(self, request):
        qs = super(ContactAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('title', 'update_time', 'pub_date', 'author')  # list
    search_fields = ('title', 'content',)  # 如果只有一个值，结尾必须有一个逗号，证明是list或元组
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 5
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-update_time',)
    # list_editable 设置默认可编辑字段,第一个字段不允许编辑
    list_editable = ['pub_date', ]
    # fk_fields 设置显示外键字段
    # fk_fields = ('machine_room_id',)
    date_hierarchy = 'pub_date'


class SpiderAdmin(admin.ModelAdmin):
    list_display = ('date', 'open', 'close', 'height', 'low', 'updownd', 'turnrate', 'count')  # list
    date_hierarchy = 'date'
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20


# Register your models here.
admin.site.register(Blog, ContactAdmin)
admin.site.register(Spider, SpiderAdmin)
# 设置登陆窗口的标题
admin.site.site_header = '屌炸天系统'
# 设置页签标题
admin.site.site_title = '牛逼轰轰'
