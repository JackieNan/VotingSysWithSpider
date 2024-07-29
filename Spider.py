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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
    }
    conn = sqlite_connect()
    cursor = conn.cursor()

    html = requests.get('https://www.gamersky.com/news/')
    html.encoding = 'utf-8'
    html_text = html.text

    if html.status_code == 200:
        print('请求成功')
        e = etree.HTML(html_text)

        candidates_list = e.xpath('//div[@class="Mid2L_con block"]/ul/li')

        for candidate in candidates_list:
            print('开始存库')
            name = candidate.xpath('//div[@class= "tit"]/a/text()')
            title_text = name[0].strip() 
            # clean_name = name
            # re.sub(r'^\[\'|\'\]$', '', str(name))
            print(title_text)

            bio = candidate.xpath('div[@class= "con"]/div/text()')
            bio_text = bio[0].strip()
            # text = re.sub(r"^\['", "", bio)

            # clean_bio = re.sub(r"\。\s*[^']*", "", text)
            
            print(bio_text)
            
            position_id = 3

            img_url = candidate.xpath('div[@class= "img"]/a/@href')
            res_img = requests.get(url=img_url, headers=headers)
            code = res_img.content
            ima_name = img_url.split('/')[-1]
            with open(f'media/candidates/{img_name}', 'wb') as f:
                f.write(code)
                print(f'{img_name}写入成功')


            insert_sql = '''INSERT INTO voting_candidate(fullname, photo, bio, position_id) VALUES(?,?,?,?) '''
            cursor.execute(insert_sql, (clean_name, f'media/candidates/{img_name}', clean_bio, position_id))
            conn.commit()
            print('存库成功')