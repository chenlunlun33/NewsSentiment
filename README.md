# NewsSentiment

### 1. 新聞爬蟲
新聞來源:ettoday
網址:https://www.ettoday.net/
資料範例:2330台積電新聞

### 2. 情緒分析
1. 先導入已爬取新聞資料
2. 刪除停用字
停用字字表可以參考網路上其他人製作的停用字表，這裡所使用的只單純刪除數字和我於幾篇新聞內容中看見之符號
4. 使用jieba分詞進行詞語切割
5. 做情緒分析
正面情緒對照表來源 : https://github.com/sweslo17/chinese_sentiment/blob/master/dict/ntusd-positive.txt
負面情緒對照表來源 : https://github.com/sweslo17/chinese_sentiment/blob/master/dictntusd-negative.txt
6. 依據指定時間間隔來作正反面情緒資料加總
時間間隔為前一日收盤時間13:30至今日收盤13:30前
例 : 1/1日所持有的新聞資料為 : 1/1日 13:30 至 1/2日 13:30 期間的所有新聞情緒資料加總
