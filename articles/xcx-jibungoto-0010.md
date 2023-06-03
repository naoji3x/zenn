---
title: "じぶんごとプラネットをScratchに移植"
emoji: "😾"
type: "tech"
topics: ["scratch", "CoderDojo", "javascript", "typescript"]
published: false
---

## はじめに

```bash
% git clone -b xcratch https://github.com/xcratch/scratch-gui.git
% cd scratch-gui
% npm install
% cd ..
% npx xcratch-create --repo=xcx-jibungoto --account=<account> --extensionID=jibungotoPlanet --extensionName='Jibungoto Planet'
% cd xcx-jibungoto
% git init -b main
% git remote add origin git@github.com:naoji3x/xcx-jibungoto.git
% git add .
% git commit -m "First commit"
% npm install
% npm run register
% cd ../scratch-gui
% npm run start
```

ここまで、xcratchの設定、以下はtypescript

```bash
% npm i -D typescript
% npm i -D eslint            
% npm init @eslint/config
npm init @eslint/config                                
✔ How would you like to use ESLint?
> To check syntax, find problems, and enforce code style
✔ What type of modules does your project use?
> JavaScript modules (import/export)
✔ Which framework does your project use?
❯ None of these
✔ Does your project use TypeScript?
> Yes
✔ Where does your code run?
> browser, node
✔ How would you like to define a style for your project?
> Use a popular style guide
✔ Which style guide do you want to follow?
❯ Standard: https://github.com/standard/eslint-config-standard-with-typescript
✔ What format do you want your config file to be in?
> JavaScript
✔ Would you like to install them now?
> Yes
✔ Which package manager do you want to use?
> npm
```

prettierをインストール

```bash
npm i -D prettier eslint-config-prettier
```

eslintrc.jsのextendsに'prettier'を追加。

```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true
  },
  extends: ['standard-with-typescript', 'prettier'],
  overrides: [
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  rules: {
  }
}
```

.prettierrc

```json
{
  "printWidth": 80,
  "trailingComma": "none",
  "tabWidth": 2,
  "semi": false,
  "singleQuote": true,
  "endOfLine": "lf"
}
```

tsconfig.jsonの設定。es5へトランスパイルするとともにasync/awaitを有効化。

```json
{
  "compilerOptions": {
    "baseUrl": "./src",
    "rootDir": "./src/ts",
    "outDir": "./src/vm/extensions/block",
    "target": "es5",
    "module": "es6",
    "strict": true,
    "jsx": "preserve",
    "allowSyntheticDefaultImports": true,
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "typeRoots": ["types", "node_modules/@types"],
    "lib": ["dom", "es2015.promise", "es5"],
  },
  "include": [
    "./src/ts/**/*"
  ]
}
```

jest

```bash
% npm i -D jest ts-jest @types/jest
```

data作成用スクリプト実行

```bash
% npm i -D ts-node
% npm i -D csv-parse
```

```json
{
  "compilerOptions": {
    "baseUrl": "./src",
    "rootDir": "./src/ts",
    "outDir": "./src/vm/extensions/block",
    "target": "es5",
    "module": "es6",
    "strict": true,
    "jsx": "preserve",
    "allowSyntheticDefaultImports": true,
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "typeRoots": ["types", "node_modules/@types"],
    "lib": ["dom", "es2015.promise", "es5"]
  },
  "ts-node": {
    "compilerOptions": {
      "module": "CommonJS"
    }
  },
  "include": ["./src/ts/**/*"]
}
```

上記でdata以下のフォルダでデータ作成用のスクリプトを実行。

vs codeでjestのdescribe等でエラーが出るので以下を導入。

```bash
npm i -D eslint-plugin-jest
```

```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
    'jest/globals': true // 追加 vs codeのエラー対策 https://qiita.com/tutu/items/66f586c455ded70bd1e2
  },
  extends: ['standard-with-typescript', 'prettier'],
  overrides: [],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
    project: ['./tsconfig.eslint.json'] // 追加 eslintを実行する際の設定 https://zenn.dev/rinda_1994/articles/07a30be1a26a38
  },
  plugins: ['jest'] // 追加 vs codeのエラー対策 https://oisham.hatenablog.com/entry/2019/08/20/111826
}
```

## huskyの設定

`package.json`に以下を追加

```json
{
    "script": {
        "prepare": "husky install"
    }
}
```

```bash
npx husky-init && npm install
npx husky add .husky/pre-commit "npm run lint:fix"
npx husky add .husky/pre-commit "npm run format"
npm i -D @commitlint/{config-conventional,cli}
npx husky add .husky/commit-msg 'npm run commit-msg'
```

huskyのcommitlintの設定は下記を参照。
https://note.com/shift_tech/n/nb4700a3b3de6

## nodeのバージョンアップ 16 -> 18

```bash
nvm current # アクティブなnodeのバージョンを表示
nvm ls # インストールされているnodeの一覧
nvm install --lts # 最新ltsをインストール
       v16.13.0
       v16.17.1
       v18.10.0
->     v18.16.0
npm install # npmのモジュールを
cd ../scratch-gui
rm -rf node_modules
rm -rf build
rm -rf dist
nvm use 18
npm install 
npm i -D webpack-dev-server
```

色々やってみたがまだ18は早かったようなので16に戻す。

```bash
nvm alias default v16.17.1
```

## ドキュメンテーション

tsdocをインストール

```bash
npm i -D @microsoft/tsdoc
npm i -D typedoc@0.23
npm i -D typedoc-theme-hierarchy@^3.0.0
```

package.jsonに以下を追加

```json
{
  ...
  "scripts": {
    ...
    "doc": "typedoc"
  },
  ...
}
```

以下を実行

```bash
npm run doc
```

## build publishのやり方

```bash
npm run build
```

この後、vs code のLive Serverで稼働確認。

https://xcratch.github.io/editor

拡張機能を追加→拡張機能を読み込むで以下を入力。
http://localhost:5500/dist/jibungotoPlanet.mjs

## npmのパッケージ公開
