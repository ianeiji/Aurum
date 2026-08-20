# CLAUDE.md

このプロジェクトの開発支援AIはClaudeを想定する。ただし、実運用の売買判断LLMはClaude固定ではない。Claude向けに実装を最適化してprovider非依存性を失わせてはならない。

## 最初に読む

1. `docs/research/llm-trading-findings.md`
2. `docs/01-architecture.md`
3. `docs/02-safety.md`
4. `docs/03-evaluation-protocol.md`
5. `docs/04-data-and-observability.md`
6. `docs/05-roadmap.md`
7. `docs/06-operations-and-llm-cost.md`

## 絶対ルール

- LLM/StrategyからMT5を直接操作させない。
- 全注文を決定論的Risk Engineへ通す。
- Risk拒否を迂回・再解釈・握りつぶさない。
- LLMにlot、loss limit、risk policyを決定/変更させない。
- 不明、timeout、不正schema、stale dataではfail closedにする。
- MT5の実状態を正とし、再照合する。
- 新規注文には有効なSLを要求する。
- 実口座やrisk上限を勝手に有効化/緩和しない。

## LLM実装

- provider固有処理はadapterへ閉じ込める。
- BUY/SELL/WAITを含むversioned schemaで出力させる。
- 自己申告confidenceを直接position sizingへ使わない。
- prompt、model、strategy変更は新versionとして扱う。
- model aliasだけでなく取得可能なrevisionも保存する。
- Rule-only baselineを削除、劣化、別条件化しない。
- 決定論的な監視・計算・Risk処理にLLM APIを追加しない。
- Claude Codeの定額枠をProduction inference APIとして流用しない。
- Chat経由のManualTradeCommandにもRisk Engineを必須とする。

## 研究・評価

- accuracyや短期PnLだけを成功条件にしない。
- fee、spread、slippage、swapを含むnet指標を使う。
- 時系列splitとIS/validation/OOS/forward/少額realの境界を守る。
- OOSを見て変更したら、新experimentとして評価をやり直す。
- strategy/prompt/model/data/risk versionと全試行を記録する。
- LLM追加版が同条件baselineを上回らなければ外せる状態を保つ。
- LLMのtoken/model/decision/trade単位コストを記録する。

## 変更時チェック

- Risk bypass経路を増やしていないか
- look-ahead/data leakageを入れていないか
- versionとdecision/order traceが欠落していないか
- retryで重複発注しないか
- error/partial fill/restart後にMT5と再照合できるか
- cost込みのテストとbaseline比較があるか

利益を保証する表現をドキュメントやUIに入れない。LLMの説明を予測能力の証拠として扱わない。

## Commit Convention

コミットメッセージは `COMMIT_CONVENTION.md` に従うこと。

- type / scope: 英語
- description: 日本語

## Branch and PR Convention

ブランチ運用とPRは `BRANCH_AND_PR_CONVENTION.md` に従うこと。

- Issue単位でブランチを切りPRを作成する
- Risk Engine等の安全性が絡む変更は「変更時チェック」をPRで確認する
