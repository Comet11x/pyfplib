---
layout: home

hero:
  name: pyfplib
  text: Python のための関数型プログラミング
  tagline: Rust にインスパイアされた Option と Result モナド、そして合成可能なシーケンスヘルパー。依存関係なし。
  actions:
    - theme: brand
      text: セットアップ
      link: /ja/guide/getting-started
    - theme: alt
      text: Option API
      link: /ja/guide/option

features:
  - title: <span class="mdi mdi-checkbox-blank-circle-outline"></span> Option
    details: nullable な値の代わりに Some と Nothing で存在・不在を明示的に表現します。
  - title: <span class="mdi mdi-shield-check-outline"></span> Result
    details: Ok と Err で成功と失敗をモデル化し、try/except を散らばせずに計算を連鎖させます。
  - title: <span class="mdi mdi-function-variant"></span> 関数型ヘルパー
    details: fold、find、any_of、all_of、none_of、head、tail などでシーケンスを簡潔に処理します。
  - title: <span class="mdi mdi-package-variant-closed"></span> 依存関係なし
    details: ランタイム依存のない純粋な Python。Python 3.12 以降に対応。
---
