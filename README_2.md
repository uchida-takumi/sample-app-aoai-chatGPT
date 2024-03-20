# このリポジトリの説明

このリポジトリは以下のリポジトリをベースにしています。

https://github.com/microsoft/sample-app-aoai-chatGPT

## 初期設定

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
git push private [自分の作業ブランチ]
```

なお、上記のコマンドはchatGPTによって生成されたもので、間違っている可能性があります。
