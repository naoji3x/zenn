---
title: "m1 macにFinchをインストール"
emoji: "💻"
type: "tech"
topics: ["mac", "m1", "docker"]
published: false
---

## はじめに

```bash
brew install --cask finch
finch vm init
finch run --rm public.ecr.aws/finch/hello-finch # テスト
finch vm stop
mv "/Applications/Finch/lima/data/finch/diffdisk" "${NEW_IMAGE_PATH}"
mv: /Volumes/Share/finch/diffdisk: set owner/group (was: 501/0): Operation not permitted
ln -s "${NEW_IMAGE_PATH}" "/Applications/Finch/lima/data/finch/diffdisk"
```

コンテナ: 実行されている実体
イメージ: 実行するディスクイメージ

```bash
finch run --name some-nginx -d -p 8080:80 nginx # nginxを起動
finch images # Dockerイメージの確認
finch ps -a # Dockerコンテナの確認
finch pull [name] # イメージのダウンロード
finch rm [container name] # コンテナの削除
finch rmi [image id or image名] #イメージの削除
```

https://knowledge.sakura.ad.jp/13795/
