---
layout: home

hero:
  name: pyfplib
  text: 面向 Python 的函数式编程
  tagline: 受 Rust 启发的 Option 与 Result 单子，以及可组合的序列辅助函数，零依赖。
  actions:
    - theme: brand
      text: 快速开始
      link: /zh/guide/getting-started
    - theme: alt
      text: Option API
      link: /zh/guide/option

features:
  - title: <span class="mdi mdi-checkbox-blank-circle-outline"></span> Option
    details: 使用 Some 和 Nothing 明确表示值的存在或缺失，而不是可空值。
  - title: <span class="mdi mdi-shield-check-outline"></span> Result
    details: 使用 Ok 和 Err 对成功与失败建模，无需到处散落 try/except 即可串联计算。
  - title: <span class="mdi mdi-function-variant"></span> 函数式辅助
    details: fold、find、any_of、all_of、none_of、head、tail 等，简洁处理序列。
  - title: <span class="mdi mdi-package-variant-closed"></span> 零依赖
    details: 纯 Python，无运行时依赖，兼容 Python 3.12 及更高版本。
---
