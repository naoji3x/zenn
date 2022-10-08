---
title: "Scratchを拡張"
emoji: "😾"
type: "tech"
topics: ["scratch", "CoderDojo", "javascript"]
published: false
---

## はじめに

[CoderDojo](https://coderdojo.jp/)というボランティア団体で、子供達のプログラミングスキル習得の支援をしております。プログラミングの開発環境は、主に[Scratch]((https://scratch.mit.edu))を使っていますが、標準機能だけでは飽き足らず、このシリーズではScratchの拡張に挑戦します！

### コマンド

```bash
git clone --depth 1 -b xcratch https://github.com/xcratch/scratch-gui.git
cd ./scratch-gui
npm i
cd ../
npx xcratch-create --repo=xcx-open-meteo --account=[github account] --extensionID=openMeteo --extensionName='Open Meteo'
cd xcx-open-meteo
npm i
```

typescriptの設定は、https://zenn.dev/big_tanukiudon/articles/c1ab3dba7ba111 を参考に各種ツールをインストールしました。

```bash
npm i -D cpx npm-run-all rimraf typescript
```

eslintのインストール

```bash
npm i -D eslint
```

eslintの構成を設定。

```bash
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

tsconfig.jsonの設定。es5へトランスパイルするとともにasync/awaitを有効化。

```json
{
  "compilerOptions": {
    "outDir": "./build",
    "allowJs": true,
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
  "include": ["./src/**/*", "./types/**/*"]
}
```

```bash
npm run build:static
npm run register
npm run relink
```
