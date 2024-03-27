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
AZURE_REGION=japaneast 
```

### azd setup

azd コマンドには、 az コマンドがインストールされている必要があります。

``` bash
# [if you need] init azd project(.azure/)
az cache purge
rm -rf .azure/

# login
azd auth login

# 新しい azd env（デプロイするアプリの環境）を設定する
azd env new ${APP_NAME} --subscription ${SUBSCRIPTION_NAME} --location ${AZURE_REGION}

```

### deploy

``` bash 
# set app project
python my_script/set_env.py --env_file .env
sh start.sh # update src/*
azd up # deploy 
```

### deploy 後に必要な設定

#### [手設定] 構築された Web アプリ の「構成＞全般設定＞スタートアップ コマンド」に以下を設定する
[スタートアップ コマンド] "python3 -m gunicorn app:app"

#### [手設定] 認証プロバイダーの設定

### すべてのリソースの削除
``` bash 
azd down
```

----

## 注意点

- 現時点では、使用しなくても、AI search がビルドされます。ここにはそれなりのコストがかかりますが、現在は許容しています。
- 特定の組み合わせの環境変数を.envに指定していないと、azd up がエラーになることが確認されています。特に、AI search のskuをフリープランで指定するとエラーになります。standardのままにしておきましょう。


