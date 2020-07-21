# -*- coding: utf-8 -*-
from notion.client import NotionClient
import feedparser   #用于读取 RSS
import config   #导入设置文件
import re  #用于正则表达式筛除 html 代码
import os #用于遍历目录
import linecache #用于读取文本文件

#读取设置
client = config.global_var.client
tableUrl =config.global_var.tableUrl

#读取设置结束

#将内容插入表格
def add_news_into_table(newstitle,newsUrl,newsSource):
    #获取表格信息
    targetCollectionView = client.get_collection_view(tableUrl)
    #添加一列表格,包含内容
    row = targetCollectionView.collection.add_row()
    row.标题 = newstitle
    row.链接 = newsUrl
    row.来源 = newsSource

#去除字符串中的 html 代码
def remove_html(html):
    dr = re.compile(r'<[^>]+>',re.S)
    newsTitle = dr.sub('',html)
    return newsTitle

#读取当前源的历史新闻 
def read_history_news(ruleName):
    ruleCacheFile = "./cache/"+ruleName
    historyUrlList = linecache.getline(ruleCacheFile, 1).replace("\n", "")
    historyUrlList = historyUrlList.split(",")
    historyUrlListGlobal = historyUrlList

    return historyUrlList

#检查当前源的历史新闻是否重复 返回 T 或 F
def check_history_news(historyUrlList,newsUrl):     
    if newsUrl not in historyUrlList:
        historyUrlListGlobal.append(newsUrl)
        return False
    else:
        return True

#检查当前标题是否符合筛选条件 返回 T 或 F
def check_keywords_in_title(newsTitle,keywordsList):
    for keyword in keywordsList:
            if keyword in newsTitle:
                return True
            else:
                return False
                
#将采集过的信息写入缓存
def write_historyUrls_into_file(ruleName,historyUrlList):
    ruleCacheFile = "./cache/"+ruleName
    print(ruleCacheFile)
    print(historyUrlList)
    with open(ruleCacheFile, 'w') as f:    
        historyUrlList = str(historyUrlList)
        historyUrlList = historyUrlList.replace("]", "")
        historyUrlList = historyUrlList.replace("[", "")
        historyUrlList = historyUrlList.replace("\'", "")
        historyUrlList = historyUrlList.replace("\'", "")
        historyUrlList = historyUrlList.replace(" ", "")
        f.write(historyUrlList)

# 限制输出标题最多为90字
def check_title_length(newsTitle):
    if len(newsTitle)>90:
        newsTitle = newsTitle[:90] + "......"
        return newsTitle
    else:
        return newsTitle

#从信息流来源读取rss信息并写入
def read_rss_from_informationFlowSource(ruleName,rssUrl,newsSource,filterStatus,filterKeywords):
    newsSource = newsSource
    newsContent=feedparser.parse(rssUrl)
   
    #
    global historyUrlListGlobal
    historyUrlListGlobal =[]
    #

   #遍历 获取的 rss 信息 列表
    for i in range(len(newsContent.entries)): 

        newsTitle = remove_html(newsContent.entries[i].description)
        newsTitle = check_title_length(newsTitle) 
        newsUrl = newsContent.entries[i].link

    #写入前检测 开始 ==============================================


        #读取当前来源的历史 Url 记录
        historyUrlList = read_history_news(ruleName)
    
        #检查当前 Url 是否重复 
        checkedHistoryBool = check_history_news(historyUrlList,newsUrl)

        if checkedHistoryBool == True :
            print("重复内容跳过")
            continue
        elif checkedHistoryBool == False :
            write_historyUrls_into_file(ruleName,historyUrlListGlobal)
        else:
            print("检查出错")
            
        #检查是否需要筛选
        if filterStatus == "on":

            #开始筛选
            if check_keywords_in_title(newsTitle,filterKeywords):
                pass
            else:
                print("不符合筛选条件跳过")
                continue
            #结束筛选

        elif filterStatus == "off":
            pass 
        else:
            print("筛选设置错误")


    #写入前检测 结束 ==============================================


        print("------分割线------")
        print(newsTitle)
        print(newsUrl)

        #写入
        add_news_into_table(newsTitle,newsUrl,newsSource)
        
#从传统来源读取rss信息并写入
def read_rss_from_traditionalSource(ruleName,rssUrl,newsSource,filterStatus,filterKeywords):
    newsSource = newsSource
    newsContent=feedparser.parse(rssUrl)

    #
    global historyUrlListGlobal
    historyUrlListGlobal =[]
    #


    #遍历 获取的 rss 信息 列表
    for i in range(len(newsContent.entries)): 
 
        newsTitle = remove_html(newsContent.entries[i].title)
        print(newsTitle)
        newsTitle = check_title_length(newsTitle) 
        newsUrl = newsContent.entries[i].link

    #写入前检测 开始 ==============================================


        #读取当前来源的历史 Url 记录
        historyUrlList = read_history_news(ruleName)
    
        #检查当前 Url 是否重复 
        checkedHistoryBool = check_history_news(historyUrlList,newsUrl)

        if checkedHistoryBool == True :
            print("重复内容跳过")
            continue
        elif checkedHistoryBool == False :
            write_historyUrls_into_file(ruleName,historyUrlListGlobal)
        else:
            print("检查出错")
            
        #检查是否需要筛选
        if filterStatus == "on":

            #开始筛选
            if check_keywords_in_title(newsTitle,filterKeywords):
                pass
            else:
                print("不符合筛选条件跳过")
                continue
            #结束筛选

        elif filterStatus == "off":
            pass 
        else:
            print("筛选设置错误")


    #写入前检测 结束 ==============================================


        print("------分割线------")
        print(newsTitle)
        print(newsUrl)

        #写入
        add_news_into_table(newsTitle,newsUrl,newsSource)
       
#读取 RSS 源规则名称地址并输出为列表
def read_all_the_rulefiles_from_files():
    ruleNamesList = os.listdir("./rules/")
    ruleFilesList = [os.path.join("./rules/",file) for file in ruleNamesList]

    #在命令行中输出读取到的规则文件地址
    #仅供测试使用
    print('读取到的规则文件')
    print(ruleFilesList)

    return ruleNamesList,ruleFilesList

#读取规则详细信息
def read_detailed_rule(ruleFile):
    ruleType = linecache.getline(ruleFile, 1).replace("\n", "")
    newsSource = linecache.getline(ruleFile, 2).replace("\n", "")
    rssUrl = linecache.getline(ruleFile, 3).replace("\n", "")
    filterStatus = linecache.getline(ruleFile, 4).replace("\n", "")
    filterKeywords = linecache.getline(ruleFile, 5).replace("\n", "")
    filterKeywords = filterKeywords.split(",")
    return ruleType,newsSource,rssUrl,filterStatus,filterKeywords

    #测试用的代码，姑且先留着
        #print(newsSource)
        #print(rssUrl)
        #print(type(filterKeywords))
        #print(filterKeywords)



#主函数
def main():
    #读取规则名称和规则地址 开始
    ruleBasicInformation = read_all_the_rulefiles_from_files()
    ruleNamesList = ruleBasicInformation[0]
    ruleFilesList = ruleBasicInformation[1]
    #读取规则名称和规则地址 结束

    #开始嵌套循环处理 (我知道这样不好读但是我想偷懒)
    for ruleOrder in range(0,len(ruleNamesList)):
        #逐一读取详细规则信息 开始
        detailedRule = read_detailed_rule(ruleFilesList[ruleOrder])
        ruleName = ruleNamesList[ruleOrder]
        ruleType =  detailedRule[0]
        newsSource = detailedRule[1]
        rssUrl = detailedRule[2]
        filterStatus = detailedRule[3]
        filterKeywords = detailedRule[4]
        #逐一读取详细规则信息 结束

        # 判断规则类型 (此处预计使用 switch 重构)
        if ruleType == "informationFlow":
            read_rss_from_informationFlowSource(ruleName,rssUrl,newsSource,filterStatus,filterKeywords)
        elif ruleType == "traditional":
            read_rss_from_traditionalSource(ruleName,rssUrl,newsSource,filterStatus,filterKeywords)
        else:
            print("规则类型不正确")
            

#测试用函数 无实际意义 随时可删除
#def main1():
    read_rss_from_informationFlowSource('weibo_snqx','https://rssfeed.today/weibo/rss/5611537367','微博','on',["联动"])

main()
