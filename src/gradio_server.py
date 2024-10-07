import gradio as gr  # 导入gradio库用于创建GUI

from config import Config  # 导入配置管理模块
from github_client import GitHubClient  # 导入用于GitHub API操作的客户端
from report_generator import ReportGenerator  # 导入报告生成器模块
from llm import LLM  # 导入可能用于处理语言模型的LLM类
from subscription_manager import SubscriptionManager  # 导入订阅管理器
from logger import LOG  # 导入日志记录器
import os
import pandas as pd

# 创建各个组件的实例
config = Config()
github_client = GitHubClient(config.github_token)
llm = LLM()
report_generator = ReportGenerator(llm)
subscription_manager = SubscriptionManager(config.subscriptions_file)

def fetch_updates(repo, days):
    return github_client.export_progress_by_date_range(repo, days)  # 获取更新内容和原始数据文件路径

def generate_report(updates_file_path, days):
    if not updates_file_path or not os.path.exists(updates_file_path):
        return "请先获取更新内容", None
    return report_generator.generate_report_by_date_range(updates_file_path, days)  # 生成报告内容和报告文件路径

def list_subscriptions():
    repo_list = subscription_manager.list_subscriptions()
    repo_df = pd.DataFrame(repo_list, columns=["项目名称"])
    return repo_df

def add_subscription(new_repo):
    repo_list = subscription_manager.list_subscriptions()
    if new_repo in repo_list:
        return f"**项目 {new_repo} 已订阅**", pd.DataFrame(repo_list, columns=["项目名称"])
    subscription_manager.add_subscription(new_repo)
    return f"**项目 {new_repo} 订阅成功**", list_subscriptions()

def del_subscription(del_repo):
    repo_list = subscription_manager.list_subscriptions()
    if del_repo not in repo_list:
        return f"**项目 {del_repo} 未订阅**", pd.DataFrame(repo_list, columns=["项目名称"])
    subscription_manager.remove_subscription(del_repo)
    return f"**项目 {del_repo} 删除成功**", list_subscriptions()

def update_dropdowns():
    repo_list = subscription_manager.list_subscriptions()
    del_repo = gr.Dropdown(repo_list, label="删除订阅", info="选择要删除的GitHub项目")
    repo = gr.Dropdown(repo_list, label="订阅列表", info="已订阅GitHub项目")
    return del_repo, repo

# 创建Gradio界面
with gr.Blocks() as demo:
    with gr.Tab(label="订阅管理"):
        with gr.Row():
            with gr.Column():
                new_repo = gr.Textbox(label="添加订阅", info="输入GitHub项目名称，例如：username/repo")
                add_subscription_btn = gr.Button(value="添加订阅")
            with gr.Column():
                del_repo = gr.Dropdown(subscription_manager.list_subscriptions(), label="删除订阅", info="选择要删除的GitHub项目")
                del_subscription_btn = gr.Button(value="删除订阅")
        action_result = gr.Markdown(label="操作结果")
        repo_list = gr.Dataframe(label="已订阅列表", headers=["项目名称"], value=list_subscriptions())
        add_subscription_btn.click(add_subscription, inputs=[new_repo], outputs=[action_result, repo_list])
        del_subscription_btn.click(del_subscription, inputs=[del_repo], outputs=[action_result, repo_list])

    with gr.Tab(label="报告生成"):
        with gr.Row():
            with gr.Column():
                repo = gr.Dropdown(
                    subscription_manager.list_subscriptions(), label="订阅列表", info="已订阅GitHub项目"
                )  # 下拉菜单选择订阅的GitHub项目
            days = gr.Slider(value=2, label="报告周期", info="生成项目过去一段时间进展，单位：天", minimum=1, maximum=7, step=1)
        with gr.Row():
            with gr.Column():
                fetch_updates_btn = gr.Button(value="获取更新")
                updates = gr.Markdown(label="更新内容", show_label=True, height=400)
                updates_file_path = gr.File(label="下载更新")
                fetch_updates_btn.click(fetch_updates, inputs=[repo, days], outputs=[updates, updates_file_path])
            with gr.Column():
                generate_report_btn = gr.Button(value="生成报告")
                report = gr.Markdown(label="报告内容", show_label=True, height=400)
                report_file_path = gr.File(label="下载报告")
                generate_report_btn.click(generate_report, inputs=[updates_file_path, days], outputs=[report, report_file_path])
        repo_list.change(update_dropdowns, outputs=[del_repo, repo])

if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0")  # 启动界面并设置为公共可访问
    # 可选带有用户认证的启动方式
    # demo.launch(share=True, server_name="0.0.0.0", auth=("django", "1234"))