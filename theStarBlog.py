from selenium import webdriver
from bs4 import BeautifulSoup
import datetime

url = 'https://klse.i3investor.com/jsp/blog/bloghl.jsp'

browser = webdriver.Chrome(executable_path=r"C:\pyhton\webCrawl\chromedriver.exe")
browser.get(url)

innerHTML = browser.execute_script('return document.body.innerHTML')
soup = BeautifulSoup(innerHTML, 'lxml')

date = soup.find("div", {"id": "maincontent730"}).find_all('h3')
print(date)

for a in date:
    print(" ")
    # print(a.text)

    data_ul = soup.find('h3', text=a.text).find_next_siblings('ul')[0]
    # print(div)
    data_li = data_ul.select('ul > li')
    # print(title)
    for b in data_li:
        title = b.find('a')
        author = b.find('span', {'class': 'comuid'})
        all_text = b.find('span', {'class': 'graydate'}).text
        child_text = b.find('span', {'class': 'comuid'}).text
        parent_text = all_text.replace(child_text, '')
        time = parent_text[5:].strip()

        print(" ")
        print("Title: "+ title.text)
        print("Author: "+ author.text)
        print(time)

        insertDate = str(datetime.datetime.now())
        date = a.text
        title = title.text
        author = author.text
        category = "blog"
        time = parent_text[5:].strip()

        # Insert data into mySQL database

        import mysql.connector

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="abc123",
            database="wqd7005"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO newsblog (date_crawl, date_publish, time_publish, title, author, category) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (insertDate, date, time, title, author, category)
        mycursor.execute(sql, val)

        mydb.commit()