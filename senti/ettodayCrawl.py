import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


timeList = []
contextList = []
headers = {'user-agent': 'Mozilla/5.0'}

code = '2330'

for i in range(1, 5):
    print('page' + str(i))
    url = 'https://www.ettoday.net/news_search/doSearch.php?keywords=' + code + '&idx=1&page=' + str(i)
    response = requests.get(url)
    html_content = response.text

    pattern = r'<!--結果01 開始-->(.*?)<!--結果01 結束-->'
    match = re.search(pattern, html_content, re.DOTALL)

    if match:
        content = match.group(1)
        # 使用正則表達式找到所有<a>標籤中的href和target屬性值之間的網址和目標
        a_tags = re.findall(r'<a\s+href="([^"]+)"\s+target="([^"]+)"', content)
        
        # 處理每個<a>標籤的網址和目標
        for href, target in a_tags[::2]:
            # 要爬取的新聞頁面
            innerUrl = href
            
            response = requests.get(innerUrl)
            html_content = response.text

            pattern1 = r'<!--本文 開始-->(.*?)<!--本文 結束-->'
            innerMatch = re.search(pattern1, html_content, re.DOTALL)
            pattern2 = r'<!--時間 開始-->(.*?)<!--時間 結束-->'
            timeMatch = re.search(pattern2, html_content, re.DOTALL)

            if timeMatch:
                timeContent = timeMatch.group(1)
                # 使用Beautiful Soup解析找到的內容，以提取<p>標籤內的文字
                soup = BeautifulSoup(timeContent, 'html.parser')
                time_tags = soup.find_all('time')
                time_texts = [time.get_text() for time in time_tags]

                # 輸出提取到的文字
                
                # print(str.strip(time_texts[0]))
                if '日' not in str.strip(time_texts[0]):
                    timeList.append(str.strip(time_texts[0]))
                
            
            if innerMatch:
                innerContent = innerMatch.group(1)
                # 使用Beautiful Soup解析找到的內容，以提取<p>標籤內的文字
                soup = BeautifulSoup(innerContent, 'html.parser')
                p_tags = soup.find_all('p')
                p_texts = [p.get_text() for p in p_tags]

                # 輸出提取到的文字
                totalText = []
                if '日' not in str.strip(time_texts[0]):
                    for text in p_texts[3:]:
                        if '責任編輯：' in text or text == '' or '※' in text or '►' in text or '▲' in text or '▸' in text:
                            continue
                        totalText.append(text)
                        # print(text)
                    contxt = ''.join(totalText)
                    contextList.append(contxt)
                    # print('')
            else:
                print("未找到新聞內容")
    else:
        print("未找到符合內容")
print(len(timeList))
print(len(contextList))
df = pd.DataFrame(zip(timeList, contextList), columns = ['time', 'context'])
df.to_csv('news\\' + code + '.csv')
