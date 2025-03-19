# コードの解説
## ページの表示の順番
1. タイトル
2. メッセージ履歴
3. ユーザー入力

## タイトルの表示
```Python
st.title("🤖 StreamlitとLangChainによるチャットボット")
```

## メッセージ履歴の表示
### 表示する前にメッセージ履歴がなければ初期化
```Python
if "messages" not in st.session_state:
    st.session_state.messages = []  # メッセージ履歴を保持するリスト
```

### メッセージ履歴を表示する
```Python
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
```

## ユーザー入力の表示と応答
以下のコードで入力欄が表示される
```Python
st.chat_input("AIに聞きたいことを書いてね")
```

### 全体
```Python
if user_input := st.chat_input("AIに聞きたいことを書いてね"):
    # ユーザーのメッセージをStreamlitのメッセージ履歴に追加し、表示
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 処理中のインジケーターを表示
    with st.spinner("AIが考えています..."):
        # Streamlitのメッセージ履歴をLangChain形式に変換（最新の入力は除外）
        history = messages_to_langchain(st.session_state.messages[:-1])
        # AI応答を取得
        response = get_response(chain, history, user_input)

    # 応答をStreamlitのメッセージ履歴に追加し、表示
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
```

### Streamlitのメッセージ履歴をLangChain形式に変換する関数
```Python
def messages_to_langchain(messages):
    """Streamlitのメッセージ履歴をLangChainのメッセージ形式に変換する"""
    langchain_messages = []
    for msg in messages:
        if msg["role"] == "user":
            langchain_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            langchain_messages.append(AIMessage(content=msg["content"]))
    return langchain_messages
```

### LLMの応答を取得する関数
```Python
def get_response(chain, history, user_input):
    """LangChainのチェインを呼び出してAIの応答を取得する"""
    try:
        response = chain.invoke({
            "history": history,  # メッセージ履歴
            "input": user_input  # 最新の入力
        })
        # Gemma 3対応: <0xE3><0x80><0x80>を全角スペースに変換して返す
        return response.replace("\u3000", "　")
    except ConnectionError:
        return "⚠️ネットワークエラーが発生しました。接続を確認してください。"
    except Exception as e:
        return f"⚠️エラーが発生しました: {str(e)}"
```

### LLMの設定
```Python
llm = ChatOpenAI(
    model_name="gemma3",
    openai_api_base="http://localhost:11434/v1",
    openai_api_key="ollama",
    temperature=0.6,  # 応答の創造性を調整
)
```
### プロンプトテンプレートの定義
```Python
prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは役に立つアシスタントです。ユーザーに寄り添って質問にやさしくていねいに答えてください。"),
    ("placeholder", "{history}"),  # メッセージ履歴
    ("human", "{input}"),          # ユーザーの最新入力
])
```
### チェインの定義（プロンプト → LLM → 出力パーサー）
```Python
chain = prompt | llm | StrOutputParser()
```
