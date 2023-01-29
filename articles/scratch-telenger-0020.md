---
title: "Scratchでオリジナルキャラクターを動かそう！ (2) こいつ動くぞ！"
emoji: "🧑‍💻"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["scratch", "CoderDojo", "animation"]
published: true
---

## はじめに

[CoderDojo](https://coderdojo.jp/)というボランティア団体で、子供達のプログラミングスキル習得の支援をしております。プログラミングの開発環境は、主に[Scratch]((https://scratch.mit.edu))を使っていますが、チュートリアルの次のレベルの教材を充実させたいと感じており、本シリーズの執筆を開始しました。

今回はオリジナルキャラクター「デジタル戦隊テレんじゃー」の「テレッド」を色々動かしてみます。

## こいつ動くぞ❗️❗️❗️

今回は矢印キーでテレッドを左右に動かすところまでを目指します。今回の成果物は以下になります。

### Scratchのサイト

1. **[こいつ動くぞ！その場で左右に歩く](https://scratch.mit.edu/projects/727787371/)**
2. **[こいつ動くぞ！矢印キーで動く！](https://scratch.mit.edu/projects/727788493/)**
3. **[こいつブロック定義で動くぞ！](https://scratch.mit.edu/projects/727788755/)**

![こいつ動くぞ！](/images/scratch-telenger-0020/scratch-telenger-0020-walking.gif)

## 左右に歩くアニメーション

[前回](https://zenn.dev/naoji/articles/scratch-telenger-0010)はその場で右に歩くアニメーションまで実装しました。今回は左右に歩くアニメーションを実現したいので前回の内容を参考に、左に歩くアニメーションをコスチュームで追加して下さい。

![コスチューム](/images/scratch-telenger-0020/walking-02-costumes.png)

ここまでできたらコードの方も修正しましょう。とりあえず、旗が押されたら最初のコスチュームを表示して、その後は次のコスチュームを「ずっと」でループさせてみましょう。右に歩く、左に歩くが交互に表示されます。

ここまでできればあとは矢印キーが押されたらアニメーションを表示するように変更すればよさそうですね。

![コード](/images/scratch-telenger-0020/walking-02-code.png)

ここまでのコードは[こちら](https://scratch.mit.edu/projects/727787371/)になります。

## 矢印キーで左右に歩く

矢印キーが押されたかどうかを判定するのは、

- イベントの「キーが押されたとき」を使う
- 「ずっと」ループの中で「もし」の条件でキーが押されたかを判定する

の２つのやり方がありますが、後者の方がスムーズに判定できるので後者を採用します。

![コード](/images/scratch-telenger-0020/walking-03-code.png)

「ずっと」の中に、右向き矢印が押された、左向き矢印が押された、を判定してアニメーションを表示るすロジックにしています。コスチュームを変更し、３歩移動、0.1秒待つ、これらの処理をコスチューム数分（最初の表示＋７回）繰り返すロジックにしています。

ここまでのコードは[こちら](https://scratch.mit.edu/projects/727788493/)になります。

これはこれで悪くないのですが、右に動く、左に動くで同じロジックが２回記述されており、後で修正する際に間違って右だけ直す、といった事態が発生しそうですね。こう言うときに役に立つのがブロック定義（他のコンピュータ言語ですとサブルーチンにあたります）です。

## ブロック定義でメインループをわかりやすく

「動く」と言う名前のブロック定義を作成し、引数に最初のコスチューム、コスチューム数、歩数を設定するように変更しました。「ずっと」のメインループは押されたキーの判定とブロック定義の呼び出しに特化して短くしました。今回のコード量だとあまり有り難みを感じないかもしれませんが、メインループはだいぶスッキリしました。

![コード](/images/scratch-telenger-0020/walking-04-code.png)

最終的なコードは[こちら](https://scratch.mit.edu/projects/727788755/)になります。

## おわりに

お疲れ様でした。まだまだ単純なアニメーションですが、基本的な構造は出来上がりました！後は表現をどんどん追加していくだけです。次はテレッドを跳ばしてみます！

## Scratchでオリジナルキャラクターを動かそう！ インデックス

[(1) テレんじゃー大地に立つ！（アニメーション）](https://zenn.dev/naoji/articles/scratch-telenger-0010)
(2) こいつ動くぞ！（キーボードで動かす）
[(3) 翔べ！テレんじゃー（ジャンプ）](https://zenn.dev/naoji/articles/scratch-telenger-0030)
[(4) 戦場はオフィス（背景を動かす）](https://zenn.dev/naoji/articles/scratch-telenger-0040)
[(5) ハンコの脅威（敵キャラを動かす）](https://zenn.dev/naoji/articles/scratch-telenger-0050)
[(6) 死闘！デジタル・フラッシュ（ビーム発射）](https://zenn.dev/naoji/articles/scratch-telenger-0060)
[(7) オフィスの激戦（当たり判定）](https://zenn.dev/naoji/articles/scratch-telenger-0070)
[(8) ハンコまわし 散る（HPバー）](https://zenn.dev/naoji/articles/scratch-telenger-0080)
