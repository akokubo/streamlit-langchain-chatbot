import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# ===============================
# アプリケーションの設定
# ===============================
# ページの基本設定（タイトル、アイコン、レイアウトなど）
st.set_page_config(
    page_title="StreamlitとLangChainによるチャットボット",
    page_icon="🤖",
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
  <svg x="6" y="6" width="20" height="20" viewBox="0 -960 960 960" xmlns="http://www.w3.org/2000/svg" fill="#ffffff"><path d="M395-144q-47 0-80-31t-38-77q-57-6-95-48t-38-100.02q0-19.98 4.5-41.48Q153-463 164-480q-10-17.07-15-36.03-5-18.97-5-39.31 0-56.39 37-97.52Q218-694 275-702q2-48 37.04-81t82.99-33q23.97 0 45.97 9t39.46 26q16.54-17 37.87-26t45.44-9Q612-816 647-783q35 33 37 81 57 7 94.5 48.72T816-555q0 20.94-5.5 39.97Q805-496 795-479q12 20 16.5 40t4.5 39.48q0 57.52-38.5 100.02Q739-257 682-252q-5 46-38 77t-80.27 31q-23.17 0-44.95-8.5T480-178q-17 16-39.03 25T395-144Zm121-551.3v431.6q0 19.7 13.92 34.2Q543.84-215 564-215q20 0 33-14t14-34q-19-8-35.07-20.33Q559.86-295.65 547-313q-9-12.48-6.5-26.74Q543-354 555.5-363q12.5-9 26.98-6.76Q596.95-367.53 606-355q10.55 15.03 26.86 23.02 16.3 7.98 35.49 7.98Q700-324 722-346t22-54q0-7-1-13t-3-12q-15.9 9-34.13 13.5Q687.64-407 668-407q-15.3 0-25.65-10.29Q632-427.58 632-442.79t10.35-25.71Q652.7-479 668-479q32 0 54-22t22-53.53q0-31.52-22-53.5Q700-630 666.25-631 655-614 639.5-601T604-581q-14 5-27.5-1.26-13.5-6.27-18.5-20.58-5-14.32 1.5-27.74Q566-644 580.45-649 594-654 603-666.39t9-28.59q0-20.02-13.92-34.52Q584.16-744 564-744q-20.16 0-34.08 14.5Q516-715 516-695.3ZM444-264v-431.31q0-19.69-14.5-34.19Q415-744 394.89-744q-20.12 0-34 14.28Q347-715.44 347-694.76q0 15.76 9 28.26 9 12.5 22.55 17.5 14.45 5 20.95 18.37Q406-617.26 401-603q-5 14-18.5 20.5T355-581q-20-7-35.5-20t-26.76-30Q260-630 238-608t-22 53.02Q216-523 238-501q22 22 54 22 15.3 0 25.65 10.29Q328-458.42 328-443.21t-10.35 25.71Q307.3-407 292-407q-19.6 0-37.8-5-18.2-5-34.2-14-2 6-3 12.67-1 6.66-1 13.33 0 32 22 54t53.65 22q19.19 0 35.49-7.98Q343.45-339.97 354-355q9.29-13.26 24.14-15.63Q393-373 405-364t14.5 24q2.5 15-6.25 27.3Q401-296 384.5-283T348-262q1 20 14 33t32.71 13q20.7 0 35-13.92Q444-243.84 444-264Zm36-215Z"/></svg>
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
