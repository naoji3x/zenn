---
title: "じぶんごとプラネットのカーボンフットプリント計算をライブラリ化"
emoji: "😾"
type: "tech"
topics: ["javascript", "typescript"]
published: false
---

## はじめに

## プロジェクトの初期化

```bash
% cfp-calc % npm init
package name: (cfp-calc) 
version: (1.0.0) 0.1.0
description: A carbon footprint calculation library for those living in Japan
entry point: (index.js) 
test command: jest
git repository: 
keywords: 
author: Naoto Komiya
license: (ISC) MIT
About to write to /Users/naoto/Documents/projects/code-for-japan/cfp-calc/package.json:

{
  "name": "cfp-calc",
  "version": "0.1.0",
  "description": "A carbon footprint calculation library for those living in Japan",
  "main": "index.js",
  "scripts": {
    "test": "jest"
  },
  "author": "Naoto Komiya",
  "license": "MIT"
}
```

## typescriptの設定

### typescript, eslint

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

### prettier

```bash
npm i -D prettier eslint-config-prettier
```

.eslintrc.jsのextendsに'prettier'を追加。

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

.prettierrcを追加。

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

### tsconfig

tsconfig.jsonの設定。es5へトランスパイルするとともにasync/awaitを有効化。

```json
{
  "compilerOptions": {
    "target": "es5",
    "module": "es6",
    "baseUrl": "./src",
    "declaration": true,  // ← 追記（コンパイルしたtsファイルの中でexportしているもの全ての型定義ファイルを出力する）
    "sourceMap": true,  // ← 追記（ソースマップを出力する）
    "outDir": "./dist",  // ← 追記（コンパイル結果の出力先を指定）
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "skipLibCheck": true,
    "allowSyntheticDefaultImports": true,
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "typeRoots": ["node_modules/@types"],
    "lib": ["dom", "es2015.promise", "es5"]
  },
  "include": ["src/**/*.ts"]  // ← 追記（コンパイルする対象ファイルの場所を指定
}
```

### jest

```bash
% npm i -D jest ts-jest @types/jest
% npm i -D eslint-plugin-jest # vs codeでjestのdescribe等でエラーが出るので導入。
```

jest.config.jsに以下を追加

```javascript
/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node'
}
```

.eslintrc.jsに以下を追加

```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
    'jest/globals': true, // 追加 vs codeのエラー対策 https://qiita.com/tutu/items/66f586c455ded70bd1e2
  },
  extends: ['standard-with-typescript', 'prettier'],
  overrides: [],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: ['./tsconfig.eslint.json'] // 追加 eslintを実行する際の設定 https://zenn.dev/rinda_1994/articles/07a30be1a26a38
  },
  rules: {},
  plugins: ['jest'] // 追加 vs codeのエラー対策 https://oisham.hatenablog.com/entry/2019/08/20/111826
}
```

tsconfig.eslint.jsonを作成。

```json
// https://zenn.dev/rinda_1994/articles/07a30be1a26a38
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "noEmit": true
  },
  "include": [
    "./src/**/*.ts",
    "./data/**/*.ts",
    "./tests/**/*.ts",
    "./dist/**/*.ts"
  ]
}
```

### data作成用スクリプト実行

```bash
% npm i -D ts-node
% npm i -D csv-parse
```

tsconfig.jsonに以下を追加。

```json
{
  ...
  "ts-node": {
    "compilerOptions": {
      "module": "CommonJS"
    }
  },
  ...
}
```

上記でdata以下のフォルダでデータ作成用のスクリプトを実行。

## GitHubへの登録

```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:naoji3x/cfp-calc.git
```

以降はforkでpush.

## huskyの設定

`package.json`に以下を追加

```bash
npx husky-init && npm install
npx husky add .husky/pre-commit "npm run lint:fix"
npx husky add .husky/pre-commit "npm run format"
npm i -D @commitlint/{config-conventional,cli}
npx husky add .husky/commit-msg 'npm run commit-msg'
```

package.jsonに以下を追加。

```json
  "scripts": {
    ...
    "commit-msg": "commitlint -e $GIT_PARAMS",
    ...
  },
```

commitlint.config.jsに以下を記載

```javascript
module.exports = {
  extends: ['@commitlint/config-conventional']
```

huskyのcommitlintの設定は下記を参照。
https://note.com/shift_tech/n/nb4700a3b3de6

## ドキュメンテーション

tsdocをインストール

```bash
npm i -D @microsoft/tsdoc typedoc
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

## npmのパッケージ公開

以下を参考に、

https://zenn.dev/k0kishima/articles/d75f4dc5bd1a26
https://qiita.com/i-tanaka730/items/c85daa3ee2dcde9bd728

.npmignoreを編集して、以下のコマンドでパブリッシュ。

```bash
npm run build
npm publish
```

publishがdistディレクトリごとパブリッシュされてしまうので、distディレクトリに移動してpublishするように変更。

```bash
npm i -D npm-run-all
npm i -D shx
```

package.json

```json

```

## gitのコマンドラインの設定

https://qiita.com/Takao_/items/129c5e83f8b608dcf0d2
