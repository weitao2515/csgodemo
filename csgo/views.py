from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
from lxml import etree
import json
# Create your views here.

header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
@csrf_exempt
def search(request):
    if request.method == 'POST':
        search_name = request.POST.get("search","weitao2515")
    datalist = []
    userlist = []
    userdict = {}
    num = str(1)
    while True:
        url = 'https://www.5ewin.com/api/search/player/{}/16?keywords='.format(num)
        fullurl = url + search_name
        res = requests.get(fullurl, header)
        data = json.loads(res.content.decode('utf-8'))
        if data['success'] == False:
            break
        list_data = data['data']['user']['list']
        if list_data == []:
            break
        datalist += list_data
        num = str(int(num) + 1)
    for i in datalist:
        datadict = {}
        datadict['id'] = i['domain']
        datadict['name'] = i['username']
        datadict['img'] = i['avatar_url']
        userlist.append(datadict)
    userdict['0'] = userlist
    return JsonResponse(userdict)

@csrf_exempt
def match(request):
    if request.method == 'POST':
        id = request.POST.get("id","weitao2515")
    demo_data = []
    demodict = {}
    num = str(1)
    url = 'https://www.5ewin.com/api/data/match_list/{}?yyyy=2019&page='.format(id)
    while True:
        fullurl = url + num
        res = requests.get(fullurl, header)
        data = json.loads(res.content.decode('utf-8'))
        if data['success'] == False:
            break
        list_data = data['data']
        demo_data += list_data
        num = str(int(num) + 1)
        # 先拿个前三页，比赛数据太多频繁爬取容易被网站屏蔽
        if num == '4':
            break
    demodict['0'] = demo_data
    return JsonResponse(demodict)

@csrf_exempt
def demo(request):
    if request.method == 'POST':
        match_code = request.POST.get("match_code","20190805214230679434")
    url = "https://www.5ewin.com/data/match/" + match_code
    res = requests.get(url, header)
    selector = etree.HTML(res.content)
    arr = []
    matchdata = {}
    img = selector.xpath('//*[@class="datas-tb fleft ml30"]//tr[@data-uid]/td[2]/a/img/@src')
    id = selector.xpath('//*[@class="datas-tb fleft ml30"]//tr[@data-uid]/td[2]//span/text()')
    kill = selector.xpath('//*[@class="datas-tb fleft ml30"]//tr[@data-uid]/td[3]/text()')
    task = selector.xpath('//*[@class="datas-tb fleft ml30"]//tr[@data-uid]/td[4]/text()')
    dead = selector.xpath('//*[@class="datas-tb fleft ml30"]//tr[@data-uid]/td[5]/text()')
    headshot = selector.xpath('//*[@class="datas-tb fleft ml30"]//tr[@data-uid]/td[6]/text()')
    firstkill = selector.xpath('//*[@class="datas-tb fleft ml30"]//tr[@data-uid]/td[7]/text()')
    morekill = selector.xpath('//*[@class="datas-tb fleft ml30"]//tr[@data-uid]/td[8]/span/text()')
    clutch = selector.xpath('//*[@class="datas-tb fleft ml30"]//tr[@data-uid]/td[9]/span/text()')
    adr = selector.xpath('//*[@class="datas-tb fleft ml30"]//tr[@data-uid]/td[10]/text()')
    rws = selector.xpath('//*[@class="datas-tb fleft ml30"]//tr[@data-uid]/td[11]/text()')
    rating = selector.xpath('//*[@class="datas-tb fleft ml30"]//tr[@data-uid]/td[12]/span/text()')
    # 处理字符串
    a = selector.xpath('//*[@class="datas-tb fleft ml30"]//tr[@data-uid]/td[13]/text()')
    b = selector.xpath('//*[@class="datas-tb fleft ml30"]//tr[@data-uid]/td[13]/span/text()')
    j = 0
    elo = []
    for i in range(10):
        x = str(a[j]) + str(b[i]) + str(a[j+1])
        elo.append(x)
        j = j + 2
    for k in range(10):
        c = [img[k],id[k],kill[k],task[k],dead[k],headshot[k],firstkill[k],morekill[k],clutch[k],adr[k],rws[k],rating[k],elo[k]]
        arr.append(c)
    matchdata['0'] = arr
    # 半场分数
    score = selector.xpath('//*[@class="score fs60"]/text()')
    score1 = selector.xpath('//*[@class="ctt1-score"]/text()')[0]
    score2 = selector.xpath('//*[@class="ctt0-score"]/text()')[0]
    score.append(score1)
    score.append(score2)
    matchdata['1'] = score
    return JsonResponse(matchdata)