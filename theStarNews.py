from selenium import webdriver
from bs4 import BeautifulSoup
import datetime

url = 'https://klse.i3investor.com/jsp/newshl.jsp'

browser = webdriver.Chrome(executable_path=r"C:\pyhton\webCrawl\chromedriver.exe")
browser.get(url)

innerHTML = browser.execute_script('return document.body.innerHTML')
soup = BeautifulSoup(innerHTML, 'lxml')

date = soup.select('div > h3')

for a in date:
    print(" ")
    print(a.text)
    div = soup.find('h3', text=a.text).find_next_siblings('ul')[0]
    title = div.find_all('a')

    for b in title:
        time_raw = b.find_next_siblings('span', {'class': 'graydate'})[0].text
        time = time_raw[3:].strip()

        insertDate = str(datetime.datetime.now())
        date = a.text
        title = b.text
        author = None
        category = "news"

        print(b.text)
        print(time)

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

browser.quit()