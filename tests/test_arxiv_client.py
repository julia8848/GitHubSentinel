import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys
import os
from io import StringIO

# 添加 src 目录到模块搜索路径，以便可以导入 src 目录中的模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from arxiv_client import ArxivClient
from logger import LOG  # 导入日志记录器


class TestArxivClient(unittest.TestCase):
    def setUp(self):
        self.client = ArxivClient()

    @patch('arxiv_client.requests.get')
    def test_get_top_articles_success(self, mock_get):
        # 模拟HTTP响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '''
        <li class="arxiv-result">
            <div class="is-marginless">
            <p class="list-title is-inline-block"><a href="https://arxiv.org/abs/2411.01969">arXiv:2411.01969</a>
                <span>&nbsp;[<a href="https://arxiv.org/pdf/2411.01969">pdf</a>, <a href="https://arxiv.org/format/2411.01969">other</a>]&nbsp;</span>
            </p>
            <p class="title is-5 mathjax">
                Active <span class="search-hit mathjax">Gaze</span> Behavior Boosts Self-Supervised Object Learning
            </p>
            <p class="authors">
            <span class="has-text-black-bis has-text-weight-semibold">Authors:</span>
            <a href="/search/?searchtype=author&amp;query=Yu%2C+Z">Zhengyang Yu</a>, 
            <a href="/search/?searchtype=author&amp;query=Aubret%2C+A">Arthur Aubret</a>, 
            <a href="/search/?searchtype=author&amp;query=Raabe%2C+M+C">Marcel C. Raabe</a>, 
            <a href="/search/?searchtype=author&amp;query=Yang%2C+J">Jane Yang</a>, 
            <a href="/search/?searchtype=author&amp;query=Yu%2C+C">Chen Yu</a>, 
            <a href="/search/?searchtype=author&amp;query=Triesch%2C+J">Jochen Triesch</a>
            </p>
            <p class="abstract mathjax">
            <span class="search-hit">Abstract</span>:
            <span class="abstract-short has-text-grey-dark mathjax" id="2411.01969v1-abstract-short" style="display: inline;">
                …while interacting with objects. High acuity vision is only available in the central visual field, which may explain why toddlers (much like adults) constantly move their <span class="search-hit mathjax">gaze</span> around during such interactions. It is unclear whether/how much toddlers curate their visual experience through these eye movements to support learning object representations. In this w…
                <a class="is-size-7" style="white-space: nowrap;" onclick="document.getElementById('2411.01969v1-abstract-full').style.display = 'inline'; document.getElementById('2411.01969v1-abstract-short').style.display = 'none';">▽ More</a>
            </span>
            <span class="abstract-full has-text-grey-dark mathjax" id="2411.01969v1-abstract-full" style="display: none;">
                Due to significant variations in the projection of the same object from different viewpoints, machine learning algorithms struggle to recognize the same object across various perspectives. In contrast, toddlers quickly learn to recognize objects from different viewpoints with almost no supervision. Recent works argue that toddlers develop this ability by mapping close-in-time visual inputs to similar representations while interacting with objects. High acuity vision is only available in the central visual field, which may explain why toddlers (much like adults) constantly move their <span class="search-hit mathjax">gaze</span> around during such interactions. It is unclear whether/how much toddlers curate their visual experience through these eye movements to support learning object representations. In this work, we explore whether a bio inspired visual learning model can harness toddlers' <span class="search-hit mathjax">gaze</span> behavior during a play session to develop view-invariant object recognition. Exploiting head-mounted eye <span class="search-hit mathjax">tracking</span> during dyadic play, we simulate toddlers' central visual field experience by cropping image regions centered on the <span class="search-hit mathjax">gaze</span> location. This visual stream feeds a time-based self-supervised learning algorithm. Our experiments demonstrate that toddlers' <span class="search-hit mathjax">gaze</span> strategy supports the learning of invariant object representations. Our analysis also reveals that the limited size of the central visual field where acuity is high is crucial for this. We further find that toddlers' visual experience elicits more robust representations compared to adults' mostly because toddlers look at objects they hold themselves for longer bouts. Overall, our work reveals how toddlers' <span class="search-hit mathjax">gaze</span> behavior supports self-supervised learning of view-invariant object recognition.
                <a class="is-size-7" style="white-space: nowrap;" onclick="document.getElementById('2411.01969v1-abstract-full').style.display = 'none'; document.getElementById('2411.01969v1-abstract-short').style.display = 'inline';">△ Less</a>
            </span>
            </p>
        </li>
        '''
        mock_get.return_value = mock_response
        
        # 调用方法并验证返回值
        top_articles = self.client.get_top_articles(keywords="gaze tracking")
        self.assertEqual(len(top_articles), 1)
        self.assertEqual(top_articles[0]['title'], 'Active Gaze Behavior Boosts Self-Supervised Object Learning')
        self.assertEqual(top_articles[0]['link'], 'https://arxiv.org/abs/2411.01969')
        self.assertEqual(top_articles[0]['authors'], 'Zhengyang Yu, Arthur Aubret, Marcel C. Raabe, Jane Yang, Chen Yu, Jochen Triesch')
        self.assertEqual(top_articles[0]['abstract'], "Due to significant variations in the projection of the same object from different viewpoints, machine learning algorithms struggle to recognize the same object across various perspectives. In contrast, toddlers quickly learn to recognize objects from different viewpoints with almost no supervision. Recent works argue that toddlers develop this ability by mapping close-in-time visual inputs to similar representations while interacting with objects. High acuity vision is only available in the central visual field, which may explain why toddlers (much like adults) constantly move their gaze around during such interactions. It is unclear whether/how much toddlers curate their visual experience through these eye movements to support learning object representations. In this work, we explore whether a bio inspired visual learning model can harness toddlers' gaze behavior during a play session to develop view-invariant object recognition. Exploiting head-mounted eye tracking during dyadic play, we simulate toddlers' central visual field experience by cropping image regions centered on the gaze location. This visual stream feeds a time-based self-supervised learning algorithm. Our experiments demonstrate that toddlers' gaze strategy supports the learning of invariant object representations. Our analysis also reveals that the limited size of the central visual field where acuity is high is crucial for this. We further find that toddlers' visual experience elicits more robust representations compared to adults' mostly because toddlers look at objects they hold themselves for longer bouts. Overall, our work reveals how toddlers' gaze behavior supports self-supervised learning of view-invariant object recognition.")
        self.assertEqual(top_articles[0]['arxiv_id'], '2411.01969')
    
    @patch('arxiv_client.requests.get')
    def test_get_top_articles_failure(self, mock_get):
        # 模拟HTTP请求失败
        mock_get.side_effect = Exception("Connection error")
        
        # 调用方法并验证返回值
        top_stories = self.client.get_top_articles(keywords="gaze tracking")
        self.assertEqual(top_stories, [])

    
    @patch('arxiv_client.requests.get')
    @patch('arxiv_client.os.makedirs')
    @patch('arxiv_client.open', new_callable=unittest.mock.mock_open)
    def test_export_top_articles(self, mock_open, mock_makedirs, mock_get):
        # 模拟HTTP响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '''
        <li class="arxiv-result">
            <div class="is-marginless">
            <p class="list-title is-inline-block"><a href="https://arxiv.org/abs/2411.01969">arXiv:2411.01969</a>
                <span>&nbsp;[<a href="https://arxiv.org/pdf/2411.01969">pdf</a>, <a href="https://arxiv.org/format/2411.01969">other</a>]&nbsp;</span>
            </p>
            <p class="title is-5 mathjax">
                Active <span class="search-hit mathjax">Gaze</span> Behavior Boosts Self-Supervised Object Learning
            </p>
            <p class="authors">
            <span class="has-text-black-bis has-text-weight-semibold">Authors:</span>
            <a href="/search/?searchtype=author&amp;query=Yu%2C+Z">Zhengyang Yu</a>, 
            <a href="/search/?searchtype=author&amp;query=Aubret%2C+A">Arthur Aubret</a>, 
            <a href="/search/?searchtype=author&amp;query=Raabe%2C+M+C">Marcel C. Raabe</a>, 
            <a href="/search/?searchtype=author&amp;query=Yang%2C+J">Jane Yang</a>, 
            <a href="/search/?searchtype=author&amp;query=Yu%2C+C">Chen Yu</a>, 
            <a href="/search/?searchtype=author&amp;query=Triesch%2C+J">Jochen Triesch</a>
            </p>
            <p class="abstract mathjax">
            <span class="search-hit">Abstract</span>:
            <span class="abstract-short has-text-grey-dark mathjax" id="2411.01969v1-abstract-short" style="display: inline;">
                …while interacting with objects. High acuity vision is only available in the central visual field, which may explain why toddlers (much like adults) constantly move their <span class="search-hit mathjax">gaze</span> around during such interactions. It is unclear whether/how much toddlers curate their visual experience through these eye movements to support learning object representations. In this w…
                <a class="is-size-7" style="white-space: nowrap;" onclick="document.getElementById('2411.01969v1-abstract-full').style.display = 'inline'; document.getElementById('2411.01969v1-abstract-short').style.display = 'none';">▽ More</a>
            </span>
            <span class="abstract-full has-text-grey-dark mathjax" id="2411.01969v1-abstract-full" style="display: none;">
                Due to significant variations in the projection of the same object from different viewpoints, machine learning algorithms struggle to recognize the same object across various perspectives. In contrast, toddlers quickly learn to recognize objects from different viewpoints with almost no supervision. Recent works argue that toddlers develop this ability by mapping close-in-time visual inputs to similar representations while interacting with objects. High acuity vision is only available in the central visual field, which may explain why toddlers (much like adults) constantly move their <span class="search-hit mathjax">gaze</span> around during such interactions. It is unclear whether/how much toddlers curate their visual experience through these eye movements to support learning object representations. In this work, we explore whether a bio inspired visual learning model can harness toddlers' <span class="search-hit mathjax">gaze</span> behavior during a play session to develop view-invariant object recognition. Exploiting head-mounted eye <span class="search-hit mathjax">tracking</span> during dyadic play, we simulate toddlers' central visual field experience by cropping image regions centered on the <span class="search-hit mathjax">gaze</span> location. This visual stream feeds a time-based self-supervised learning algorithm. Our experiments demonstrate that toddlers' <span class="search-hit mathjax">gaze</span> strategy supports the learning of invariant object representations. Our analysis also reveals that the limited size of the central visual field where acuity is high is crucial for this. We further find that toddlers' visual experience elicits more robust representations compared to adults' mostly because toddlers look at objects they hold themselves for longer bouts. Overall, our work reveals how toddlers' <span class="search-hit mathjax">gaze</span> behavior supports self-supervised learning of view-invariant object recognition.
                <a class="is-size-7" style="white-space: nowrap;" onclick="document.getElementById('2411.01969v1-abstract-full').style.display = 'none'; document.getElementById('2411.01969v1-abstract-short').style.display = 'inline';">△ Less</a>
            </span>
            </p>
        </li>
        '''
        mock_get.return_value = mock_response
        
        # 调用方法
        file_path = self.client.export_top_articles(keywords="gaze tracking")
        today = datetime.now().date().isoformat()
        # 验证目录和文件创建
        mock_makedirs.assert_called_once_with(f'arxiv/gaze_tracking', exist_ok=True)
        mock_open.assert_called_once_with(f'arxiv/gaze_tracking/{today}.md', 'w')
        
        # 验证文件内容
        mock_open().write.assert_any_call(f"# Arxiv Recent Articles About `gaze tracking` ({today})\n\n")
        mock_open().write.assert_any_call("## 1. Active Gaze Behavior Boosts Self-Supervised Object Learning\n")
        mock_open().write.assert_any_call("**Arxiv**: [2411.01969](https://arxiv.org/abs/2411.01969)  \n")
        mock_open().write.assert_any_call("**Authors**: Zhengyang Yu, Arthur Aubret, Marcel C. Raabe, Jane Yang, Chen Yu, Jochen Triesch  \n")
        mock_open().write.assert_any_call("**Abstract**: Due to significant variations in the projection of the same object from different viewpoints, machine learning algorithms struggle to recognize the same object across various perspectives. In contrast, toddlers quickly learn to recognize objects from different viewpoints with almost no supervision. Recent works argue that toddlers develop this ability by mapping close-in-time visual inputs to similar representations while interacting with objects. High acuity vision is only available in the central visual field, which may explain why toddlers (much like adults) constantly move their gaze around during such interactions. It is unclear whether/how much toddlers curate their visual experience through these eye movements to support learning object representations. In this work, we explore whether a bio inspired visual learning model can harness toddlers' gaze behavior during a play session to develop view-invariant object recognition. Exploiting head-mounted eye tracking during dyadic play, we simulate toddlers' central visual field experience by cropping image regions centered on the gaze location. This visual stream feeds a time-based self-supervised learning algorithm. Our experiments demonstrate that toddlers' gaze strategy supports the learning of invariant object representations. Our analysis also reveals that the limited size of the central visual field where acuity is high is crucial for this. We further find that toddlers' visual experience elicits more robust representations compared to adults' mostly because toddlers look at objects they hold themselves for longer bouts. Overall, our work reveals how toddlers' gaze behavior supports self-supervised learning of view-invariant object recognition.\n\n")

    @patch('arxiv_client.requests.get')
    @patch('arxiv_client.os.makedirs')
    @patch('arxiv_client.open', new_callable=unittest.mock.mock_open)
    def test_export_top_articles_no_articles(self, mock_open, mock_makedirs, mock_get):
        # 模拟HTTP响应为空
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html></html>'
        mock_get.return_value = mock_response
        
        # 调用方法
        file_path = self.client.export_top_articles(keywords="gaze tracking")
        
        # 验证没有创建文件
        mock_makedirs.assert_not_called()
        mock_open.assert_not_called()
        self.assertIsNone(file_path)

if __name__ == '__main__':
    unittest.main()
