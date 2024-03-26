# このリポジトリの説明

このリポジトリは以下のリポジトリをベースにしています。

https://github.com/microsoft/sample-app-aoai-chatGPT


--- 
## ライブラリの初期設定

上記のリポジトリの更新を追跡するため、このgitリポジトリには以下のコマンドで設定しています。

``` bash
git remote add upstream https://github.com/microsoft/sample-app-aoai-chatGPT
git fetch upstream
```


## オリジナルリポジトリとの連携方法について

オリジナルのリポジトリの更新内容とマージ/リベース/プッシュするには、以下のコマンドを実行すること

``` bash
# マージ
git checkout [自分の作業ブランチ]
git merge upstream/[マージしたいブランチ]

# リベース
git checkout [自分の作業ブランチ]
git rebase upstream/[リベースしたいブランチ]

# プッシュ
git add .
git commit -m "wip"
git push private [自分の作業ブランチ]
```

なお、上記のコマンドはchatGPTによって生成されたもので、間違っている可能性があります。


----

## web-app のデプロイ

基本的には README_azc.md を参照すること。

### デプロイ用の環境変数

``` bash
APP_NAME=ai-for-children-dev
SUBSCRIPTION_NAME=cobloom
RESOURCE_GROUP_NAME=rg-ai-for-children-dev
AZURE_REGION=japaneast #
```

### azd setup

``` bash
# init azd project(.azure/)
az cache purge
rm -rf .azure/

# login
azd auth login
az login


# AI search をフリープランSKUに変更する
# infra/core/search/search-services.bicep の sku.name:'free' に変更する

# set app project
azd config set defaults.location ${AZURE_REGION}
azd config set defaults.subscription ${SUBSCRIPTION_NAME}
python my_script/set_env.py --type azd --env_file .env
sh start.sh # update src
azd up

# [手設定] 構築された Web アプリ の「構成＞全般設定＞スタートアップ コマンド」に以下を設定する
[スタートアップ コマンド] "python3 -m gunicorn app:app"




# set .env in app 
python my_script/set_env.py --type az --app_name ${APP_NAME} --resource_group_name ${RESOURCE_GROUP_NAME} --subscription_name ${SUBSCRIPTION_NAME}

# allow local code deployment
az webapp config appsettings set -g ${RESOURCE_GROUP_NAME} -n ${APP_NAME} --subscription ${SUBSCRIPTION_NAME} --settings WEBSITE_WEBDEPLOY_USE_SCM=false

az webapp config set --startup-file "python3 -m gunicorn app:app" --name ${APP_NAME} --subscription ${SUBSCRIPTION_NAME}

# deploy app
az webapp up --runtime PYTHON:3.11 --sku B1 --name ${APP_NAME} --resource-group ${RESOURCE_GROUP_NAME} --location ${AZURE_REGION} --subscription ${SUBSCRIPTION_NAME}

az webapp down

```



### 初期ビルド
``` bash
＃ルートディレクトリの azure.yaml がIACファイル
azd up 
```


### set .env to azure
azure 上の環境変数に、.env の環境変数を設定する

``` bash 
# .env ファイルを参考にAPPで動作させる環境変数を設定
azd env set DEBUG True
azd env set AZURE_OPENAI_RESOURCE test-univ-t-20240305
azd env set AZURE_OPENAI_MODEL gpt-35-turbo-16k
azd env set AZURE_OPENAI_KEY 97b9769239584c599549cb313d50dfd2
azd env set AZURE_OPENAI_MODEL_NAME gpt-35-turbo-16k
azd env set AZURE_OPENAI_TEMPERATURE 0
azd env set AZURE_OPENAI_TOP_P 1.0
azd env set AZURE_OPENAI_MAX_TOKENS 4000
azd env set AZURE_OPENAI_SYSTEM_MESSAGE "あなたは日本の子どもとおしゃべりをしたり、その質問に答えるAIです。"
azd env set AZURE_OPENAI_PREVIEW_API_VERSION 2023-12-01-preview
azd env set AZURE_OPENAI_STREAM True
azd env set AZURE_OPENAI_ENDPOINT 'https://test-univ-t-20240305.openai.azure.com/'
azd env set AZURE_OPENAI_EMBEDDING_NAME text-embedding-ada-002
azd env set AZURE_OPENAI_EMBEDDING_ENDPOINT 'https://test-univ-t-20240305.openai.azure.com/'
azd env set AZURE_OPENAI_EMBEDDING_KEY 97b9769239584c599549cb313d50dfd2

azd env set UI_TITLE テストアプリ
azd env set UI_CHAT_TITLE テストチャットアプリ





```


### APPの初期デプロイ
``` bash
az webapp up --runtime PYTHON:3.11 --sku B1 --name ${APP_NAME} --resource-group ${RESOURCE_GROUP_NAME} --location ${AZURE_REGION} --subscription ${SUBSCRIPTION_NAME}

az webapp config set --startup-file "python3 -m gunicorn app:app" --name ${APP_NAME} --subscription ${SUBSCRIPTION_NAME}

```

### 既存APP の setting を更新する場合

``` bash 
EXISTING_APP_NAME=ai-for-children
EXISTING_SKU=B1
EXISTING_RUNTIME=PYTHON:3.11

az webapp config appsettings set \
    -g ${RESOURCE_GROUP_NAME} \
    -n ${EXISTING_APP_NAME} \
    --subscription ${SUBSCRIPTION_NAME} \ 
    --settings WEBSITE_WEBDEPLOY_USE_SCM=false

az webapp up --runtime ${EXISTING_RUNTIME} --sku ${EXISTING_SKU} --name ${EXISTING_APP_NAME} --resource-group ${RESOURCE_GROUP_NAME}

az webapp config set --startup-file "python3 -m gunicorn app:app" --name ${EXISTING_APP_NAME}
```