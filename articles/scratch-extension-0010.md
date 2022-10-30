---
title: "Scratchを拡張しよう！(1)天気予報を取得"
emoji: "😾"
type: "tech"
topics: ["scratch", "CoderDojo", "javascript"]
published: true
---

## はじめに

[CoderDojo](https://coderdojo.jp/)というボランティア団体で、子供達のプログラミングスキル習得の支援をしております。プログラミングの開発環境は、主に[Scratch]((https://scratch.mit.edu))を使っていますが、標準機能だけでは飽き足らず、このシリーズではScratchの拡張機能開発に挑戦します！

完成したサイトはこちらになります。

**[天気予報拡張機能付きScratch](https://naoji3x.github.io/scratch-gui/)**

![天気予報拡張機能付きScratch](/images/scratch-extension-0010/extension.png)
*ラージサイズ 600px x 372px*

拡張機能から天気予報を追加すると、

- 現在地の天気予報、もしくは、都道府県別の天気予報を取得するブロックが使えるようになります。
- １週間分の天気予報をリストに格納する機能が追加されます。

:::message alert
**一週間分の天気予報を格納するリストですが、リスト名欄にはリストをドラック＆ドロップするのではなく、リストの名前を書き込んで下さい**。
:::

## Scratchの拡張機能開発

Scratchの拡張機能の開発は[Scratch Japan Wiki](https://ja.scratch-wiki.info/wiki/Scratch_3.0%E3%81%AE%E6%8B%A1%E5%BC%B5%E6%A9%9F%E8%83%BD%E3%82%92%E4%BD%9C%E3%81%A3%E3%81%A6%E3%81%BF%E3%82%88%E3%81%86)や[タコキンのPスクール・ブログ](https://p-school.tacoskingdom.com/developer#blog)に丁寧に解説されていますが、色々つまづきポイントもありましたので備忘も含めまとめます。今回は、気軽に天気予報が取得できる[Open Meteo](https://open-meteo.com)から情報を取得して、Scratchで表示する拡張機能を作成します。

https://open-meteo.com

### 下準備

まずは、scratch本家のリポジトリを自分のリポジトリにフォークしてコードを変更できるようにします。以下、２つのリポジトリをフォークします。フォークはGithub上でリポジトリを自分用にコピーする機能で、詳細は[こちら](https://docs.github.com/ja/get-started/quickstart/fork-a-repo)を参照ください。

| リポジトリ | 内容 |
| --- | --- |
| https://github.com/LLK/scratch-vm | スクラッチの実行エンジン |
| https://github.com/LLK/scratch-gui | スクラッチのユーザーインタフェースのリポジトリ |

次に、フォークしたリポジトリをローカルにクローンして開発環境を整えます。
```bash
git clone --depth 1 https://github.com/[GitHubのアカウント]/scratch-vm.git # 1
git clone --depth 1 https://github.com/[GitHubのアカウント]/scratch-gui.git # 2
cd scratch-vm # 3
npm i # 4
npm run build # 5
npm link # 6
cd ../scratch-gui # 7
npm i # 8
npm link scratch-vm # 9
npm start # 10
```

以下に各々のコマンドの意味を説明します；

1. scratch-vmをクローンします。--depth 1はデフォルトブランチの最後のコミットのみをクローンするオプションで、過去の履歴が必要ない場合に指定します（ダウンロードする容量が削減されるため高速化に寄与します）。`[GitHubのアカウント]`には個人のアカウントを指定してください。httpsでクローンする場合は`https://github.com/[GitHubのアカウント]/scratch-vm.git`ですが、SSHの場合は`git@github.com:[GitHubのアカウント]/scratch-vm.git`でクローンして下さい。
2. scratch-guiをクローンします。詳細は1と同様です。
3. scratch-vmディレクトリに移動します。
4. `npm i`は`npm install`の省略形で、scratch-vmに必要なパッケージをインストールします。
5. scratch-vmの実行環境を構築します。※インターネット上の記事ではこのコマンドが省略されていますが、今回、このコマンドを実行しないとブラウザ上でエラーが発生しました。
6. `npm link`でscratch-vmの環境をローカルPC内の他のプロジェクトから参照できるように設定します。後ほど、scratch-guiのプロジェクトからこのローカル環境を参照するように設定します。
7. scratch-guiディレクトリに移動します。
8. scratch-guiに必要なパッケージをインストールします。
9. `link scratch-vm`で今回ダウンロードしたscratch-vmを参照するようにします。この設定をしないと、ローカルのscratch-vmのソースコードの変更がscratch-gui側に反映されません。
10. ローカルでWeb Serverを立ち上げて、scratchをテストできるようにします。

上記後、`http://localhost:8601`にブラウザでアクセスするとお馴染みのScratchの編集画面が立ち上がります。

### scratch-gui側の開発

`scratch-gui/src/lib/libraries/extensions`に`openmeteo`ディレクトリを作りましょう。この中にScratchの拡張機能のアイコンを格納します。ラージサイズのアイコンは600px x 372px, スモールサイズのアイコンは80px x 80pxになります。

![ラージサイズ](/images/scratch-extension-0010/open-meteo.png)
*ラージサイズ 600px x 372px*

![スモールサイズ](/images/scratch-extension-0010/open-meteo-small.png)
*スモールサイズ 80px x 80px*

この後は、ソースコードの修正になります。`scratch-gui/src/lib/libraries/extensions/index.jsx`に以下のコードを追加します。

```javascript
...中略

import gdxforInsetIconURL from './gdxfor/gdxfor-small.svg';
import gdxforConnectionIconURL from './gdxfor/gdxfor-illustration.svg';
import gdxforConnectionSmallIconURL from './gdxfor/gdxfor-small.svg';

import openMeteoIconURL from './openmeteo/open-meteo.png'; // この行を追加
import openMeteoInsetIconURL from './openmeteo/open-meteo-small.png'; // この行を追加

...中略

       connectingMessage: (
            <FormattedMessage
                defaultMessage="Connecting"
                description="Message to help people connect to their force and acceleration sensor."
                id="gui.extension.gdxfor.connectingMessage"
            />
        ),
        helpLink: 'https://scratch.mit.edu/vernier'
    },
    // 最後に以下の行を追加
    {
        name: '天気予報(てんきよほう)',
        extensionId: 'openMeteo',
        iconURL: openMeteoIconURL,
        insetIconURL: openMeteoInsetIconURL,
        description: '天気予報を取得します（てんきよほうをしゅとくします）',
        internetConnectionRequired: true,
        featured: true
    }
    // ここまで
];
```

`index.jsx`には`拡張機能を選ぶの画面`で表示する内容を設定します。`openmeteo`ディレクトリに格納した画像のURLとその他各種表示情報を設定します。本当は、多言語対応、ひらがな表示対応まで設定したかったのですが、色々大変そうなため今回は日本語表示のみにしています。

### scratch-vm側の開発

次に拡張機能のロジック本体を開発します。こちらはscratch-vm側を改造することになります。

先ずはscratchの開発でasync/awaitが使えるように以下のパッケージを追加します（[こちら](https://p-school.tacoskingdom.com/blog/65)を参考にしました）。この設定は必須ではありませんが、コードの見通しが良くなるのでオススメです。以下、async/awaitが使える前提でコーディングしています。

```bash
cd ../scratch-vm
npm i @babel/runtime @babel/plugin-transform-runtime -D
```

`src/virtual-machine.js`にの先頭に以下を追加するとasync/awaitが使えるようになります。

```js
require('core-js');
require('regenerator-runtime/runtime');
```

次に拡張機能のアイコンを準備します。サイズは40px x 40pxで、メニュー用とブロック用の２つを準備します。

![メニューアイコン](/images/scratch-extension-0010/icons.png)
*メニューアイコン、ブロックアイコン*

上記のアイコンはソースコードに埋め込みますので、[こちらのサイト](https://lab.syncer.jp/Tool/Base64-encode/)等でbase64にエンコードして下さい（このあたりも[タコキンのPスクール・ブログ](https://p-school.tacoskingdom.com/blog/39)に詳しく記載されています）。

いよいよ拡張機能の開発です。`src/extensions`ディレクトリにscratch3_open_meteoディレクトリを作成し、以下のファイルを追加してコードを記述下さい。

#### index.js

拡張機能のメイン処理が書かれています。以下の機能をブロックとして公開しています。blockIconURI, menuIconURIにはbase64にエンコードしたアイコンがコピペされています。

- `getPrefectureWeather`で都道府県の天気を取得
- `getWeather`で現在地の天気を取得
- `listPrefectureWeather`で都道府県の一週間分の天気を取得しリストに格納
- `listWether`で現在地の一週間分の天気を取得しリストに格納

全体のソースコードの構造は、[Scratch 3.0の拡張機能を作ってみよう/基本の書式](https://ja.scratch-wiki.info/wiki/Scratch_3.0%E3%81%AE%E6%8B%A1%E5%BC%B5%E6%A9%9F%E8%83%BD%E3%82%92%E4%BD%9C%E3%81%A3%E3%81%A6%E3%81%BF%E3%82%88%E3%81%86/%E5%9F%BA%E6%9C%AC%E3%81%AE%E6%9B%B8%E5%BC%8F)を、リストからのデータ取得は[Scratch Extensionをつくってわかったこと](https://qiita.com/yume_yu/items/c7b96fc278771a80a0e5)を参考に作成しています。

```javascript
const ArgumentType = require('../../extension-support/argument-type');
const BlockType = require('../../extension-support/block-type');
const Cast = require('../../util/cast');
const Variable = require('../../engine/variable');
const prefectureLocations = require('./prefecture-locations');

/**
 * Icon svg to be displayed at the left edge of each extension block, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const blockIconURI = 'data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+Cjxzdmcgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgdmlld0JveD0iMCAwIDQwIDQwIiB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHhtbDpzcGFjZT0icHJlc2VydmUiIHhtbG5zOnNlcmlmPSJodHRwOi8vd3d3LnNlcmlmLmNvbS8iIHN0eWxlPSJmaWxsLXJ1bGU6ZXZlbm9kZDtjbGlwLXJ1bGU6ZXZlbm9kZDtzdHJva2UtbGluZWpvaW46cm91bmQ7c3Ryb2tlLW1pdGVybGltaXQ6MjsiPgogICAgPGcgdHJhbnNmb3JtPSJtYXRyaXgoMSwwLDAsMSwtNjEwLC05MCkiPgogICAgICAgIDxnIGlkPSJibG9jay1pY29uIiB0cmFuc2Zvcm09Im1hdHJpeCgxLDAsMCwwLjk1MjM4MSwwLDMuMzMzMzMpIj4KICAgICAgICAgICAgPHJlY3QgeD0iNjEwIiB5PSI5MSIgd2lkdGg9IjQwIiBoZWlnaHQ9IjQyIiBzdHlsZT0iZmlsbDpub25lOyIvPgogICAgICAgICAgICA8ZyB0cmFuc2Zvcm09Im1hdHJpeCgwLjEwNjkxNiwwLDAsMC4xNDk2ODIsNjA0LjM0LDg1LjA1NzIpIj4KICAgICAgICAgICAgICAgIDxnIHRyYW5zZm9ybT0ibWF0cml4KDE5Ljg3MjYsMCwwLDE0LjkwNDUsODEuMDQxNiw1My4zMTIxKSI+CiAgICAgICAgICAgICAgICAgICAgPHBhdGggZD0iTTcsOEM3LDggNyw4IDcsOEM4LjkyLDggMTAuNSw5LjU4IDEwLjUsMTEuNUMxMC41LDExLjUxOCAxMC41LDExLjUzNyAxMC41LDExLjU1NUMxMC41LDExLjU1OCAxMC41LDExLjU2IDEwLjUsMTEuNTYzQzEwLjUsMTEuODM3IDEwLjcyNiwxMi4wNjMgMTEsMTIuMDYzQzExLjA0MiwxMi4wNjMgMTEuMDgzLDEyLjA1NyAxMS4xMjQsMTIuMDQ3QzExLjI0NiwxMi4wMTYgMTEuMzcxLDEyIDExLjQ5NywxMkMxMi4zMiwxMiAxMi45OTgsMTIuNjc3IDEzLDEzLjVDMTMsMTQuMzIzIDEyLjMyMywxNSAxMS41LDE1TDMsMTVDMS45MDcsMTQuOTk0IDEuMDExLDE0LjA5MyAxLjAxMSwxM0MxLjAxMSwxMS45MDMgMS45MTQsMTEgMy4wMTEsMTFDMy4wNDEsMTEgMy4wNywxMS4wMDEgMy4xLDExLjAwMkMzLjMzNywxMS4wMTQgMy41NTEsMTAuODU3IDMuNjEsMTAuNjI3QzQuMDA4LDkuMDg2IDUuNDA4LDggNyw4Wk0xMS40NzMsMTFDMTEuMjIxLDguNzMyIDkuMjgyLDYuOTk2IDcsNi45OTZDNS4wOTMsNi45OTYgMy4zODMsOC4yMDkgMi43NTMsMTAuMDFDMS4yMDUsMTAuMTM3IC0wLjAwMiwxMS40NDYgLTAuMDAyLDEzQy0wLjAwMiwxNC42NDYgMS4zNTIsMTYgMi45OTgsMTZDMi45OTgsMTYgMi45OTksMTYgMywxNkwxMS41LDE2QzEyLjg3MSwxNiAxNCwxNC44NzEgMTQsMTMuNUMxNCwxMi4xMjkgMTIuODcxLDExIDExLjUsMTFMMTEuNDczLDExWiIgc3R5bGU9ImZpbGw6d2hpdGU7ZmlsbC1ydWxlOm5vbnplcm87Ii8+CiAgICAgICAgICAgICAgICA8L2c+CiAgICAgICAgICAgICAgICA8ZyB0cmFuc2Zvcm09Im1hdHJpeCgxOS44NzI2LDAsMCwxNC45MDQ1LDgxLjA0MTYsNTMuMzEyMSkiPgogICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik0xMC41LDEuNUMxMC41LDEuMjI2IDEwLjI3NCwxIDEwLDFDOS43MjYsMSA5LjUsMS4yMjYgOS41LDEuNUw5LjUsMi41QzkuNSwyLjc3NCA5LjcyNiwzIDEwLDNDMTAuMjc0LDMgMTAuNSwyLjc3NCAxMC41LDIuNUwxMC41LDEuNVpNMTQuMjQzLDMuNDY0QzE0LjM0MSwzLjM3IDE0LjM5NiwzLjI0IDE0LjM5NiwzLjEwNEMxNC4zOTYsMi44MyAxNC4xNywyLjYwNCAxMy44OTYsMi42MDRDMTMuNzYsMi42MDQgMTMuNjMsMi42NTkgMTMuNTM2LDIuNzU3TDEyLjgyOCwzLjQ2NEMxMi43MzQsMy41NTggMTIuNjgxLDMuNjg1IDEyLjY4MSwzLjgxOEMxMi42ODEsNC4wOTMgMTIuOTA3LDQuMzE5IDEzLjE4Miw0LjMxOUMxMy4zMTUsNC4zMTkgMTMuNDQyLDQuMjY2IDEzLjUzNiw0LjE3MkwxNC4yNDMsMy40NjRaTTYuNDY0LDIuNzU3QzYuMzcxLDIuNjY3IDYuMjQ2LDIuNjE3IDYuMTE3LDIuNjE3QzUuODQyLDIuNjE3IDUuNjE3LDIuODQyIDUuNjE3LDMuMTE3QzUuNjE3LDMuMjQ2IDUuNjY3LDMuMzcxIDUuNzU3LDMuNDY0TDYuNDY0LDQuMTcyQzYuNTU4LDQuMjY2IDYuNjg1LDQuMzE5IDYuODE4LDQuMzE5QzcuMDkzLDQuMzE5IDcuMzE5LDQuMDkzIDcuMzE5LDMuODE4QzcuMzE5LDMuNjg1IDcuMjY2LDMuNTU4IDcuMTcyLDMuNDY0TDYuNDY0LDIuNzU3Wk04LjE5OCw2LjEzMUM4LjUzMSw1LjQ0MSA5LjIzMyw1IDkuOTk5LDVDMTEuMDk2LDUgMTEuOTk5LDUuOTAzIDExLjk5OSw3QzExLjk5OSw3LjQ5IDExLjgxOSw3Ljk2MyAxMS40OTQsOC4zMjlDMTEuNjkzLDguNjEgMTEuODY2LDguOTExIDEyLjAxLDkuMjI3QzEyLjYzOSw4LjY1OCAxMi45OTksNy44NDkgMTIuOTk5LDcuMDAxQzEyLjk5OSw1LjM1NSAxMS42NDUsNC4wMDEgOS45OTksNC4wMDFDOC43Myw0LjAwMSA3LjU5Miw0LjgwNiA3LjE3LDYuMDAyQzcuNTIyLDYuMDEzIDcuODY2LDYuMDU3IDguMTk4LDYuMTMxWk0xMi42ODIsMTAuMjA1QzEzLjI4MiwxMC40MiAxMy44MDcsMTAuNzk1IDE0LjIwNCwxMS4yNzdDMTQuMzIxLDExLjE4MiAxNC4zODksMTEuMDM5IDE0LjM4OSwxMC44ODhDMTQuMzg5LDEwLjc1NiAxNC4zMzcsMTAuNjI5IDE0LjI0MywxMC41MzVMMTMuNTM2LDkuODI4QzEzLjQ0Miw5LjczNCAxMy4zMTQsOS42ODEgMTMuMTgxLDkuNjgxQzEyLjkwNyw5LjY4MSAxMi42ODEsOS45MDYgMTIuNjgxLDEwLjE4MUMxMi42ODEsMTAuMTg5IDEyLjY4MiwxMC4xOTcgMTIuNjgyLDEwLjIwNVpNMTQuNSw2LjVDMTQuMjI2LDYuNSAxNCw2LjcyNiAxNCw3QzE0LDcuMjc0IDE0LjIyNiw3LjUgMTQuNSw3LjVMMTUuNSw3LjVDMTUuNzc0LDcuNSAxNiw3LjI3NCAxNiw3QzE2LDYuNzI2IDE1Ljc3NCw2LjUgMTUuNSw2LjVMMTQuNSw2LjVaIiBzdHlsZT0iZmlsbDp3aGl0ZTtmaWxsLXJ1bGU6bm9uemVybzsiLz4KICAgICAgICAgICAgICAgIDwvZz4KICAgICAgICAgICAgPC9nPgogICAgICAgIDwvZz4KICAgIDwvZz4KPC9zdmc+Cg==';

/**
 * Icon svg to be displayed in the category menu, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const menuIconURI = 'data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+Cjxzdmcgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgdmlld0JveD0iMCAwIDQwIDQwIiB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHhtbDpzcGFjZT0icHJlc2VydmUiIHhtbG5zOnNlcmlmPSJodHRwOi8vd3d3LnNlcmlmLmNvbS8iIHN0eWxlPSJmaWxsLXJ1bGU6ZXZlbm9kZDtjbGlwLXJ1bGU6ZXZlbm9kZDtzdHJva2UtbGluZWpvaW46cm91bmQ7c3Ryb2tlLW1pdGVybGltaXQ6MjsiPgogICAgPGcgdHJhbnNmb3JtPSJtYXRyaXgoMSwwLDAsMSwtNjEwLC0xNDApIj4KICAgICAgICA8ZyBpZD0ibWVudS1pY29uIiB0cmFuc2Zvcm09Im1hdHJpeCgxLDAsMCwwLjk1MjM4MSwwLDUzLjMzMzMpIj4KICAgICAgICAgICAgPHJlY3QgeD0iNjEwIiB5PSI5MSIgd2lkdGg9IjQwIiBoZWlnaHQ9IjQyIiBzdHlsZT0iZmlsbDpub25lOyIvPgogICAgICAgICAgICA8Y2xpcFBhdGggaWQ9Il9jbGlwMSI+CiAgICAgICAgICAgICAgICA8cmVjdCB4PSI2MTAiIHk9IjkxIiB3aWR0aD0iNDAiIGhlaWdodD0iNDIiLz4KICAgICAgICAgICAgPC9jbGlwUGF0aD4KICAgICAgICAgICAgPGcgY2xpcC1wYXRoPSJ1cmwoI19jbGlwMSkiPgogICAgICAgICAgICAgICAgPGcgdHJhbnNmb3JtPSJtYXRyaXgoMSwwLDAsMS4wNSwwLC01NikiPgogICAgICAgICAgICAgICAgICAgIDxjaXJjbGUgY3g9IjYzMCIgY3k9IjE2MCIgcj0iMjAiIHN0eWxlPSJmaWxsOnJnYigwLDE5NSwyNTUpOyIvPgogICAgICAgICAgICAgICAgPC9nPgogICAgICAgICAgICAgICAgPGcgdHJhbnNmb3JtPSJtYXRyaXgoMC4xMzQxODgsMCwwLDAuMTg3ODYzLDU5Mi4wODIsODMuMTA0NikiPgogICAgICAgICAgICAgICAgICAgIDxnIHRyYW5zZm9ybT0ibWF0cml4KDE5Ljg3MjYsMCwwLDE0LjkwNDUsODEuMDQxNiw1My4zMTIxKSI+CiAgICAgICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik03LDhDNyw4IDcsOCA3LDhDOC45Miw4IDEwLjUsOS41OCAxMC41LDExLjVDMTAuNSwxMS41MTggMTAuNSwxMS41MzcgMTAuNSwxMS41NTVDMTAuNSwxMS41NTggMTAuNSwxMS41NiAxMC41LDExLjU2M0MxMC41LDExLjgzNyAxMC43MjYsMTIuMDYzIDExLDEyLjA2M0MxMS4wNDIsMTIuMDYzIDExLjA4MywxMi4wNTcgMTEuMTI0LDEyLjA0N0MxMS4yNDYsMTIuMDE2IDExLjM3MSwxMiAxMS40OTcsMTJDMTIuMzIsMTIgMTIuOTk4LDEyLjY3NyAxMywxMy41QzEzLDE0LjMyMyAxMi4zMjMsMTUgMTEuNSwxNUwzLDE1QzEuOTA3LDE0Ljk5NCAxLjAxMSwxNC4wOTMgMS4wMTEsMTNDMS4wMTEsMTEuOTAzIDEuOTE0LDExIDMuMDExLDExQzMuMDQxLDExIDMuMDcsMTEuMDAxIDMuMSwxMS4wMDJDMy4zMzcsMTEuMDE0IDMuNTUxLDEwLjg1NyAzLjYxLDEwLjYyN0M0LjAwOCw5LjA4NiA1LjQwOCw4IDcsOFpNMTEuNDczLDExQzExLjIyMSw4LjczMiA5LjI4Miw2Ljk5NiA3LDYuOTk2QzUuMDkzLDYuOTk2IDMuMzgzLDguMjA5IDIuNzUzLDEwLjAxQzEuMjA1LDEwLjEzNyAtMC4wMDIsMTEuNDQ2IC0wLjAwMiwxM0MtMC4wMDIsMTQuNjQ2IDEuMzUyLDE2IDIuOTk4LDE2QzIuOTk4LDE2IDIuOTk5LDE2IDMsMTZMMTEuNSwxNkMxMi44NzEsMTYgMTQsMTQuODcxIDE0LDEzLjVDMTQsMTIuMTI5IDEyLjg3MSwxMSAxMS41LDExTDExLjQ3MywxMVoiIHN0eWxlPSJmaWxsOndoaXRlO2ZpbGwtcnVsZTpub256ZXJvOyIvPgogICAgICAgICAgICAgICAgICAgIDwvZz4KICAgICAgICAgICAgICAgICAgICA8ZyB0cmFuc2Zvcm09Im1hdHJpeCgxOS44NzI2LDAsMCwxNC45MDQ1LDgxLjA0MTYsNTMuMzEyMSkiPgogICAgICAgICAgICAgICAgICAgICAgICA8cGF0aCBkPSJNMTAuNSwxLjVDMTAuNSwxLjIyNiAxMC4yNzQsMSAxMCwxQzkuNzI2LDEgOS41LDEuMjI2IDkuNSwxLjVMOS41LDIuNUM5LjUsMi43NzQgOS43MjYsMyAxMCwzQzEwLjI3NCwzIDEwLjUsMi43NzQgMTAuNSwyLjVMMTAuNSwxLjVaTTE0LjI0MywzLjQ2NEMxNC4zNDEsMy4zNyAxNC4zOTYsMy4yNCAxNC4zOTYsMy4xMDRDMTQuMzk2LDIuODMgMTQuMTcsMi42MDQgMTMuODk2LDIuNjA0QzEzLjc2LDIuNjA0IDEzLjYzLDIuNjU5IDEzLjUzNiwyLjc1N0wxMi44MjgsMy40NjRDMTIuNzM0LDMuNTU4IDEyLjY4MSwzLjY4NSAxMi42ODEsMy44MThDMTIuNjgxLDQuMDkzIDEyLjkwNyw0LjMxOSAxMy4xODIsNC4zMTlDMTMuMzE1LDQuMzE5IDEzLjQ0Miw0LjI2NiAxMy41MzYsNC4xNzJMMTQuMjQzLDMuNDY0Wk02LjQ2NCwyLjc1N0M2LjM3MSwyLjY2NyA2LjI0NiwyLjYxNyA2LjExNywyLjYxN0M1Ljg0MiwyLjYxNyA1LjYxNywyLjg0MiA1LjYxNywzLjExN0M1LjYxNywzLjI0NiA1LjY2NywzLjM3MSA1Ljc1NywzLjQ2NEw2LjQ2NCw0LjE3MkM2LjU1OCw0LjI2NiA2LjY4NSw0LjMxOSA2LjgxOCw0LjMxOUM3LjA5Myw0LjMxOSA3LjMxOSw0LjA5MyA3LjMxOSwzLjgxOEM3LjMxOSwzLjY4NSA3LjI2NiwzLjU1OCA3LjE3MiwzLjQ2NEw2LjQ2NCwyLjc1N1pNOC4xOTgsNi4xMzFDOC41MzEsNS40NDEgOS4yMzMsNSA5Ljk5OSw1QzExLjA5Niw1IDExLjk5OSw1LjkwMyAxMS45OTksN0MxMS45OTksNy40OSAxMS44MTksNy45NjMgMTEuNDk0LDguMzI5QzExLjY5Myw4LjYxIDExLjg2Niw4LjkxMSAxMi4wMSw5LjIyN0MxMi42MzksOC42NTggMTIuOTk5LDcuODQ5IDEyLjk5OSw3LjAwMUMxMi45OTksNS4zNTUgMTEuNjQ1LDQuMDAxIDkuOTk5LDQuMDAxQzguNzMsNC4wMDEgNy41OTIsNC44MDYgNy4xNyw2LjAwMkM3LjUyMiw2LjAxMyA3Ljg2Niw2LjA1NyA4LjE5OCw2LjEzMVpNMTIuNjgyLDEwLjIwNUMxMy4yODIsMTAuNDIgMTMuODA3LDEwLjc5NSAxNC4yMDQsMTEuMjc3QzE0LjMyMSwxMS4xODIgMTQuMzg5LDExLjAzOSAxNC4zODksMTAuODg4QzE0LjM4OSwxMC43NTYgMTQuMzM3LDEwLjYyOSAxNC4yNDMsMTAuNTM1TDEzLjUzNiw5LjgyOEMxMy40NDIsOS43MzQgMTMuMzE0LDkuNjgxIDEzLjE4MSw5LjY4MUMxMi45MDcsOS42ODEgMTIuNjgxLDkuOTA2IDEyLjY4MSwxMC4xODFDMTIuNjgxLDEwLjE4OSAxMi42ODIsMTAuMTk3IDEyLjY4MiwxMC4yMDVaTTE0LjUsNi41QzE0LjIyNiw2LjUgMTQsNi43MjYgMTQsN0MxNCw3LjI3NCAxNC4yMjYsNy41IDE0LjUsNy41TDE1LjUsNy41QzE1Ljc3NCw3LjUgMTYsNy4yNzQgMTYsN0MxNiw2LjcyNiAxNS43NzQsNi41IDE1LjUsNi41TDE0LjUsNi41WiIgc3R5bGU9ImZpbGw6d2hpdGU7ZmlsbC1ydWxlOm5vbnplcm87Ii8+CiAgICAgICAgICAgICAgICAgICAgPC9nPgogICAgICAgICAgICAgICAgPC9nPgogICAgICAgICAgICA8L2c+CiAgICAgICAgPC9nPgogICAgPC9nPgo8L3N2Zz4K';

/**
 * Class for the new blocks in Scratch 3.0
 * @param {Runtime} runtime - the runtime instantiating this block package.
 * @constructor
 */
class Scratch3OpenMeteoBlocks {
    constructor (runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {Runtime}
         */
        this.runtime = runtime;
    }

    getWeatherDescription (code = -1) {
        switch (code) {
        case 0: return '快晴';
        case 1: return '晴れ';
        case 2: return '晴れ時々曇り';
        case 3: return '曇り';
        case 45: return '霧';
        case 48: return '霧';
        case 51: return '弱い霧雨';
        case 53: return '霧雨';
        case 55: return '強い霧雨';
        case 56: return '寒い霧雨';
        case 57: return '凍える霧雨';
        case 61: return '小雨';
        case 63: return '雨';
        case 65: return '豪雨';
        case 66: return '寒い雨';
        case 67: return '凍える雨';
        case 71: return '弱い雪';
        case 73: return '雪';
        case 75: return '強い雪';
        case 77: return '霧雪';
        case 80: return '弱いにわか雨';
        case 81: return 'にわか雨';
        case 82: return '強いにわか雨';
        case 85: return '弱いにわか雪';
        case 86: return '強いにわか雪';
        case 95: return '雷雨';
        case 96: return '雷雨';
        case 99: return '強い雷雨';
        default: return '不明';
        }
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo () {
        return {
            id: 'openMeteo',
            name: '天気',
            menuIconURI: menuIconURI,
            blockIconURI: blockIconURI,
            blocks: [
                {
                    opcode: 'listWeather',
                    text: '天気予報の日付を[DATE_LIST]に、天気を[WEATHER_LIST]に格納する',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        DATE_LIST: {
                            type: ArgumentType.STRING,
                            defaultValue: 'リスト名'
                        },
                        WEATHER_LIST: {
                            type: ArgumentType.STRING,
                            defaultValue: 'リスト名'
                        }
                    }
                },
                {
                    opcode: 'listPrefectureWeather',
                    text: '[PREFECTURE]の天気予報の日付を[DATE_LIST]に、天気を[WEATHER_LIST]に格納する',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        PREFECTURE: {
                            type: ArgumentType.NUMBER,
                            menu: 'prefectureMenu',
                            defaultValue: 0
                        },
                        DATE_LIST: {
                            type: ArgumentType.STRING,
                            defaultValue: 'リスト名'
                        },
                        WEATHER_LIST: {
                            type: ArgumentType.STRING,
                            defaultValue: 'リスト名'
                        }
                    }
                },
                {
                    opcode: 'getWeather',
                    text: '[OFFSET]日後の天気を取得',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        OFFSET: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    }
                },
                {
                    opcode: 'getPrefectureWeather',
                    text: '[PREFECTURE]の[OFFSET]日後の天気を取得',
                    blockType: BlockType.REPORTER,
                    arguments: {
                        PREFECTURE: {
                            type: ArgumentType.NUMBER,
                            menu: 'prefectureMenu',
                            defaultValue: 0
                        },
                        OFFSET: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 1
                        }
                    }
                }
            ],
            menus: {
                prefectureMenu: {
                    acceptReporters: true,
                    items: prefectureLocations.map((loc, index) => ({
                        text: loc.prefecture,
                        value: index
                    }))
                }
            }
        };
    }

    async fetchWeather (latitude, longitude) {
        const prefix = 'https://api.open-meteo.com/v1/forecast?';
        const suffix = '&daily=weathercode&timezone=Asia%2FTokyo';

        const url = `${prefix}latitude=${latitude}&longitude=${longitude}${suffix}`;
        const res = await fetch(url);
        const result = await res.json();

        return result.daily;
    }

    async getPointWeather (latitude, longitude, offset) {
        const res = await this.fetchWeather(latitude, longitude);
        const weathercodes = res.weathercode;

        if (offset >= 0 && offset < weathercodes.length) {
            return this.getWeatherDescription(weathercodes[offset]);
        }
        return this.getWeatherDescription();
    }

    async getCurrentLocationWether (offset) {
        const position = await new Promise((resolve, reject) =>
            navigator.geolocation.getCurrentPosition(resolve, reject));
        return await this.getPointWeather(position.coords.latitude, position.coords.longitude, offset);
    }

    setList (list, array) {
        list.value = array;
        list._monitorUpToDate = false;
    }

    // 指定した県の日付指定の天気を取得
    getPrefectureWeather (args) {
        const index = Cast.toNumber(args.PREFECTURE);
        const loc = prefectureLocations[index];
        return this.getPointWeather(loc.latitude, loc.longitude, Cast.toNumber(args.OFFSET));
    }


    // 現在地の日付指定の天気を取得
    getWeather (args) {
        return this.getCurrentLocationWether(Cast.toNumber(args.OFFSET));
    }

    // 指定した県の一週間分の天気を取得
    async listPrefectureWeather (args, util) {
        const dateListName = Cast.toString(args.DATE_LIST);
        const weatherListName = Cast.toString(args.WEATHER_LIST);

        const dateList = util.target.lookupVariableByNameAndType(dateListName, Variable.LIST_TYPE);
        const weatherList = util.target.lookupVariableByNameAndType(weatherListName, Variable.LIST_TYPE);

        let res;
        if (dateList || weatherList) {
            const index = Cast.toNumber(args.PREFECTURE);
            const loc = prefectureLocations[index];
            res = await this.fetchWeather(loc.latitude, loc.longitude);
        }

        if (dateList) this.setList(dateList, res.time);
        if (weatherList) this.setList(weatherList, res.weathercode.map(wc => this.getWeatherDescription(wc)));
    }


    // 現在地の一週間分の天気を取得
    async listWeather (args, util) {
        const dateListName = Cast.toString(args.DATE_LIST);
        const weatherListName = Cast.toString(args.WEATHER_LIST);

        const dateList = util.target.lookupVariableByNameAndType(dateListName, Variable.LIST_TYPE);
        const weatherList = util.target.lookupVariableByNameAndType(weatherListName, Variable.LIST_TYPE);

        let res;
        if (dateList || weatherList) {
            const position = await new Promise((resolve, reject) =>
                navigator.geolocation.getCurrentPosition(resolve, reject));
            res = await this.fetchWeather(position.coords.latitude, position.coords.longitude);
        }

        if (dateList) this.setList(dateList, res.time);
        if (weatherList) this.setList(weatherList, res.weathercode.map(wc => this.getWeatherDescription(wc)));
    }
}

module.exports = Scratch3OpenMeteoBlocks;
```

#### prefecture-locations.js

都道府県の緯度、経度データになります。[やじろべえ](https://techtech-sorae.com/jp_city_latlon/)さんのサイトのcsvデータをjsonに変換して取り込みました。

```javascript
const prefectureLocations = [
    {
        prefecture: '北海道',
        latitude: 43.064359,
        longitude: 141.347449
    },
    {
        prefecture: '青森県',
        latitude: 40.824294,
        longitude: 140.74005
    },
    {
        prefecture: '岩手県',
        latitude: 39.70353,
        longitude: 141.152667
    },
    {
        prefecture: '宮城県',
        latitude: '38.268737',
        longitude: '140.872183'
    },
    {
        prefecture: '秋田県',
        latitude: 39.718175,
        longitude: 140.103356
    },
    {
        prefecture: '山形県',
        latitude: 38.240127,
        longitude: 140.362533
    },
    {
        prefecture: '福島県',
        latitude: 37.750146,
        longitude: 140.466754
    },
    {
        prefecture: '茨城県',
        latitude: 36.341817,
        longitude: 140.446796
    },
    {
        prefecture: '栃木県',
        latitude: 36.56575,
        longitude: 139.883526
    },
    {
        prefecture: '群馬県',
        latitude: 36.391205,
        longitude: 139.060917
    },
    {
        prefecture: '埼玉県',
        latitude: 35.857771,
        longitude: 139.647804
    },
    {
        prefecture: '千葉県',
        latitude: 35.604563,
        longitude: 140.123179
    },
    {
        prefecture: '東京都',
        latitude: 35.689185,
        longitude: 139.691648
    },
    {
        prefecture: '神奈川県',
        latitude: 35.447505,
        longitude: 139.642347
    },
    {
        prefecture: '新潟県',
        latitude: 37.901699,
        longitude: 139.022728
    },
    {
        prefecture: '富山県',
        latitude: 36.695274,
        longitude: 137.211302
    },
    {
        prefecture: '石川県',
        latitude: 36.594729,
        longitude: 136.62555
    },
    {
        prefecture: '福井県',
        latitude: 36.06522,
        longitude: 136.221641
    },
    {
        prefecture: '山梨県',
        latitude: 35.665102,
        longitude: 138.568985
    },
    {
        prefecture: '長野県',
        latitude: 36.651282,
        longitude: 138.180972
    },
    {
        prefecture: '岐阜県',
        latitude: 35.39116,
        longitude: 136.722204
    },
    {
        prefecture: '静岡県',
        latitude: 34.976987,
        longitude: 138.383057
    },
    {
        prefecture: '愛知県',
        latitude: 35.180247,
        longitude: 136.906698
    },
    {
        prefecture: '三重県',
        latitude: 34.730547,
        longitude: 136.50861
    },
    {
        prefecture: '滋賀県',
        latitude: 35.004532,
        longitude: 135.868588
    },
    {
        prefecture: '京都県',
        latitude: 35.0209962,
        longitude: 135.7531135
    },
    {
        prefecture: '大阪府',
        latitude: 34.686492,
        longitude: 135.518992
    },
    {
        prefecture: '兵庫県',
        latitude: 34.69128,
        longitude: 135.183087
    },
    {
        prefecture: '奈良県',
        latitude: 34.685296,
        longitude: 135.832745
    },
    {
        prefecture: '和歌山県',
        latitude: 34.224806,
        longitude: 135.16795
    },
    {
        prefecture: '鳥取県',
        latitude: 35.503463,
        longitude: 134.238258
    },
    {
        prefecture: '島根県',
        latitude: 35.472248,
        longitude: 133.05083
    },
    {
        prefecture: '岡山県',
        latitude: 34.66132,
        longitude: 133.934414
    },
    {
        prefecture: '広島県',
        latitude: 34.396033,
        longitude: 132.459595
    },
    {
        prefecture: '山口県',
        latitude: 34.185648,
        longitude: 131.470755
    },
    {
        prefecture: '徳島県',
        latitude: '34.065732',
        longitude: '134.559293'
    },
    {
        prefecture: '香川県',
        latitude: 34.34014,
        longitude: 134.04297
    },
    {
        prefecture: '愛媛県',
        latitude: 33.841649,
        longitude: 132.76585
    },
    {
        prefecture: '高知県',
        latitude: 33.55969,
        longitude: 133.530887
    },
    {
        prefecture: '福岡県',
        latitude: 33.606767,
        longitude: 130.418228
    },
    {
        prefecture: '佐賀県',
        latitude: 33.249367,
        longitude: 130.298822
    },
    {
        prefecture: '長崎県',
        latitude: 32.744542,
        longitude: 129.873037
    },
    {
        prefecture: '熊本県',
        latitude: 32.790385,
        longitude: 130.742345
    },
    {
        prefecture: '大分県',
        latitude: 33.2382,
        longitude: 131.612674
    },
    {
        prefecture: '宮崎県',
        latitude: 31.91109,
        longitude: 131.423855
    },
    {
        prefecture: '鹿児島県',
        latitude: 31.560219,
        longitude: 130.557906
    },
    {
        prefecture: '沖縄県',
        latitude: 26.211538,
        longitude: 127.681115
    }
];

module.exports = prefectureLocations;
```

#### extension-manager.jsへの登録

上記のコードをScratch-vmに登録します。`src/extension-support/extension-manager.js`を以下のように修正します。

```javascript
...中略
const builtinExtensions = {
    // This is an example that isn't loaded with the other core blocks,
    // but serves as a reference for loading core blocks as extensions.
    coreExample: () => require('../blocks/scratch3_core_example'),
    // These are the non-core built-in extensions.
    pen: () => require('../extensions/scratch3_pen'),
    wedo2: () => require('../extensions/scratch3_wedo2'),
    music: () => require('../extensions/scratch3_music'),
    microbit: () => require('../extensions/scratch3_microbit'),
    text2speech: () => require('../extensions/scratch3_text2speech'),
    translate: () => require('../extensions/scratch3_translate'),
    videoSensing: () => require('../extensions/scratch3_video_sensing'),
    ev3: () => require('../extensions/scratch3_ev3'),
    makeymakey: () => require('../extensions/scratch3_makeymakey'),
    boost: () => require('../extensions/scratch3_boost'),
    gdxfor: () => require('../extensions/scratch3_gdx_for'),
    openMeteo: () => require('../extensions/scratch3_open_meteo') // <- この行を追加
};
...中略
```


### テスト

以下のコマンドを実行後、`http://localhost:8601`にブラウザでアクセスするとお馴染みのScratchのサイトから拡張機能を確認できます。ソースコードの変更がリアルタイムに反映されますので効率的にデバッグできます。

```bash
cd ../scratch-gui
npm start
```

### GitHub Pagesでの公開

以上のscratch-vm, scratch-guiの変更をGitHubにpushします。GitHubのデフォルトブランチはdevelopになっていますが、新しいブランチを作成して、そちらをデフォルトブランチに設定して開発を進めるのがオススメです（developブランチは本家のscratch-vm, scratch-guiの変更が反映されていきますので）。

ここまでできれば、以下のコマンドで作成した拡張機能をGitHub Pagesに公開しましょう。

```bash
cd ../scratch-vm
npm i
npm run build # 念のためscratch-vm側もbuild
cd ../scratch-gui
npm run build
npm run deploy
```

上記で、`https://[GitHubのアカウント].github.io/scratch-gui/`に拡張機能付きのScratchが公開されます。

## おわりに

既に多くの方々がScratchの拡張に挑戦していますのでインターネット上に多くの有益な情報があり大変助かりました！今回は直接Scratchのコードをフォークして拡張しましたが、[Xcratch](https://github.com/xcratch/)のように拡張機能を追加したScratchも公開されています。ある程度拡張のやり方がわかってきたらXcratchにも挑戦したいと思います！
