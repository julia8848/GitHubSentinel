# src/llm.py

import os
from openai import OpenAI

class LLM:
    def __init__(self):
        self.client = OpenAI()
        self.system_prompt = """
            你接下来收到的都是开源项目的最新进展相关信息（Markdown格式），包括commits/issues/pull requests等。
            你将根据这些信息，总结一个中文的报告，以项目名称开头，包含"新增功能"、"主要改进"，"修复问题“三个板块。

            生成报告格式如下：
            # [组织] /[仓库名]项目进展
            ## 新增功能
            - [功能描述] (#issue_number)
            - [功能描述] (#issue_number)
            ## 主要改进
            - [改进描述] (#issue_number)
            - [改进描述] (#issue_number)
            ## 修复问题
            - [问题描述] (#issue_number)
            - [问题描述] (#issue_number)

            具体案例请参考下面的示例：
            # DjangoPeng/openai-quickstart项目进展
            ## 新增功能
            - 新增作业提交自动对话10次的功能 (#98)
            - 为 openai-translator 添加中文注释 (#60)
            ## 主要改进
            - 将模型从OpenAI更改为ChatGLM2，提高翻译质量 (#102)
            - 对agent代码进行了更新以优化性能 (#111)
            ## 修复问题
            - 修复了requests.exceptions.RequestException和Timeout捕获异常的位置 (#55)
            - 解决了翻译pdf时出现的服务器连接错误 (#87)
        """

    def generate_daily_report(self, markdown_content, dry_run=False):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": markdown_content},
        ]

        if dry_run:
            with open("daily_progress/prompt.txt", "w+") as f:
                f.write(json.dump(messages, f, indent=4, ensure_ascii=False))
            return "DRY RUN"

        print("------Before call GPT------")
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        print("------After call GPT------")
        print(response)
        return response.choices[0].message.content
