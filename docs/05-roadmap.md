# Roadmap

## Phase 0 — 仕様と再現性の土台

- StrategyDecision、MarketSnapshot、RiskResultの契約を定義
- version/experiment registryとdataset manifestを定義
- Rule-only baselineと評価指標を事前登録
- Risk不変条件と脅威/障害シナリオをテスト仕様化
- Edge / Execution / Riskの責務とLive / Evaluation境界を定義
- OFF / ASSIST / MANUAL+ / AUTOの状態遷移を定義

**完了条件:** version不明の結果を集計できず、Risk bypassを設計上許さない。

## Phase 1 — ローカルMT5 PoC

- MT5 market/account/position取得
- bar確定、timezone、欠損、再接続
- Order Managerのdry-run、idempotency、reconciliation
- PostgreSQL監査イベントと基本dashboard/alerts

**完了条件:** LLMなしで取得から監査まで再現できる。まだreal発注しない。

## Phase 2 — Deterministic Risk Engine

- lot/exposure/position、SL、daily loss/DD
- spread gate、cooldown、trades/hour/day
- kill switch、stale/障害時fail closed
- property/integration/failure tests

**完了条件:** 全注文経路でRisk check必須、拒否理由を追跡可能。

## Phase 3 — Baselineとbacktest

- Rule-only baseline
- realistic fee/spread/slippage model
- 時系列splitとIS/validation/OOS runner
- regime別、version別レポート

**完了条件:** cost込みの再現可能なbaselineがある。

## Phase 4 — LLM adapter（shadowのみ）

- provider非依存adapterとschema validation
- prompt/model/strategy version固定
- sanitized prompt/response監査
- champion/challenger shadow比較
- LLM Gateway、provider/model routing、token/cost計測

**完了条件:** LLMがMT5/Risk設定へアクセスせず、baselineとの差を測れる。

## Phase 5 — Demo forward

- Rule-onlyとLLM版を同条件で並走
- latency、timeout、invalid output、cost、drift監視
- restart/recovery/MT5不一致の訓練
- rolling PF等のStrategy degradation detectionと自動停止訓練

**完了条件:** 事前登録した期間・件数・安全/成績ゲートを満たす。

## Phase 6 — 少額real

- 承認済みversionのみ有効化
- 厳しいrisk capと自動停止
- 実slippage/feeを再推定
- 段階増額またはrollback判定

**完了条件:** 事前条件を満たしても増額は自動にしない。人間が監査結果を確認する。

## 後続候補

- Interactive Trading Assistant（ChatSession、ContextBuilder、ChatLLM）
- MANUAL+のManualTradeCommandと権限・確認フロー
- チャート横Chatを備えたFastAPI/Web UI（Engineとは疎結合）
- Replay、Experiment Tracking、Strategy Comparison UI
- cheap model → high-performance modelの二段階routing
- news/text feature generator
- regime-aware routing
- 複数model challenger
- Edge Monitor（独立コンポーネント化）: 現状02-safety.mdの「昇格とロールバック」と03-evaluation-protocol.mdの「Production劣化検知」に分散しているrolling PF/expectancy/regime別成績の監視とStrategy停止・shadow降格判断を、Risk Engineとは別の専任コンポーネントとして切り出す
- VPS/冗長化、必要性を確認後にEA併用を再判断
