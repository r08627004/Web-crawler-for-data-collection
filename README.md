# Web crawler for data collection
Using Python and R to do web crawling, and get specific data.

## Python
### Shopping mall
#### 家樂福
* URL : https://online.carrefour.com.tw/zh/homepage
* Using skills
  * BeautifulSoup, pandas
#### 熊媽媽買菜網
* URL : https://www.happy-shopping.tw/
* Using skills
  * Selenium, BeautifulSoup
  * See Shopping_mall_crawler.ipynb

### Wine Data
#### 愛酒窩iCheers
* URL : https://www.icheers.tw/iCheers/
* Using skills
  * Selenium, BeautifulSoup, pandas
  * See iCheers.py & iCheers.ipynb
#### 酒條通
* URL : https://www.609.com.tw
* Using skills
  * Selenium, BeautifulSoup, pandas (pd.concat)
  * See JGC.py

### Wage Data
#### 薪資——縣市重要指標
* URL : https://yoursalary.taiwanjobs.gov.tw/Salary/SalaryHome#
* Using skills
  * Selenium(window_handles,Select), BeautifulSoup, pandas
  * See Wage_crawler.ipynb


## R
### Climate data
* URL : https://e-service.cwb.gov.tw/HistoryDataQuery/
* Using packages : "jsonlite", "rvest", "magrittr", "lubridate"
* See climate_data_crawler.R
