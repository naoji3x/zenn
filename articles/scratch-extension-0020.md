---
title: "Scratchを拡張しよう！(2)地図を表示"
emoji: "😾"
type: "tech"
topics: ["scratch", "CoderDojo", "javascript"]
published: true
---

## はじめに

[CoderDojo](https://coderdojo.jp/)というボランティア団体で、子供達のプログラミングスキル習得の支援をしております。プログラミングの開発環境は、主に[Scratch]((https://scratch.mit.edu))を使っていますが、標準機能だけでは飽き足らず、このシリーズではScratchの拡張機能開発に挑戦します！今回は地図表示に挑戦します。

地図表示の拡張機能は、Junya Ishiharaさんが開発した[Geo Scratch](https://github.com/geolonia/x-geo-scratch)がよくできていますのでそちらをご利用頂くのがオススメですが、今回は画像表示の練習として取り組んでみました。

https://github.com/geolonia/x-geo-scratch

完成したサイトはこちらになります。

**[地図表示拡張機能付きScratch](https://naoji3x.github.io/scratch-gui/)**

![地図表示拡張機能付きScratch](/images/scratch-extension-0020/extension.png)
*地図表示拡張機能付きScratch*

拡張機能から地図を追加すると、

- 緯度、経度、ズームレベル(0〜18)を指定しての地図を表示できます。デフォルトは東京都庁を表示します。※ちなみに地図を消去する機能がないのでご注意下さい。

今回表示する地図はオープンデータの[Open Street Map](https://www.openstreetmap.org)を利用しています。著作権は[こちら](https://www.openstreetmap.org/copyright)をご参照下さい。

### 下準備

下準備は[(1)天気予報を取得](https://zenn.dev/naoji/articles/scratch-extension-0010)を参照下さい。

### scratch-gui側の開発

`scratch-gui/src/lib/libraries/extensions`に`openstreetmap`ディレクトリを作りましょう。この中にScratchの拡張機能のアイコンを格納します。ラージサイズのアイコンは600px x 372px, スモールサイズのアイコンは80px x 80pxになります。

![ラージサイズ](/images/scratch-extension-0020/open-street-map.png)
*ラージサイズ 600px x 372px*

![スモールサイズ](/images/scratch-extension-0020/open-street-map-small.png)
*スモールサイズ 80px x 80px*

この後は、ソースコードの修正になります。`scratch-gui/src/lib/libraries/extensions/index.jsx`に以下のコードを追加します。

```javascript
...中略

import gdxforInsetIconURL from './gdxfor/gdxfor-small.svg';
import gdxforConnectionIconURL from './gdxfor/gdxfor-illustration.svg';
import gdxforConnectionSmallIconURL from './gdxfor/gdxfor-small.svg';

import openMeteoIconURL from './openmeteo/open-meteo.png';
import openMeteoInsetIconURL from './openmeteo/open-meteo-small.png';

import openStreetMapIconURL from './openstreetmap/open-street-map.png'; // この行を追加
import openStreetMapInsetIconURL from './openstreetmap/open-street-map-small.png'; // この行を追加

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
    {
        name: '天気予報(てんきよほう)',
        extensionId: 'openMeteo',
        iconURL: openMeteoIconURL,
        insetIconURL: openMeteoInsetIconURL,
        description: '天気予報を取得します（てんきよほうをしゅとくします）',
        internetConnectionRequired: true,
        featured: true
    },
    // 最後に以下の行を追加
    {
        name: '地図(ちず)',
        extensionId: 'openStreetMap',
        iconURL: openStreetMapIconURL,
        insetIconURL: openStreetMapInsetIconURL,
        description: '地図を表示します（ちずをひょうじします）。地図の著作権はhttps://www.openstreetmap.orgのcopyrightを参照ください。©︎OpenStreetMap contributors',
        internetConnectionRequired: true,
        featured: true,
        helpLink: 'https://www.openstreetmap.org/copyright'
    }
    // ここまで
];
```

今回も、多言語対応、ひらがな表示対応まで設定したかったのですが、色々大変そうなため日本語表示のみにしています。

### scratch-vm側の開発

scratch-vmの開発も[(1)天気予報を取得](https://zenn.dev/naoji/articles/scratch-extension-0010)と同様ですので参考にして下さい。今回はOpen Street Mapの地図表示がキモですので、実装の概要をまとめます。

1. Open Street Mapでは256px x 256pxのタイル状の地図を以下のAPIで提供します。
```https://a.tile.openstreetmap.org/[z]/[x]/[y].png```
2. ここで、```[z]```はズームレベル、```[x]```は地図のx方向のタイル番号、```[y]```はy方向のタイル番号になります。
3. ズームレベルが0の時は、256px x 256pxの１つのタイルに全世界のマップが描かれ、ズームレベルが1の時は2x2の4つのタイルに全世界が描かれ、と、以降ズームレベルが増えるごとに倍々でタイル数が増える構造です。
4. 緯度と経度からx,yに相互変換する方法につきましては[Slippy map tilenames](https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames)を参照下さい。コードサンプルもありますので、ほぼそのまま活用させていただきました。
5. 今回はタイルの処理が複雑なため、緯度、経度から表示するタイル情報を計算するクラス```TileMap```と、タイル情報から地図を取得しキャッシュするクラス```TileCache```を作りました。

https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames

`src/extensions`ディレクトリに```scratch3_open_street_map```ディレクトリを作成し、以下の```index.js```, ```tile-map.js```, ```tile-cache.js```を追加ください。

#### index.js

```javascript
const ArgumentType = require('../../extension-support/argument-type');
const BlockType = require('../../extension-support/block-type');
const Cast = require('../../util/cast');
const StageLayering = require('../../engine/stage-layering');
const TileMap = require('./tile-map');
const TileCache = require('./tile-cache');

/**
 * Icon svg to be displayed at the left edge of each extension block, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const blockIconURI = 'data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+Cjxzdmcgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgdmlld0JveD0iMCAwIDQwIDQwIiB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHhtbDpzcGFjZT0icHJlc2VydmUiIHhtbG5zOnNlcmlmPSJodHRwOi8vd3d3LnNlcmlmLmNvbS8iIHN0eWxlPSJmaWxsLXJ1bGU6ZXZlbm9kZDtjbGlwLXJ1bGU6ZXZlbm9kZDtzdHJva2UtbGluZWpvaW46cm91bmQ7c3Ryb2tlLW1pdGVybGltaXQ6MjsiPgogICAgPGcgdHJhbnNmb3JtPSJtYXRyaXgoMSwwLDAsMSwtNjEwLC05MCkiPgogICAgICAgIDxnIGlkPSJibG9jay1pY29uIiB0cmFuc2Zvcm09Im1hdHJpeCgxLDAsMCwwLjk1MjM4MSwwLDMuMzMzMzMpIj4KICAgICAgICAgICAgPHJlY3QgeD0iNjEwIiB5PSI5MSIgd2lkdGg9IjQwIiBoZWlnaHQ9IjQyIiBzdHlsZT0iZmlsbDpub25lOyIvPgogICAgICAgICAgICA8ZyB0cmFuc2Zvcm09Im1hdHJpeCgxLjY4NzUsMCwwLDEuNzcxODcsNjE3LDk3LjI5OTkpIj4KICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik0xNS44MTcsMC4xMTNDMTUuOTMzLDAuMjA4IDE2LDAuMzUgMTYsMC41TDE2LDE0LjVDMTYsMTQuNzM3IDE1LjgzMSwxNC45NDMgMTUuNTk4LDE0Ljk5TDEwLjU5OCwxNS45OUMxMC41MzMsMTYuMDAzIDEwLjQ2NywxNi4wMDMgMTAuNDAyLDE1Ljk5TDUuNSwxNS4wMUwwLjU5OCwxNS45OUMwLjU2NiwxNS45OTYgMC41MzMsMTYgMC41LDE2QzAuMjI2LDE2IDAsMTUuNzc0IDAsMTUuNUwwLDEuNUMwLDEuMjYzIDAuMTY5LDEuMDU3IDAuNDAyLDEuMDFMNS40MDIsMC4wMUM1LjQ2NywtMC4wMDMgNS41MzMsLTAuMDAzIDUuNTk4LDAuMDFMMTAuNSwwLjk5TDE1LjQwMiwwLjAxQzE1LjU0OSwtMC4wMiAxNS43MDEsMC4wMTggMTUuODE3LDAuMTEzWk0xMCwxLjkxTDYsMS4xMUw2LDE0LjA5TDEwLDE0Ljg5TDEwLDEuOTFaTTExLDE0Ljg5TDE1LDE0LjA5TDE1LDEuMTFMMTEsMS45MUwxMSwxNC44OVpNNSwxNC4wOUw1LDEuMTFMMSwxLjkxTDEsMTQuODlMNSwxNC4wOVoiIHN0eWxlPSJmaWxsOndoaXRlOyIvPgogICAgICAgICAgICA8L2c+CiAgICAgICAgPC9nPgogICAgPC9nPgo8L3N2Zz4K';

/**
 * Icon svg to be displayed in the category menu, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const menuIconURI = 'data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+Cjxzdmcgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgdmlld0JveD0iMCAwIDQwIDQwIiB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHhtbDpzcGFjZT0icHJlc2VydmUiIHhtbG5zOnNlcmlmPSJodHRwOi8vd3d3LnNlcmlmLmNvbS8iIHN0eWxlPSJmaWxsLXJ1bGU6ZXZlbm9kZDtjbGlwLXJ1bGU6ZXZlbm9kZDtzdHJva2UtbGluZWpvaW46cm91bmQ7c3Ryb2tlLW1pdGVybGltaXQ6MjsiPgogICAgPGcgdHJhbnNmb3JtPSJtYXRyaXgoMSwwLDAsMSwtNjEwLC0xNDApIj4KICAgICAgICA8ZyBpZD0ibWVudS1pY29uIiB0cmFuc2Zvcm09Im1hdHJpeCgxLDAsMCwwLjk1MjM4MSwwLDUzLjMzMzMpIj4KICAgICAgICAgICAgPHJlY3QgeD0iNjEwIiB5PSI5MSIgd2lkdGg9IjQwIiBoZWlnaHQ9IjQyIiBzdHlsZT0iZmlsbDpub25lOyIvPgogICAgICAgICAgICA8Y2xpcFBhdGggaWQ9Il9jbGlwMSI+CiAgICAgICAgICAgICAgICA8cmVjdCB4PSI2MTAiIHk9IjkxIiB3aWR0aD0iNDAiIGhlaWdodD0iNDIiLz4KICAgICAgICAgICAgPC9jbGlwUGF0aD4KICAgICAgICAgICAgPGcgY2xpcC1wYXRoPSJ1cmwoI19jbGlwMSkiPgogICAgICAgICAgICAgICAgPGcgdHJhbnNmb3JtPSJtYXRyaXgoMSwwLDAsMS4wNSwwLC01NikiPgogICAgICAgICAgICAgICAgICAgIDxjaXJjbGUgY3g9IjYzMCIgY3k9IjE2MCIgcj0iMjAiIHN0eWxlPSJmaWxsOnJnYigyNTUsMTgxLDApOyIvPgogICAgICAgICAgICAgICAgPC9nPgogICAgICAgICAgICAgICAgPGcgdHJhbnNmb3JtPSJtYXRyaXgoMS40Mzc1LDAsMCwxLjUwOTM3LDYxOC41LDk5LjkyNTEpIj4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBkPSJNMTUuODE3LDAuMTEzQzE1LjkzMywwLjIwOCAxNiwwLjM1IDE2LDAuNUwxNiwxNC41QzE2LDE0LjczNyAxNS44MzEsMTQuOTQzIDE1LjU5OCwxNC45OUwxMC41OTgsMTUuOTlDMTAuNTMzLDE2LjAwMyAxMC40NjcsMTYuMDAzIDEwLjQwMiwxNS45OUw1LjUsMTUuMDFMMC41OTgsMTUuOTlDMC41NjYsMTUuOTk2IDAuNTMzLDE2IDAuNSwxNkMwLjIyNiwxNiAwLDE1Ljc3NCAwLDE1LjVMMCwxLjVDMCwxLjI2MyAwLjE2OSwxLjA1NyAwLjQwMiwxLjAxTDUuNDAyLDAuMDFDNS40NjcsLTAuMDAzIDUuNTMzLC0wLjAwMyA1LjU5OCwwLjAxTDEwLjUsMC45OUwxNS40MDIsMC4wMUMxNS41NDksLTAuMDIgMTUuNzAxLDAuMDE4IDE1LjgxNywwLjExM1pNMTAsMS45MUw2LDEuMTFMNiwxNC4wOUwxMCwxNC44OUwxMCwxLjkxWk0xMSwxNC44OUwxNSwxNC4wOUwxNSwxLjExTDExLDEuOTFMMTEsMTQuODlaTTUsMTQuMDlMNSwxLjExTDEsMS45MUwxLDE0Ljg5TDUsMTQuMDlaIiBzdHlsZT0iZmlsbDp3aGl0ZTsiLz4KICAgICAgICAgICAgICAgIDwvZz4KICAgICAgICAgICAgPC9nPgogICAgICAgIDwvZz4KICAgIDwvZz4KPC9zdmc+Cg==';

/**
 * Class for the new blocks in Scratch 3.0
 * @param {Runtime} runtime - the runtime instantiating this block package.
 * @constructor
 */
class Scratch3OpenStreetMapBlocks {
    constructor (runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {Runtime}
         */
        this.runtime = runtime;
        this.tileMap = new TileMap();
        this.tileCache = new TileCache();

        this.canvas = document.createElement('canvas');
        this.canvas.width = 480;
        this.canvas.height = 360;
    }

    async drawImages () {
        if (this.runtime.renderer) {
            this.ctx = this.canvas.getContext('2d');

            const promises = [];
            for (const tile of this.tileMap.tiles) {
                promises.push(this.tileCache.getImage(tile.zoom, tile.x, tile.y));
            }

            const images = [];
            for (const promise of promises) {
                images.push(await promise);
            }

            let index = 0;
            for (const tile of this.tileMap.tiles) {
                this.ctx.drawImage(images[index], tile.screenX, tile.screenY);
                ++index;
            }

            // Scratch固有の処理
            this.skinId = this.runtime.renderer.createBitmapSkin(this.canvas, 1);
            const drawableId = this.runtime.renderer.createDrawable(
                StageLayering.BACKGROUND_LAYER
            );
            this.runtime.renderer.updateDrawableProperties(drawableId, {
                skinId: this.skinId
            });
            // ここまで
        }
    }

    drawTileMap (args) {
        const latitude = Cast.toNumber(args.LATITUDE);
        const longitude = Cast.toNumber(args.LONGITUDE);
        const zoom = Cast.toNumber(args.ZOOM);

        this.tileMap.buildTiles(zoom, longitude, latitude, 480, 360);
        this.drawImages();
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo () {
        return {
            id: 'openStreetMap',
            name: '地図',
            menuIconURI: menuIconURI,
            blockIconURI: blockIconURI,
            blocks: [
                {
                    opcode: 'drawTileMap',
                    text: '緯度 [LATITUDE], 経度 [LONGITUDE]の地図をズームレベル[ZOOM]で表示する',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        ZOOM: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 18
                        },
                        LATITUDE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 35.689185
                        },
                        LONGITUDE: {
                            type: ArgumentType.NUMBER,
                            defaultValue: 139.691648
                        }
                    }
                }
            ],
            menus: {
            }
        };
    }
}

module.exports = Scratch3OpenStreetMapBlocks;
```

```index.js```のポイントは、以下のScratchの描画エンジンを使うところで、この部分は[タコキンのPスクール・ブログ](https://p-school.tacoskingdom.com/developer#blog)の解説を参考にさせていただきました（ありがとうございますございます🙇）。

```javascript
            // Scratch固有の処理
            this.skinId = this.runtime.renderer.createBitmapSkin(this.canvas, 1);
            const drawableId = this.runtime.renderer.createDrawable(
                StageLayering.BACKGROUND_LAYER
            );
            this.runtime.renderer.updateDrawableProperties(drawableId, {
                skinId: this.skinId
            });
            // ここまで
```

#### tile-map.js

```javascript
class TileMap {
    constructor () {
        this.tileSize = 256;
        this.xCount = 0;
        this.yCount = 0;
        this.tiles = [];
    }

    // 経度→x変換
    longitude2x (lon, zoom) {
        return (Math.floor((lon + 180) / 360 * Math.pow(2, zoom)));
    }

    // 緯度→y変換
    latitude2y (lat, zoom) {
        const n = lat * Math.PI / 180;
        return (Math.floor((1 - (Math.log(Math.tan(n) + (1 / Math.cos(n))) / Math.PI)) / 2 * Math.pow(2, zoom)));
    }

    // x→経度変換
    x2longitude (x, zoom) {
        return (x / Math.pow(2, zoom) * 360) - 180;
    }

    // y→緯度変換
    y2latitude (y, zoom) {
        const n = Math.PI - (2 * Math.PI * y / Math.pow(2, zoom));
        return (180 / Math.PI * Math.atan(0.5 * (Math.exp(n) - Math.exp(-n))));
    }

    // x, yをcountからはみ出ている場合に補正
    adjust (index, count) {
        // 計算例
        // count = 1の時は常に0
        // count = 2, index = -1 の時は1を返す
        // count = 2, index = -2 の時は0を返す
        // count = 2, index = 2 の時は0を返す
        // count = 2, index = 3 の時は1を返す
        if (count === 1) {
            return 0;
        } else if (index >= 0 && index < count) {
            return index;
        }
        const remainder = index % count;

        return (index < 0) ? count + remainder : remainder;
    }

    // screenWidth, screenHeightを埋めるタイルを計算しtilesに格納する。
    buildTiles (zoom, centerLongitude, centerLatitude, screenWidth, screenHeight) {
        zoom = Math.round(zoom);
        if (zoom < 0) zoom = 0;
        if (zoom > 18) zoom = 18;

        // 画面の1/2に敷き詰めるタイル数を計算
        const wHalfCount = Math.ceil(screenWidth / (2 * this.tileSize));
        const hHalfCount = Math.ceil(screenHeight / (2 * this.tileSize));

        // 真ん中のタイルのx, yを求める
        const xc = this.longitude2x(centerLongitude, zoom);
        const yc = this.latitude2y(centerLatitude, zoom);

        // 画面に表示するタイルの範囲を取得
        const yMin = yc - hHalfCount;
        const yMax = yc + hHalfCount;
        const xMin = xc - wHalfCount;
        const xMax = xc + wHalfCount;

        // タイル行列の列数、行数を計算
        this.xCount = xMax - xMin + 1;
        this.yCount = yMax - yMin + 1;
        this.tiles = [];

        // 真ん中のタイルの左上のWold座標を求める
        const lng0 = this.x2longitude(xc, zoom);
        const lat0 = this.y2latitude(yc, zoom);

        // 真ん中のタイルの右下のWorld座標を求める
        const lng1 = this.x2longitude(xc + 1, zoom);
        const lat1 = this.y2latitude(yc + 1, zoom);

        // センタータイルの表示位置の左上からのオフセット（画面座標系）を計算
        const xOffset = this.tileSize * (centerLongitude - lng0) / (lng1 - lng0);
        const yOffset = this.tileSize * (centerLatitude - lat0) / (lat1 - lat0);

        const count = 2 ** zoom;
        // 画面に表示するタイルを列挙
        let n = 0;
        for (let y = yMin; y <= yMax; ++y) {
            let m = 0;
            for (let x = xMin; x <= xMax; ++x) {
                // 画面上のx座標を計算
                const screenX = -(this.xCount * this.tileSize / 2) +
                (m * this.tileSize) + (this.tileSize / 2) - xOffset + (screenWidth / 2);
                // 画面上のy座標を計算
                const screenY = -(this.yCount * this.tileSize / 2) +
                (n * this.tileSize) + (this.tileSize / 2) - yOffset + (screenHeight / 2);
                this.tiles.push({zoom, x: this.adjust(x, count), y: this.adjust(y, count), screenX, screenY});
                ++m;
            }
            ++n;
        }
    }
}

module.exports = TileMap;
```

#### tile-cache.js

```javascript
class TileCache {
    constructor () {
        this.cache = new Map();
    }

    async getImage (zoom, x, y) {
        const key = `${zoom}-${x}-${y}`;
        const cachedImage = this.cache.get(key);
        if (cachedImage) {
            return cachedImage;
        }

        const img = await this.loadImage(zoom, x, y);
        // キャッシュする画像は100まで
        if (this.cache.size >= 100) {
            const deleteKey = this.cache.keys().next().value;
            this.cache.delete(deleteKey);
        }
        this.cache.set(key, img);
        return img;
    }

    loadImage (zoom, x, y) {
        const prefix = 'https://a.tile.openstreetmap.org';
        const suffix = '.png';

        const url = `${prefix}/${zoom}/${x}/${y}${suffix}`;
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => resolve(img);
            img.onerror = e => reject(e);
            img.src = url;
            img.crossOrigin = 'Anonymous';
        });
    }
}

module.exports = TileCache;
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
    openMeteo: () => require('../extensions/scratch3_open_meteo'),
    openStreetMap: () => require('../extensions/scratch3_open_street_map') // <- この行を追加
};
...中略
```

### テスト〜GitHub Pagesでの公開

[(1)天気予報を取得](https://zenn.dev/naoji/articles/scratch-extension-0010)と同じですので参照下さい。

## おわりに

完成してみると比較的シンプルな実装にまとまりましたが、ここまで来るのにだいぶ試行錯誤しました😅。Javascriptなので、最初は[leaflet](https://leafletjs.com/)で実装しようと思いましたが、、、Scratchの描画エンジンを使いたかったので、最終的にはOpen Street Map APIから画像を取得して表示する、今回の実装方法に落ち着きました。

地図はピン表示など色々応用が考えられそうですので、今回の実装を元に更にブラッシュアップしていきたいと思います！
