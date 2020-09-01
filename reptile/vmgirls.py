from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import requests
import os
import time
# from urllib.parse import quote
# import string

#----initialize----
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) #用于排除bluetooth_adapter_winrt.cc:1074 Getting Default Adapter failed
options.add_argument("--headless")
driver = webdriver.Chrome(options=options,executable_path=r'D:\Users\PC\Downloads\chromedriver')
driver.implicitly_wait(10) #隐式sleep,一旦加载完成就会返回find结果
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OSX10_14_2) AppleWebKit/537.36(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
filePath = "D://" #图片存放位置

def getImgs():
    title = driver.title.split()[0]
    dirName = filePath + title + '/'
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    else:
        return
    elements = driver.find_elements_by_css_selector("body .post-content img")
    for e in elements:
        url = e.get_attribute("data-src")      
        url = transform(url)
        fileName = url.split('/')[-1]
        print('Downloading image : %s' % fileName)
        r = requests.get(url,headers=headers)
        with open(dirName + fileName,'wb') as f:
            f.write(r.content)
        time.sleep(1)

def transform(url):
    if ".webp" in url: # 将webp链接转为.jpg/.jpeg...的链接
        fileName = url.split('/')[-1]
        seps = fileName.split('.')
        url = url.replace(fileName,seps[0][1:] + '.' + seps[1])   
    return 'http://vmgirls.com/' + url

def main(): # head=9 | tail=14244
    driver.get('https://www.vmgirls.com/9.html')
    count = 5
    while(count>0):
        try:
            print("Visiting : %s, %d to go..." % (driver.current_url, count))
            time.sleep(1) # 等'下一个'按钮加载完成
            getImgs()
            driver.find_element_by_css_selector('.col-12.col-md-6:nth-child(2) a').click()                   
        except Exception as e:
            print(e)
            return
        count -= 1
    driver.quit()

main()




# sectors = [quote('https://www.vmgirls.com/special/%e8%bd%bb%e7%a7%81%e6%88%bf',safe=string.printable),
#     quote('https://www.vmgirls.com/special/%e5%b0%8f%e5%a7%90%e5%a7%90',safe=string.printable),
#     'https://www.vmgirls.com/photography',
#     'https://www.vmgirls.com/campus',
#     'https://www.vmgirls.com/fresh',
#     'https://www.vmgirls.com/pure',
#     'https://www.vmgirls.com/tag/beauty']
# articles = []
# for sector in sectors:
#     driver.get(sector)
#     aTags = driver.find_elements_by_css_selector('div.row.list-grouped a.text-md')
#     for a in aTags:
#         text,link = a.text,a.get_attribute("href")
#         if (text,link) not in articles:
#             articles.append((text,link))
# for articleInfo in articles:
#     print(articleInfo)