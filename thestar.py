from selenium import webdriver
from lxml import html
import requests
from bs4 import BeautifulSoup
import string


url = 'https://www.thestar.com.my/business/marketwatch/stock-list/?alphabet='

alpha = []
for letter in string.ascii_uppercase:
    alpha.append(letter)

alpha.append('0-9')
# print(alpha)


for i in alpha:
    browser = webdriver.Chrome(executable_path=r"C:\pyhton\webCrawl\chromedriver.exe")
    browser.get(url + i)

    innerHTML = browser.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(innerHTML, 'lxml')

    stock_table = soup.find('table', {'class': 'market-trans'})
    links = stock_table.findAll('a')

    company = []
    for link in links:
        # company.append(print('https://www.thestar.com.my'+link.get('href')))
        start_page = requests.get('https://www.thestar.com.my' + link.get('href'))
        tree = html.fromstring(start_page.text)

        url_link = 'https://www.thestar.com.my' + link.get('href')
        board = tree.xpath('//li[@class="f14"]/text()')[0]
        stock_code = tree.xpath('//li[@class="f14"]/text()')[1]
        week_high52 = tree.xpath('//li[@class="f14"]/text()')[2]
        week_low52 = tree.xpath('//li[@class="f14"]/text()')[3]
        name = tree.xpath('//h1[@class="stock-profile f16"]/text()')[0]
        updateDate = tree.xpath('//span[@id="slcontent_0_ileft_0_datetxt"]/text()')[0]
        updateTime = tree.xpath('//span[@class="time"]/text()')[0]
        open_price = tree.xpath('//td[@id="slcontent_0_ileft_0_lastdonetext"]/text()')[0]
        high_price = tree.xpath('//td[@id="slcontent_0_ileft_0_opentext"]/text()')[0]
        low_price = tree.xpath('//td[@id="slcontent_0_ileft_0_lowtext"]/text()')[0]
        last_price = tree.xpath('//td[@id="slcontent_0_ileft_0_lastdonetext"]/text()')[0]
        change_price_p = tree.xpath('//*[@id="slcontent_0_ileft_0_chgpercenttrext"]/text()')[0]
        vol_00 = tree.xpath('//*[@id="slcontent_0_ileft_0_voltext"]/text()')[0]
        buy_vol_00 = tree.xpath('//*[@id="slcontent_0_ileft_0_buyvol"]/text()')[0]
        sell_vol_00 = tree.xpath('//*[@id="slcontent_0_ileft_0_sellvol"]/text()')[0]


        print(board)
        print(stock_code)
        print(name)
        print(updateDate)
        print(open_price)

        # Insert data into mySQL database

        import mysql.connector

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="abc123",
            database="wqd7005"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO stockdetails (url_link,board,stock_code,week_high52,week_low52,name,date,time,open_price,"\
                "high_price,low_price, last_price,change_price_p,vol_00, buy_vol_00, sell_vol_00) "\
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (
        url_link, board[3:], stock_code[3:], week_high52[3:], week_low52[3:], name, updateDate[10:-2], updateTime,
        open_price, high_price, low_price, last_price, change_price_p, vol_00, buy_vol_00, sell_vol_00)
        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")

browser.quit()






