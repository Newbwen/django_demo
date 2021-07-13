from django.shortcuts import render

# Create your views here.
import base64
from io import BytesIO

import requests
from django.http import JsonResponse
from django.shortcuts import render
import markdown
# Create your views here.

import blog.models as m
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt


# 查询
# models.UserInfo.objects.all()
# models.UserInfo.objects.all().values('user')    #只取user列
# models.UserInfo.objects.all().values_list('id','user')    #取出id和user列，并生成一个列表
# models.UserInfo.objects.get(id=1)
# models.UserInfo.objects.get(user='yangmv')

# 增
# models.UserInfo.objects.create(user='yangmv',pwd='123456')
# 或者
# obj = models.UserInfo(user='yangmv',pwd='123456')
# obj.save()
# 或者
# dic = {'user':'yangmv','pwd':'123456'}
# models.UserInfo.objects.create(**dic)

# 删
# models.UserInfo.objects.filter(id=1).delete()

# 改
# models.UserInfo.objects.filter(user='yangmv').update(pwd='520')
# 或者
# obj = models.UserInfo.objects.get(user='yangmv')
# obj.pwd = '520'
# obj.save()
def index(request):
    i = request.GET.get('id')
    # postdata = request.POST['id']
    blog = m.Blog.objects.get(id=i)
    blog_content = markdown.markdown(blog.content)
    spider = m.Spider.objects.all().values()
    plot_data = showMatplot(pd.DataFrame(spider))
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    return render(request, "blog.html", {'blog': blog, 'blog_content': blog_content, 'img': imd})


def indexes(request):
    blogs = m.Blog.objects.all()
    return render(request, "blogs.html", {'blogs': blogs})


# 图标嵌入django页面
def showMatplot(df):
    plt.figure(figsize=(12, 10))  # 设置图像大小
    plt.subplot(212)  # 布局两行1列的第二个
    col = ['date', 'open', 'close', 'height', 'low', 'updownd', 'count']
    df = df.astype(
        {'open': 'float', 'close': 'float', 'height': 'float', 'low': 'float', 'updownd': 'float', 'count': 'float'})
    df = pd.DataFrame(df, columns=col)
    # print(df)
    # print("*" * 40)
    # # corr只能对数值型数据进行相关度计算
    # print(df.corr())
    x = pd.to_datetime(df['date'])
    y1 = df["open"]
    y2 = df["close"]
    y3 = df["height"]
    y4 = df["low"]

    plt.plot(x, y1, label='open', linestyle='-', c='black', linewidth=1)
    plt.plot(x, y2, label='close', linestyle='--', c='r', linewidth=1)
    plt.plot(x, y3, label='height', linestyle=':', c='g', linewidth=1)
    plt.plot(x, y4, label='low', linestyle='-.', c='b', linewidth=1)
    plt.legend()
    plt.subplot(211)  # 布局两行一列第一个
    df1 = df.sort_values(by='date', ascending=True)
    # df1 = df1.iloc[30:]
    col = ["date", "close"]
    close = pd.DataFrame(df1, columns=col)

    data = cal_macd_system(close, 12, 26, 9)
    x = pd.to_datetime(data['date'])
    # y = pd.to_numeric(data["close"])
    y1 = data["macd"]
    # plt.plot(x, y, label="k")
    plt.plot(x, y1, label="macd")
    plt.title("某公司股票", fontproperties=zhfont1, fontsize=15)
    plt.legend()
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    return plot_data


# 下载字体放到项目目录中，解决图标中文显示
zhfont1 = matplotlib.font_manager.FontProperties(fname="FZSTK.TTF")


# macd指标算法
def cal_macd_system(data, short_, long_, m):
    '''
    data是包含高开低收成交量的标准dataframe
    short_,long_,m分别是macd的三个参数
    返回值是包含原始数据和diff,dea,macd三个列的dataframe
    '''
    data['diff'] = data['close'].ewm(adjust=False, alpha=2 / (short_ + 1), ignore_na=True).mean() - \
                   data['close'].ewm(adjust=False, alpha=2 / (long_ + 1), ignore_na=True).mean()
    data['dea'] = data['diff'].ewm(adjust=False, alpha=2 / (m + 1), ignore_na=True).mean()
    data['macd'] = 2 * (data['diff'] - data['dea'])
    return data


# 绘制macd指标曲线
def macdview(df):
    df1 = df.sort_values(by='date', ascending=True)
    # df1 = df1.iloc[30:]
    col = ["date", "close"]
    close = pd.DataFrame(df1, columns=col)

    data = cal_macd_system(close, 12, 26, 9)
    x = pd.to_datetime(data['date'])
    # y = pd.to_numeric(data["close"])
    y1 = data["macd"]
    # plt.plot(x, y, label="k")
    plt.plot(x, y1, label="macd")
    plt.title("某公司股票", fontproperties=zhfont1, fontsize=15)
    # plt.legend()
    buffer = BytesIO()
    buffer.flush()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    buffer.close()
    return plot_data


# 在线启动爬虫
def start_scrapy(request):
    # 获取页面传参，要区分请求类型是POST还是GET，不同请求用不同的方法接收参数
    year = request.POST.get('year')
    jd = request.POST.get('jd')
    url = 'http://127.0.0.1:6800/schedule.json'
    # spider是执行scrapy list返回的名称,参数问题：除了内置key的参数外如project,spider等，其他参数均由爬虫初始化函数的kwargs接收
    # 同时jobid也有kwargs接收，**kwargs是接收字典型的参数，带有key值的
    data = {'project': 'pachong', 'spider': 'pachong_spider', 'year': year, 'jd': jd}
    print(requests.post(url=url, data=data))
    return JsonResponse({'result': 'ok'})
