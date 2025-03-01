import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# ===============================
# アプリケーションのタイトル設定
# ===============================
st.title("Chatbot with Streamlit and LangChain")

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
SYSTEM_PROMPT = (
    "あなたは役に立つアシスタントです。"
)

# ===============================
# ChatOpenAIクライアントの初期化
# ===============================
# langchainのChatOpenAIを利用して、指定のモデルとAPI設定でクライアントを初期化する
chat = ChatOpenAI(
    model_name=MODEL,
    openai_api_base=BASE_URL,
    openai_api_key=OPENAI_API_KEY,
    temperature=TEMPERATURE
)

# ===============================
# セッション状態の初期化
# ===============================
# st.session_stateにチャットの履歴が保存されるリストが存在しなければ初期化
# 最初のメッセージとしてシステムメッセージ（プロンプト）を追加する
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
        messages (list): 辞書形式のメッセージリスト。各辞書は "role" と "content" をキーに持つ。
        
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
# st.session_state.messagesに保存されているメッセージを順に表示する
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ===============================
# ユーザーからの入力取得と応答生成
# ===============================
# ユーザーからの入力を受け付ける。入力があればチャットの処理を開始する。
if prompt := st.chat_input("AIに聞きたいことを書いてね"):
    # ユーザーの入力メッセージをセッション状態に追加して、履歴として保持
    st.session_state.messages.append({"role": "user", "content": prompt})

    # ユーザーの入力メッセージをチャットに表示
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # セッション状態のメッセージをlangchain用の形式に変換
    messages_for_model = convert_messages(st.session_state.messages)
    
    # ChatOpenAIクライアントを利用して、変換したメッセージリストを元に応答を生成
    response = chat.invoke(messages_for_model)

    # 応答メッセージをセッション状態に追加して、履歴として保持
    st.session_state.messages.append({"role": "assistant", "content": response.content})

    # 生成された応答をチャットに表示
    with st.chat_message("assistant"):
        st.markdown(response.content)
