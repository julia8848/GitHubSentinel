import requests, os, re
from bs4 import BeautifulSoup
from datetime import datetime
from logger import LOG 

class ArxivClient:
    def __init__(self):
        self.url_template = "http://arxiv.org/search/?query={keywords}&searchtype=all"

    def get_url(self, keywords="gaze tracking"):
        return self.url_template.format(keywords=keywords) 

    def get_top_articles(self, keywords):
        LOG.debug(f"Fetching Arxiv articles: {keywords}")
        try:
            response = requests.get(self.get_url(keywords), timeout=10)
            response.raise_for_status()  # 检查请求是否成功
            top_articles = self.parse_articles(response.text)
            return top_articles
        except Exception as e:
            LOG.error(f"Fail to fetch Arxiv articles：{str(e)}")
            return []


    def parse_articles(self, html_content):
        LOG.debug("Parsing fetched HTML...")
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('li', class_='arxiv-result') 

        top_articles = []
        for article in articles:
            new_entry = {}
            link_tag = article.find('p', class_='list-title').find('a')
            if not link_tag: continue
            new_entry["link"] = link_tag['href'] 
            arxiv_id = link_tag.text
            arxiv_id = re.sub(r'\s*arXiv:\s*', '', arxiv_id)
            new_entry["arxiv_id"] = arxiv_id

            title_element = article.find('p', class_='title')
            if title_element:
                new_entry["title"] = title_element.text.strip()  # Extract title text

            authors_element = article.find('p', class_='authors')
            if authors_element:
                authors = authors_element.text.strip()
                authors = re.sub(r'^\s*Authors:\s*', '', authors)
                authors = re.sub(r'\s+', ' ', authors)
                new_entry["authors"] = authors

            abstract_element = article.find('span', class_='abstract-full')
            if abstract_element:
                abstract = abstract_element.text.strip()
                abstract = re.sub(r'\s*\S\s*Less\s*$', '', abstract)
                new_entry["abstract"] = abstract
            top_articles.append(new_entry)

        LOG.info(f"{len(top_articles)} Articles parsed successfully.")
        return top_articles
    
    def export_top_articles(self, keywords="gaze tracking"):
        LOG.debug("Prepare to export recent articles from Arxiv.")
        top_articles = self.get_top_articles(keywords)
        
        if not top_articles:
            LOG.warning("No articles found.")
            return None

        # 构建存储路径
        dir_path = os.path.join('arxiv', re.sub(r'\W+', '_', keywords))
        os.makedirs(dir_path, exist_ok=True)  # 确保目录存在
        
        today = datetime.now().date().isoformat()
        file_path = os.path.join(dir_path, f'{today}.md')  # 定义文件路径
        with open(file_path, 'w') as file:
            file.write(f"# Arxiv Recent Articles About `{keywords}` ({today})\n\n")
            for idx, article in enumerate(top_articles, start=1):
                file.write(f"## {idx}. {article['title']}\n")
                file.write(f"**Arxiv**: [{article['arxiv_id']}]({article['link']})  \n")
                file.write(f"**Authors**: {article['authors']}  \n")
                file.write(f"**Abstract**: {article['abstract']}\n\n")
        
        LOG.info(f"File exported for recent articles from Arxiv: {file_path}")
        return file_path


    
if __name__ == "__main__":
    arxiv_client = ArxivClient()
    arxiv_client.export_top_articles("RAG")