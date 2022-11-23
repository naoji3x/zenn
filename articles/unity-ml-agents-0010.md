---
title: "Unity ml-agentsを動かす"
emoji: "💻"
type: "tech"
topics: ["mac", "m1", "unity", "machinelearning", "python"]
published: true
---

## はじめに

プロフィールにUnity歴6年と書いておきながら、Unityネタがなかったのでml-agentsを題材に記事を書いてみました。m1 macだとインストールからつまづきましたので、そこまで備忘としてまとめます。最終的にはShqnDさんの記事のおかげで動くようになりました（ありがとうございました😆！）。

https://qiita.com/ShqnD/items/471d9950a0e072a4cb65

## ml-agentsとは

ゲームの敵キャラの動きなどをAIでチューニングする仕組みです。

https://unity.com/ja/products/machine-learning-agents

見た目が面白いので、そのうちCoderDojoで使ってみたいと思っています。

## インストールした環境

16インチ MacBook Pro 2021にインストールしました。スペックは以下になります。

チップ Apple M1 Max
メモリ 32 GB
macOS 13.0.1

## ml-agentsの取得

先ずはml-agentsのソースをGitHubからダウンロードしました。2022/11/23時点でrelease 20が最新なのでそちらをcloneしています。

```zsh
% cd your/project/root
% git clone --depth 1 --branch release_20 git@github.com:Unity-Technologies/ml-agents.git
% cd ml-agents
```

## Python環境の整備

Pythonの環境は以下の記事にあるようにminiforgeで構築しています。

https://zenn.dev/naoji/articles/m1-mac-setting-0010


ml-agents用に`ml-agents-20`という名前の仮想環境を作成してアクティベートしました。

```zsh
% conda create -n ml-agents-20 python=3.8 # 公式マニュアルに3.8が推奨とあったので3.8にしました。
% conda activate ml-agents-20
```

## 各種パッケージのインストール

公式のインストールマニュアルには書いてないのですが、いくつかPythonのパッケージのインストールが必要です。

https://github.com/Unity-Technologies/ml-agents/blob/release_20/docs/Installation.md


以下のパッケージをcondaでインストールしました。

```zsh
% conda install numpy
% conda install pytorch=1.8.0
% conda install h5py
% conda install grpcio
```

上記がインストールできれば、後は公式のインストールマニュアル通り、mlagentsをインストールします。

```zsh
% python -m pip install mlagents==0.30.0
```

## Exampleの動かし方

Exampleを動かすところまで、冒頭のShqnDさんが丁寧に記載していますのでご参照下さい。

## おわりに

まとめてみると大したことはやっていないのですが、ShqnDさんの記事に辿り着くまで、なかなかインストールのエラーが解消されず、かなりハマっていました😭。ようやく動くようになりましたので色々~~遊んで~~勉強してみます。

