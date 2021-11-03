##### 爬氣候資料
# 目標網站：https://e-service.cwb.gov.tw/HistoryDataQuery/
packages <- c("jsonlite", "rvest", "magrittr", "lubridate")

installed_packages <- packages %in% rownames(installed.packages())
if (any(installed_packages == FALSE)) {
  install.packages(packages[!installed_packages])
}

# 載入所需套件
lapply(packages, library, character.only = TRUE) %>%
  invisible()


# url <- "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=466910&stname=%25E9%259E%258D%25E9%2583%25A8&datepicker=2000-01"
url_start <- "https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=C0K330&stname=%25E8%2599%258E%25E5%25B0%25BE&datepicker="
temp <- seq.Date(from = as.Date("2000-01-01",format = "%Y-%m-%d"), by = "month", length.out = 252)
temp <- format(temp, format = "%Y-%m")
data1 <- data.frame()
data2 <- data.frame()
for(i in temp){
  url <- paste0(url_start,as.character(i))
  #時間資料
  day <- url %>% 
    read_html() %>%
    html_nodes(xpath='//*[(@id = "MyTable")]//td[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]') %>% 
    html_text(trim	= T) %>% 
    as.numeric()
  #氣溫資料
  temperature <- url %>% 
    read_html() %>%
    html_nodes(xpath='//td[(((count(preceding-sibling::*) + 1 ) = 8) and parent::*)]') %>% 
    html_text(trim	= T) %>% 
    as.numeric()
  temperature <- temperature[2:length(temperature)]  
  #降雨資料
  rainfall <- url %>% 
    read_html() %>%
    html_nodes(xpath='//td[(((count(preceding-sibling::*) + 1 ) = 22) and parent::*)]') %>% 
    html_text(trim	= T) %>%
    as.numeric()
  data1 <- cbind(as.character(i), day, temperature, rainfall)
  data2 <- rbind(data2, data1)
  write.csv(data1,file = paste0("saving_path", i, ".csv"))
}
write.csv(data2,file = paste0("file_name.csv"))