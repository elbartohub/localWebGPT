# 導入必要的庫
import gradio as gr
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from datetime import datetime
import os

# 初始化 Ollama 並加載 "llama3.1:latest" 版本模型
llm = Ollama(model="llama3.1:latest")

# 創建聊天提示模板
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一個智能助手。請使用繁體中文回覆。"),
    ("human", "{input}"),
])

# 創建聊天鏈
chat_chain = chat_prompt | llm | StrOutputParser()

# 定義保存提示的函數
def save_prompt(message):
    # 如果 prompt.txt 存在則追加，不存在則創建新文件
    mode = 'a' if os.path.exists("prompt.txt") else 'w'
    with open("prompt.txt", mode, encoding="utf-8") as file:
        # 獲取當前時間戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 將時間戳和消息寫入文件
        file.write(f"{timestamp}: {message}\n\n")

# 定義聊天函數
def chat(message, history):
    # 保存用戶的提示
    save_prompt(message)
    partial_message = ""
    # 使用流式處理來生成回應
    for chunk in chat_chain.stream({"input": message}):
        partial_message += chunk
        # 逐步產生回應
        yield partial_message

# 使用 Gradio Blocks 創建界面
with gr.Blocks() as demo:
    # 創建聊天界面
    gr.ChatInterface(
        fn=chat,  # 使用的聊天函數
        title="Ollama - Llama 3.1 聊天機器人",  # 界面標題
        description="這是個可以在完全沒有網絡下的全本地化聊天機器人。而所有提示都會被保存到文件中。",  # 描述
        examples=["你好，你是誰？", "請告訴我一些關於人工智能的知識。", "你能寫一首短詩嗎？"],  # 示例問題
        theme="soft"  # 使用柔和主題
    )

# 主程序
if __name__ == "__main__":
    # 啟動 Gradio 界面
    demo.launch()