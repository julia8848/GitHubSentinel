import requests, os
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta  # 导入日期处理模块
from logger import LOG  # 导入日志模块

class HackerNewsClient:
    def __init__(self) -> None:
        self.url = 'https://news.ycombinator.com/'

    def fetch_hackernews_top_stories(self):
        response = requests.get(self.url)
        response.raise_for_status()  # 检查请求是否成功

        soup = BeautifulSoup(response.text, 'html.parser')
        # 查找包含新闻的所有 <tr> 标签
        stories = soup.find_all('tr', class_='athing')

        top_stories = []
        for story in stories:
            title_tag = story.find('span', class_='titleline').find('a')
            if title_tag:
                title = title_tag.text
                link = title_tag['href']
                top_stories.append({'title': title, 'link': link})

        return top_stories


    def export_progress(self):
        top_stories = self.fetch_hackernews_top_stories()

        # get current date time in format "YYYYMMDD_HH_mm_ss"
        now = datetime.now()
        formatted_filename = now.strftime("%Y%m%d_%H_%M_%S")
        formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        hacker_news_dir = os.path.join('daily_progress', 'hacker_news')  # 构建存储路径
        os.makedirs(hacker_news_dir, exist_ok=True)  # 确保目录存在
        file_path = os.path.join(hacker_news_dir, f'{formatted_filename}.md')  # 构建文件路径
        with open(file_path, 'w') as file:
            file.write(f"# Top Stories from Hacker News ({formatted_datetime})\n\n")
            for story in top_stories:  # 写入今天关闭的问题
                file.write(f"- {story['title']} (Link: {story['link']})\n")
        LOG.info(f"[Hacker News最新消息生成： {file_path}]")  # 记录日志
        return file_path


if __name__ == "__main__":
    hacker_news_client = HackerNewsClient()
    hacker_news_client.export_progress()
    