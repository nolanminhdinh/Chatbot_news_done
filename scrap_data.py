import requests
from bs4 import BeautifulSoup
import json




#  lấy những link category chính từ trang chủ 
def get_category_links():
    url = 'https://vnexpress.net'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    category_links = {}
    category_menu = soup.find('nav', class_='main-nav')
    if category_menu:
        categories = category_menu.find_all('a')
        for category in categories[2:]: # lấy từ mục thời sự 
            name = category.text.strip()
            link = category['href']
            if link.startswith('/'):
                link = url + link
            if link.startswith('http'):  # Chỉ thêm liên kết hợp lệ
                category_links[name] = link

    return category_links

def get_news_links_from_category(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    articles = soup.find_all('article', class_='item-news')
    for article in articles:
        link_tag = article.find('a', href=True)
        if link_tag:
            links.append(link_tag['href'])

    return links

def get_news_details(link, parent_category):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find('h1', class_='title-detail')
    summary_tag = soup.find('p', class_='description')

    title = title_tag.text.strip() if title_tag else 'No title'
    summary = summary_tag.text.strip() if summary_tag else 'No summary'

    return {
        'title': title,
        'summary': summary,
        'link': link,
        'category': parent_category  # Sử dụng danh mục cha (lớn) làm danh mục,  là lấy chủ đề lớn nhất của bài báo đỏ làm mục category 
    }

def prepare_intents(news_data):
    intents = {"intents": []}
    for news in news_data:
        intents['intents'].append({
            'title': news['title'],
            'summary': news['summary'],
            'news_link': news['link'],
            'category': news['category'] 
        })
    return intents

# Lấy danh sách liên kết các danh mục từ trang chủ
category_links = get_category_links()

# Lấy danh sách các liên kết bài báo từ các danh mục
all_news_links = []
for category, link in category_links.items():
    print(f"Processing category: {category}")
    news_links = get_news_links_from_category(link)
    # Thêm thông tin danh mục cha vào mỗi liên kết
    for news_link in news_links:
        all_news_links.append((news_link, category))
    time.sleep(1)  # Tạm dừng để tránh bị chặn bởi server

# Lấy chi tiết từng bài báo
news_data = []
for link, parent_category in all_news_links:
    news_details = get_news_details(link, parent_category)
    news_data.append(news_details)
    time.sleep(1)  # Tạm dừng để tránh bị chặn bởi server

# Xử lý và lưu vào file JSON
news_intents = prepare_intents(news_data)

with open('news_scrap_data.json', 'w', encoding='utf-8') as file:
    json.dump(news_intents, file, ensure_ascii=False, indent=4)

print('Hoàn thành việc lấy dữ liệu từ web')
