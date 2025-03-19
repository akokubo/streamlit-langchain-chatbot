# StreamlitとLangChainによるチャットボット

![Streamlit LangChain Chatbot](images/streamlit-langchain-chatbot.png)

## 使用したもの
* [Streamlit](https://streamlit.io/)
* [LangChain](https://www.langchain.com/)
* [Ollama](https://ollama.com/)か[LM Studio](https://lmstudio.ai/)

## インストール
```
git clone https://github.com/akokubo/streamlit-langchain-chatbot.git
cd streamlit-langchain-chatbot
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```
※Windowsの場合、WSL2の[新しいもの](https://github.com/microsoft/WSL/releases/)をインストールし、アップデート&アップグレードし、python3-pipやpython3.12-venvなどなどをインストールしてからご利用ください。

※仮想環境は、condaなどでもいい。

## Ollamaの準備
1. Ollamaをインストール
   - Windowsの場合は、WSL2で仮想環境から `curl -fsSL https://ollama.com/install.sh | sh` でインストール
   - Macの場合は、[ダウンロード](https://ollama.com/download/windows)してインストール
2. Ollamaで大規模言語モデルの `gemma3` などをpullする。
```
ollama pull gemma3
```
※大規模言語モデルは、自由に選べ、他のものでもいい。

※Ollamaの代わりに[LM Studio](https://lmstudio.ai/)も利用できる。その場合、「lmstudio-community/gemma-3-4b-it」などのモデルをダウンロードする。LM Studioで、サーバーを走らせるには、左の「開発者」を選び、「Status」のトグルスイッチを切り替え「Running」にし、「Settings」で「ローカルネットワークでサービング」をオンにする。そして、app.pyの中の「BASE_URL」を `"http://localhost:1234/v1"`に変更する。右の「This model's API identifier」の値を「MODEL」に指定する。

※Windowsで、WSLからLM Studioに接続するには、ローカルネットワークでサービングをオンにし、右の「The local server is reachable at this address」のIPアドレスを `localhost` の代わりに指定する。

## 実行
最初に、プログラムを展開したフォルダに入る。
次に仮想環境に入っていない場合(コマンドプロンプトに(venv)と表示されていないとき)、仮想環境に入る。
```
source venv/bin/activate
```

Ollamaが起動していないかもしれないので、仮想環境に入っている状態で、大規模言語モデルのリストを表示する(すると起動していなければ、起動する)。
```
ollama list
```
※Ollamaの代わりにLM Studioを使っている場合は不要

仮想環境に入っている状態で、以下のコマンドでアプリを起動する。
```
python3 -m streamlit run app.py
```

## コードの解説
詳しいコードの解説は[こちら](docs/CODE_EXPLANATION.md)をご覧ください。

## 作者
[小久保 温(こくぼ・あつし)](https://akokubo.github.io/)

## ライセンス
[MIT License](LICENSE)
