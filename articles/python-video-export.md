---
title: "Pythonで動画ファイルからGIFアニメーションを作成"
emoji: "🐍"
type: "tech"
topics: ["python", "CoderDojo", "video"]
published: false
---

## はじめに

Scratchで作った作品の解説のために、[youtubeで動画を公開](https://www.youtube.com/channel/UC5Zmd4YgCeQ3OgYmJWLM6cg)し記事にリンクを貼っていましたが、再生に再生ボタンを押すという一手間、と、再生した後におすすめ動画一覧が表示されてしまう点、を改善したかったため、今回、動画をGIFアニメーションに置き換えました。その際、色々な調整を効率化するためPythonのスクリプトで動画を変換するようにしていますのでその手順をまとめます。

## GIFアニメーションとは

GIFは画像のファイルフォーマットの一つで、静止画だけでなくアニメーションも表示できます（詳しくは[こちら](https://ja.wikipedia.org/wiki/GIF%E3%82%A2%E3%83%8B%E3%83%A1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3)）。音声はファイルに保存できない、256色までしか表示できない、等の短所がありますが、古くあるフォーマットなので多くのソフトが対応しています。

## zennでGIFアニメーションを表示する際の注意点

zennではアップロードできるファイルのサイズは最大3MBになっています。GIFアニメーションを作る際は3MBを上回らないようにする調整する必要があります。今回はmacで画面キャプチャした動画(movファイル)をGIFアニメーションに変換しますが、その際に動画の画像の大きさや尺の長さ、１秒あたりのコマ数を調整して、3MBを上回らないように調整しています。

## GIFアニメーションの作成方法

動画ファイルからGIFアニメーションの作成は、

- 無料の変換サイトを利用する
- 変換ソフトを使う
- プログラムを組んで変換する

上記の方法が考えられます。今回は、色々試行錯誤の調整が必要なのと、複数の動画を変換する必要があることから、機械的に実行可能な「プログラムを組んで変換する」を選択しました。幸いPythonのmoviepyで動画編集が簡単にできますので、このライブラリを活用しています。

https://pypi.org/project/moviepy/

## 環境構築

### 最新Python環境の構築

moviepyはPython 3.4以上で動くようですが、念の為、最新のPython環境をcondaで構築しました。Pythonのインストール自体は以下を参照下さい。

https://zenn.dev/naoji/articles/m1-mac-setting-0010

以下のコマンでcondaで環境を構築して、アクティベートしています。

```bash
conda create -n v311 python=3.11 # Python 3.11環境を構築
conda activate v311 # 3.11環境をアクティベート
```

### moviepyとffmpegのインストール

moviepyはPythonの仮想環境を作ってそちらにインストールしました。また、moviepyが内部的にffmpegを利用しており、そちらのインストールも必要でした。

https://ffmpeg.org/

```bash
python -m venv venv # Pythonの仮想環境を構築
source venv/bin/activate # 仮想環境をアクティベート
pip install moviepy # moviepyのインストール
brew install ffmpeg # moviepyが内部で使用するffmpegはbrewでインストール
```

これで環境構築は完了です。後はコードを書くだけです。

## Pythonのコード

moviepyがよくできていますのでPythonのコードは至ってシンプルです。記事一つに対してPythonのスクリプトファイルを１つ作成するようにしました。

```python
from moviepy.editor import VideoFileClip, concatenate_videoclips

# movファイルを読み込んでトリミング（動画その１）
name = "scratch-telenger-0070-1-fighting"
clip = VideoFileClip("../zenn-assets/videos/" + name + ".mov").crop(x1=300,y1=60,x2=1620,y2=1050)
# サイズを変更(横幅を480pxにして縦はアスペクト比固定で自動的に設定)
clip = clip.resize(width=480)
clip1 = clip.subclip(1, 3) # 1秒〜3秒までの動画を切り抜き
clip2 = clip.subclip(18.8, 21) # 18.8秒〜21秒までの動画を切り抜き
clip = concatenate_videoclips([clip1, clip2]) # 上記の動画を繋げ合わせる
# GIFファイルの出力(fps = frames per second, 1秒あたりのコマ数)
clip.write_gif("images/scratch-telenger-0070/" + name + ".gif", fps=15)

# movファイルを読み込んでトリミング（動画その２）
name = "scratch-telenger-0070-2-fighting"
clip = VideoFileClip("../zenn-assets/videos/" + name + ".mov").crop(x1=300,y1=60,x2=1620,y2=1050)
# サイズを変更(横幅を480pxにして縦はアスペクト比固定で自動的に設定)、7秒〜11秒までの動画を切り抜き
clip = clip.resize(width=480).subclip(7, 11) 
# GIFファイルの出力(fps = frames per second, 1秒あたりのコマ数)
clip.write_gif("images/scratch-telenger-0070/" + name + ".gif", fps=15)
```

## GIFアニメーションへの変換結果

上記のコードで変換した動画のオリジナル（YouTube）、と変換後（GIFアニメーション）は以下になります。GIFアニメーションはzennではアップロード3MB制約があるので、尺は数秒が限界ですが、すぐに表示されるのでわかりやすいですね。

### YouTube（その１）

https://youtu.be/ZmOx7AGsP4M

### GIFアニメーション（その１）

![オフィスの激戦](/images/scratch-telenger-0070/scratch-telenger-0070-1-fighting.gif)

### YouTube（その２）

https://youtu.be/YZUWXLYx4Rs

### GIFアニメーション（その２）

![意図しない挙動](/images/scratch-telenger-0070/scratch-telenger-0070-2-fighting.gif)

## おわりに

動画をPythonで簡単に編集できることがわかったので、今後は機械的な編集はPythonを積極的に活用しようと思います！
