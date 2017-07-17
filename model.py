import jieba
import requests
from db_config import db_session, Base
from sqlalchemy import Column, Integer, String
from bs4 import BeautifulSoup


class Record(Base):
    __tablename__ = 'Records'
    id = Column(Integer, primary_key=True)
    url = Column(String(1000), unique=True)
    keys = Column(String(1000))

    def featch(self, url):
        self.url = url
        html = requests.get(self.url).content
        soup = BeautifulSoup(html, 'html.parser')
        keys_list = jieba.lcut_for_search(soup.title.string)
        self.keys = ' '.join(keys_list)
        return self

    def __str__(self):
        return "%s%s%s" % (self.id, self.keys, self.url)
