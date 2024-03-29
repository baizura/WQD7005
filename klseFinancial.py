import mysql.connector
from selenium import webdriver
import mysql.connector


driver = webdriver.Chrome(executable_path=r"C:\pyhton\webCrawl\chromedriver.exe")
driver.implicitly_wait(40)

url = 'https://klse.i3investor.com/financial/quarter/latest.jsp'
driver.get(url)
innerHTML = driver.execute_script('return document.body.innerHTML')
# soup = BeautifulSoup(innerHTML, 'lxml')

# to expand the "modify the visible columns i.e. checkboxes"
WebElementexpanded = driver.find_element_by_xpath(
    "//*[@id='ui-accordion-financialResultTableColumnsDiv-header-0']/span")
WebElementexpanded.click()

# to check all check boxes except xCheckBox where x = 1,2,3,4,19,20,22,23
allLinks = driver.find_elements_by_xpath('//input[@type="checkbox"]')
for link in allLinks:
    if link.is_selected():
        print('Checkbox already selected');
    else:
        link.click();
        print('Checkbox selected');
    # http://allselenium.info/working-with-checkboxes-using-python-selenium-webdriver/

# scrape all data in data tables
## IT works but does NOT include all of the additional data
# for tr in soup.find(class_="dataTable").find_all("tr"):
# data = [item.get_text(strip=True) for item in tr.find_all(["th","td"])]
# print(data)

# table = driver.find_element_by_xpath('//*[@id="tablebody"]')
# for row in table.find_elements_by_xpath('./tr/*'):
# print(row.text)

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# to automate clicking next page
elm = driver.find_element_by_class_name('next')
table = driver.find_element_by_xpath('//*[@id="tablebody"]')
# elm.click()

# https://codereview.stackexchange.com/questions/87901/copy-table-using-selenium-and-python
while True:
    element = WebDriverWait(driver, 100).until(lambda x: x.find_element_by_id('tablebody'))
    # for row in table.find_elements_by_xpath('./tr/*'):
    for row in table.find_elements_by_tag_name('tr'):
        # print(row.text)
        data = row.find_elements_by_tag_name('td')
        file_row = []
        for datum in data:
            datum_text = datum.text  # .encode('utf8')
            file_row.append(datum_text)
        print(file_row)

        # Insert data into mySQL database

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="abc123",
            database="wqd7005"
        )

        val = tuple(file_row)
        mycursor = mydb.cursor()
        sql = "INSERT INTO financial VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        mycursor.execute(sql, val)
        mydb.commit()

    elm = driver.find_element_by_class_name('next')
    if 'ui-state-disabled' in elm.get_attribute('class'):
        break;
    elm.click()





