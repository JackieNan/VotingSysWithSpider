import re
import requests
import sqlite3
from lxml import etree

# Connect to database
def sqlite_connect():
    conn = sqlite3.connect('db.sqlite3')
    return conn

def req(url):
    res = requests.get(url=url)
    res.encoding = 'utf-8'
    return res.text

if __name__ == '__main__':
    conn = sqlite_connect()
    cursor = conn.cursor()

    html = requests.get('https://www.nytimes.com/interactive/2023/us/politics/presidential-candidates-2024.html')
    html.encoding = 'utf-8'
    html_text = html.text

    if html.status_code == 200:
        print('请求成功')
        e = etree.HTML(html_text)

        candidates_list = e.xpath('//div[contains(@aria-label, "information card")]')

        for candidate in candidates_list:
            print('开始存库')
            name = candidate.xpath('div[@class= "image-container svelte-jedu2t"]/header/h4/text()')
            clean_name = re.sub(r'^\[\'|\'\]$', '', str(name))
            print(clean_name)

            bio = candidate.xpath('div[contains(@class, "body svelte")]/p/text()')
            c_bio = re.sub(r'^\[\'|\'\]$', '', str(bio))
            clean_bio = c_bio.rstrip("', '\\n\\t\\n")
            print(clean_bio)
            
            position_id = 3
            img_url_full = ""

            div_element = candidate.xpath('div[contains(@class,"image svelte-jedu2t")]')
            if div_element:
                div_element = div_element[0]
                style_value = div_element.get('style')

                match = re.search(r'url\((.*?)\)', style_value)
                if match:
                    print('开始下载图片')
                    img_url = unquote(match.group(1))
                    img_url_full = urljoin('https://www.nytimes.com', img_url)
                    print(img_url_full)
                    response = requests.get(img_url_full)
                    if response.status_code == 200:
                        # 保存图片
                        with open('harris.jpg', 'wb') as f:
                            f.write(response.content)
                        print('图片已保存')
                    else:
                        print('图片下载失败')
            
            insert_sql = '''INSERT INTO voting_candidate(fullname, photo, bio, position_id) VALUES(?,?,?,?) '''
            cursor.execute(insert_sql, (clean_name, img_url_full, clean_bio, position_id))
            conn.commit()
            print('存库成功')