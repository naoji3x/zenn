---
title: "m1 macにTensorFlowをインストール"
emoji: "💻"
type: "tech"
topics: ["mac", "m1", "python", "deeplearning", "tensorflow"]
published: true
---

## はじめに

以下のリンクにあります通り、既に多くの方々がインストールに成功していますが、私の環境にインストールしたときに色々つまづきましたので備忘としてまとめます。

https://qiita.com/chipmunk-star/items/90931fb5180b8024adcb
https://www.mk-tech20.com/tensorflow/
https://storikai.hatenablog.com/entry/2022/05/24/010217

## インストールした環境

16インチ MacBook Pro 2021にインストールしました。スペックは以下になります。

チップ Apple M1 Max
メモリ 32 GB
macOS 13.0.1

## 事前準備

pythonの環境がminicondaでないと上手く動かないという記事が多くありましたので、以前インストールしていたpyenvを削除しました。幸いpythonはそこまでヘビーに使っていなかったのでpyenvからminicondaへの変更も許容範囲でした。

`pyenv versions`で確認すると、3.9.9がインストールされているので、それを削除し、

```zsh
% pyenv versions
  system
* 3.9.9 (set by /Users/[your account]/.pyenv/version) # [your account]はユーザー名になります
% rm -rf /Users/[your account]/.pyenv # [your account]はユーザー名になります
```

pyenvはbrewでインストールしたので以下のコマンドでアンインストールしました。

```zsh
% brew uninstall pyenv
Uninstalling /opt/homebrew/Cellar/pyenv/2.3.3... (932 files, 3MB)
```

また、`.zshrc`から以下のpyenvの設定を削除しました。

```zsh
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/shims:$PATH"
eval "$(pyenv init -)"
```

## コマンドラインツールをインストール

CommandLineToolsをインストールされていない場合は以下のコマンドでインストール。

```zsh
% xcode-select --install
```

## Pythonのインストール

m1 macの場合、Pythonはminiforgeでインストールするのが良いとのことでしたので、以下のサイトから、Miniforge3-MacOSX-arm64.shをダンロードして、

https://github.com/conda-forge/miniforge

以下のコマンドでインストールしました。

```zsh
% bash ~/Downloads/Miniforge3-MacOSX-arm64.sh # 色々聞かれますが、全てyesで回答
```

ちなみに、Appleのページのインストール方法ではMiniforgeではなく、Minicondaへのリンクがありますが、Miniforgeでも問題なく動きました。※Miniforgeは追加のパッケージをconda-forgeからダウンロードするのでライセンス上安心です。

https://developer.apple.com/metal/tensorflow-plugin/

## TensorFlow用の仮想環境の構築

TensorFlow用の仮想環境を構築してそちらにTensorFlowのパッケージをインストールします。`tf29`という名前の仮想環境を作成してアクティベートしました。

```zsh
% conda create -n tf29 python=3.9
% conda activate tf29
```

## TensorFlowのインストール

以下のコマンドでTensorFlowのパッケージをインストールしました。

```zsh
% conda install -c apple tensorflow-deps==2.9.0
% python -m pip install tensorflow-macos==2.9.0
% python -m pip install tensorflow-metal==0.5.0
```

## 稼働確認

AppleのページにあるVerify用のスクリプトを実行ください。色々ワーニングが出ますが以下のように実行が進みます。

```zsh
782/782 [==============================] - 55s 56ms/step - loss: 4.7397 - accuracy: 0.0762n -m pip install tensorflow-metal
Epoch 2/5
782/782 [==============================] - 44s 56ms/step - loss: 4.0085 - accuracy: 0.1392
Epoch 3/5
782/782 [==============================] - 43s 55ms/step - loss: 3.8392 - accuracy: 0.1509
Epoch 4/5
782/782 [==============================] - 45s 58ms/step - loss: 3.4944 - accuracy: 0.2095
Epoch 5/5
782/782 [==============================] - 46s 59ms/step - loss: 3.3775 - accuracy: 0.2211
```

## ハマりポイント

TensorFlowのパッケージをインストールする際に、最後にバージョン（2.9.0, 2.9.0, 0.5.0）をつけないと上手く動きませんでした。特に最後のtensorflow-metalにも付ける必要があったのですが中々わからず、かなりハマりました。

## おわりに

以下のサイトにもあります通り、m1 macはNVIDIAのGPUと比べると遅いようですが、これくらいのスピードが出れば結構使えそうです。

https://take6shin-tech-diary.com/tensorflow_macos/