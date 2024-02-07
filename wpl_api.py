import os
from urllib.request import urlopen

import requests 
from bs4 import BeautifulSoup 

class WPLAPI():
    wpl_url = "https://www.seogu.go.kr/learning/wolpyeonglib/index.do" 
    base_url = "https://www.seogu.go.kr"
    img_dir = "images"
    
    
    def save_recent_holiday_img(self):
        notice_title, notice_url = self._find_recent_holiday_notice()
        img_type, img_url  = self._get_holiday_img_url(notice_url)
        img_name = f"{self.img_dir}/{notice_title}.{img_type}"
        os.makedirs(self.img_dir, exist_ok=True)
        self.save_by_img_url(img_url, img_name)
        return img_name      
            
    def save_by_img_url(self, img_url, img_name):
        try:
            with urlopen(img_url) as f:
                with open(img_name, "wb") as file:
                    file.write(f.read())
        except Exception as e:
            raise Exception("이미지 저장에 실패했습니다.") from e
        
    def _get_holiday_img_url(self, notice_url):
        res = requests.get(notice_url)
        res.raise_for_status() # 정상 200
        soup = BeautifulSoup(res.text, "lxml")
        imgs = soup.find_all('img')
        img_type, target_img_url = None, None
        for img in imgs:
            img_url = img.get('src')
            if "jpg" in img_url:
                img_type = "jpg"
                target_img_url = img_url
            elif "png" in img_url:
                img_type = "png"
                target_img_url = img_url
        return img_type, target_img_url

    def _find_recent_holiday_notice(self):
        notice_items = self._get_notice_items()
        notice_title, notice_url = None, None
        for notice_item in notice_items:
            _title, _url = self._parse_notice_item(notice_item)
            if "휴관일" in _title:
                notice_title = _title
                notice_url = _url
        if notice_title:
            return notice_title, notice_url
        else:
            raise Exception("휴관일 공지가 없습니다.")

    def _get_notice_items(self):
        res = requests.get(self.wpl_url)
        res.raise_for_status() # 정상 200
        soup = BeautifulSoup(res.text, "lxml")
        notice = soup.find('div', id = 'notice')
        notice_ul = notice.find('ul')
        notice_items = notice_ul.find_all('a')
        return notice_items

    def _parse_notice_item(self, notice_item):
        notice_item = str(notice_item)
        temp = notice_item.split("href=\"")[1]
        sub_url, temp = temp.split("\">")
        title, temp = temp.split("</a>")
        _url = self.base_url + sub_url
        url = _url.replace("amp;", "")
        return title, url
