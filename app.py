import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# ===============================
# アプリケーションの設定
# ===============================
# ページの基本設定（タイトル、アイコン、レイアウトなど）
st.set_page_config(
    page_title="StreamlitとLangChainによるチャットボット",
    page_icon="‍🤖",
    layout="wide"
)
st.title("StreamlitとLangChainによるチャットボット")

# ===============================
# モデルおよびAPIの設定
# ===============================
# 使用する生成モデルの名前（例: lucas2024/gemma-2-2b-jpn-it:q8_0）
MODEL = "lucas2024/gemma-2-2b-jpn-it:q8_0"
# APIのベースURL（ここではローカルのollamaサーバーを指定）
BASE_URL = "http://localhost:11434/v1"
# APIキー（ここでは「ollama」という固定値を使用）
OPENAI_API_KEY = "ollama"
# 生成温度：0.6で多様な応答、0.0に設定すると決定論的な出力
TEMPERATURE = 0.6

# システムプロンプト：アシスタントの役割や振る舞いを定義
SYSTEM_PROMPT = "あなたは役に立つアシスタントです。"

# ===============================
# システムアイコン用SVG（32x32の角丸背景に20x20のアイコン）
# ===============================
SYSTEM_ICON = '''
<svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
  <!-- 背景の角丸正方形（薄い灰色） -->
  <rect x="0" y="0" width="32" height="32" rx="8" fill="#cccccc" />
  <!-- 中央に配置された20x20のアイコン -->
  <svg x="6" y="6" width="20" height="20" viewBox="0 -960 960 960" xmlns="http://www.w3.org/2000/svg" fill="#1f1f1f">
    <path d="M390-120q-51 0-88-35.5T260-241q-60-8-100-53t-40-106q0-21 5.5-41.5T142-480q-11-18-16.5-38t-5.5-42q0-61 40-105.5t99-52.5q3-51 41-86.5t90-35.5q26 0 48.5 10t41.5 27q18-17 41-27t49-10q52 0 89.5 35t40.5 86q59 8 99.5 53T840-560q0 22-5.5 42T818-480q11 18 16.5 38.5T840-400q0 62-40.5 106.5T699-241q-5 50-41.5 85.5T570-120q-25 0-48.5-9.5T480-156q-19 17-42 26.5t-48 9.5Zm130-590v460q0 21 14.5 35.5T570-200q20 0 34.5-16t15.5-36q-21-8-38.5-21.5T550-306q-10-14-7.5-30t16.5-26q14-10 30-7.5t26 16.5q11 16 28 24.5t37 8.5q33 0 56.5-23.5T760-400q0-5-.5-10t-2.5-10q-17 10-36.5 15t-40.5 5q-17 0-28.5-11.5T640-440q0-17 11.5-28.5T680-480q33 0 56.5-23.5T760-560q0-33-23.5-56T680-640q-11 18-28.5 31.5T613-587q-16 6-31-1t-20-23q-5-16 1.5-31t22.5-20q15-5 24.5-18t9.5-30q0-21-14.5-35.5T570-760q-21 0-35.5 14.5T520-710Zm-80 460v-460q0-21-14.5-35.5T390-760q-21 0-35.5 14.5T340-710q0 16 9 29.5t24 18.5q16 5 23 20t2 31q-6 16-21 23t-31 1q-21-8-38.5-21.5T279-640q-32 1-55.5 24.5T200-560q0 33 23.5 56.5T280-480q17 0 28.5 11.5T320-440q0 17-11.5 28.5T280-400q-21 0-40.5-5T203-420q-2 5-2.5 10t-.5 10q0 33 23.5 56.5T280-320q20 0 37-8.5t28-24.5q10-14 26-16.5t30 7.5q14 10 16.5 26t-7.5 30q-14 19-32 33t-39 22q1 20 16 35.5t35 15.5q21 0 35.5-14.5T440-250Zm40-230Z"/>
  </svg>
</svg>
'''

# ===============================
# ChatOpenAIクライアントの初期化
# ===============================
chat = ChatOpenAI(
    model_name=MODEL,
    openai_api_base=BASE_URL,
    openai_api_key=OPENAI_API_KEY,
    temperature=TEMPERATURE
)

# ===============================
# セッション状態の初期化
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# ===============================
# メッセージ変換関数の定義
# ===============================
def convert_messages(messages):
    """
    セッション状態の辞書形式のメッセージリストを、
    langchainのメッセージオブジェクト（SystemMessage, HumanMessage, AIMessage）のリストに変換する関数。
    
    Parameters:
        messages (list): 各辞書が "role" と "content" をキーに持つメッセージリスト。
        
    Returns:
        list: LangChain用のメッセージオブジェクトリスト。
    """
    converted = []
    for msg in messages:
        if msg["role"] == "system":
            converted.append(SystemMessage(content=msg["content"]))
        elif msg["role"] == "user":
            converted.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            converted.append(AIMessage(content=msg["content"]))
    return converted

# ===============================
# 既存のチャットメッセージの表示
# ===============================
for message in st.session_state.messages:
    if message["role"] == "system":
        # システムメッセージの場合、カスタムSVGアイコンを指定
        with st.chat_message("system", avatar=SYSTEM_ICON):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ===============================
# ユーザーからの入力取得と応答生成
# ===============================
if prompt := st.chat_input("AIに聞きたいことを書いてね"):
    # ユーザーのメッセージをメッセージ履歴に追加し、表示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 一連のメッセージ履歴をLLMに送信して応答を取得
    messages_for_model = convert_messages(st.session_state.messages)    
    response = chat.invoke(messages_for_model)

    # 応答をセッション状態に追加し、表示
    st.session_state.messages.append({"role": "assistant", "content": response.content})
    with st.chat_message("assistant"):
        st.markdown(response.content)
