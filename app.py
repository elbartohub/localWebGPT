# 導入必要的庫
import gradio as gr
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough
from datetime import datetime
import os

# 初始化 Ollama 模型，使用 "llama3:latest" 版本
llm = Ollama(model="llama3.1:latest")

# 創建記憶組件
memory = ConversationBufferMemory(return_messages=True)

# 創建聊天提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一個智能助手。請始終使用繁體中文回覆。"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# 創建對話鏈
chain = (
    RunnablePassthrough.assign(
        history=lambda x: memory.load_memory_variables({})["history"]
    )
    | prompt
    | llm
    | StrOutputParser()
)

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
    response = chain.invoke({"input": message})
    memory.save_context({"input": message}, {"output": response})
    return response

# 使用 Gradio Blocks 創建界面
with gr.Blocks() as demo:
    # 創建聊天界面
    gr.ChatInterface(
        fn=chat,  # 使用的聊天函數
        title="Llama 3 聊天機器人",  # 界面標題
        description="這是一個使用 Llama 3 模型的簡單聊天機器人。所有的提示都會被保存到 prompt.txt 文件中。機器人會使用繁體中文回覆，並且能夠記住對話歷史。",  # 描述
        examples=["你好，你是誰？", "請告訴我一些關於人工智能的知識。", "你能寫一首短詩嗎？"],  # 示例問題
        theme="soft"  # 使用柔和主題
    )

# 主程序入口
if __name__ == "__main__":
    # 啟動 Gradio 界面
    demo.launch()
