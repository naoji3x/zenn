---
title: "炭素の足跡"
emoji: "💻"
type: "tech"
topics: ["carbon footprint", "CO2", "SDGs"]
published: false
---

## はじめに

## プロジェクトの初期化

blog-starterをベースに制作していきます。

```bash
yarn create next-app --example blog-starter tanso-no-asiato
cd tanso-no-asiato
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/naoji3x/tanso-no-asiato.git
git push -u origin main
```

カーボンフットプリント計算を追加。

```bash
yarn add cfp-calc
```

### eslint

```bash
yarn add --dev eslint
npm init @eslint/config
(base) naoto@Hundolin tanso-no-asiato % npm init @eslint/config
✔ How would you like to use ESLint? · style
✔ What type of modules does your project use? · esm
✔ Which framework does your project use? · react
✔ Does your project use TypeScript? · Yes
✔ Where does your code run? · browser
✔ How would you like to define a style for your project? · guide
✔ Which style guide do you want to follow? · standard-with-typescript
✔ What format do you want your config file to be in? · JavaScript
Checking peerDependencies of eslint-config-standard-with-typescript@latest
The config that you've selected requires the following dependencies:
```

### prettier

```bash
yarn  add --dev prettier eslint-config-prettier
```

.eslintrc.jsのextendsに'prettier'を追加。

```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true
  },
  extends: ['plugin:react/recommended', 'standard-with-typescript', 'prettier'],
  overrides: [],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  plugins: ['react'],
  rules: {}
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

### remark-lint-frontmatter-schema

frontmatterのコード補完の設定

```bash
 yarn add --dev remark-cli remark-frontmatter remark-lint-frontmatter-schema 
```

vscodeでremarkプラグインをインストール。

.remarkrc.mjsに以下を設定

```javascript
import remarkFrontmatter from 'remark-frontmatter'
import remarkLintFrontmatterSchema from 'remark-lint-frontmatter-schema'

const remarkConfig = {
  plugins: [
    remarkFrontmatter,
    [
      remarkLintFrontmatterSchema,
      {
        schemas: {
          './schemas/post.yaml': ['./content/hello-world.md', './_posts/*.md']
        }
      }
    ]
  ]
}

export default remarkConfig
```

schemas/post.yaml, page.yamlの設定。

### tailwind-starter-kit-mainのインストール

```bash
yarn add --dev @fullhuman/postcss-purgecss
yarn add --dev postcss-preset-env
yarn add @fortawesome/fontawesome-free
yarn add sass
```

以下のファイルをプロジェクトルートにコピー。

- tailwind.css
- tailwind.min.css
- compiled.tailwind.css
- compiled.tailwind.min.css
- Landing Page/next-landing-page/postcss.config.js
- tailwind.config.js

 