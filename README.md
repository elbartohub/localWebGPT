<pre>
LocalWebGPT 

一、 項目目標

localWebGPT 項目旨在創建一個無需聯網的本地 Llama 3.2 AI 聊天機器人，用戶在沒有網絡連接的情況下也能使用大型語言模型進行對話。

二、 主要功能

本地化運行: 利用 Ollama 平台，在本地加載和運行 LLM 模型，無需依賴網絡連接。
多模型支持: 支持 Ollama 平台兼容的各種 LLM 模型，例如 Llama3.2:latest。
聊天記錄保存: 自動將用戶與機器人的對話內容保存到 "prompt.txt" 文件中，方便用戶查看和管理。
繁體中文界面和輸出: 使用 Gradio 庫構建了用戶友好的繁體中文聊天界面，並確保機器人始終以繁體中文進行回復。
對話記憶: 利用 ConversationBufferMemory 模塊，使機器人能夠記住對話歷史，並在後續對話中參考之前的信息。
  
三、 代碼實現

模型加載與初始化:
llm = Ollama(model="llama3.2:latest")
使用 Ollama 庫加載 "llama3.2:latest" 模型。
對話記憶:
memory = ConversationBufferMemory(return_messages=True)
創建 ConversationBufferMemory 對象，用於存儲和管理對話歷史。
提示模板:
prompt = ChatPromptTemplate.from_messages([
("system", "你是一個智能助手。請始終使用繁體中文回覆。"),
MessagesPlaceholder(variable_name="history"),
("human", "{input}")
])
定義聊天提示模板，設定機器人的身份和行為，並使用 "history" 變量來引用對話歷史。
對話鏈:
chain = (
RunnablePassthrough.assign(
history=lambda x: memory.load_memory_variables({})["history"]
)
| prompt
| llm
| StrOutputParser()
)
創建對話鏈，將各個組件連接起來，實現完整的對話流程：
從 memory 中加載對話歷史。
將歷史記錄和用戶輸入填充到提示模板中。
調用 llm 模型進行推理。
使用 StrOutputParser 解析模型輸出。
聊天界面:
with gr.Blocks() as demo:
gr.ChatInterface(
fn=chat,
title="Llama 3 聊天機器人",
description="這是一個使用 Llama 3 模型的簡單聊天機器人。所有的提示都會被保存到 prompt.txt 文件中。機器人會使用繁體中文回覆，並且能夠記住對話歷史。",
examples=["你好，你是誰？", "請告訴我一些關於人工智能的知識。", "你能寫一首短詩嗎？"],
theme="soft"
)
使用 Gradio 庫創建用戶友好的聊天界面，並提供一些示例問題。
提示保存:
def save_prompt(message):
mode = 'a' if os.path.exists("prompt.txt") else 'w'
with open("prompt.txt", mode, encoding="utf-8") as file:
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
file.write(f"{timestamp}: {message}\n\n")
定義 save_prompt 函數，將用戶輸入的提示信息保存到 "prompt.txt" 文件中。
  
四、 總結

localWebGPT 項目提供了一個簡單易用的本地 LLM AI 聊天機器人解決方案。它結合了 Ollama, Langchain 和 Gradio 等工具的優勢，實現了模型加載、對話管理、界面構建和數據保存等功能。該項目對於希望在離線環境下使用 LLM 進行實驗和開發的用戶非常有價值。
</pre>

![ui](https://github.com/user-attachments/assets/d5b2e6eb-9a43-40ac-9bf5-6c8cc5458c24)

<pre>
系統需求：

Win or Mac

支援任何版本 Ollama （簡易安裝方法)

目前默認 Llama3.2:latest 模型 或任何 Ollama 支持的 LLM

安裝：

git clone https://github.com/elbartohub/localWebGPT
cd localGPT
pip install -r requirements.txt
  </pre>
  
python app.py

自動將 Prompt 存檔為 prompt.txt。
