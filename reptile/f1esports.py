from selenium import webdriver

# ----Initialize----
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options,executable_path=r'D:\Users\PC\Downloads\chromedriver')
driver.implicitly_wait(5)

# ----attributes----
telNumber = ""

# ----work zone----
driver.get('https://www.f1esports.cn/login')
driver.find_element_by_css_selector('[placeholder=手机号]').send_keys(telNumber)
driver.find_element_by_class_name('el-button').click()
driver.find_element_by_css_selector('[placeholder=验证码]').send_keys(input('输入验证码 : '))
driver.find_element_by_class_name('login_btn').click()
driver.find_element_by_class_name('view-btn').click()
results = driver.find_elements_by_css_selector('.rank-item,.right-rank-item')
for result in results:
    rank = result.find_element_by_class_name('value').text
    name = result.find_element_by_class_name('nickname').text
    score = result.find_element_by_class_name('score').text
    print("%3s%14s%9s" % (rank,name,score))
input("Press any button to quit.")
driver.quit()