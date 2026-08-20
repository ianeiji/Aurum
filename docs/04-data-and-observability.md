# Data and observability

## 目的

「なぜ判断し、Riskがどう処理し、何が約定し、コスト後にどうなったか」を再現可能にする。通常ログはstdout/file、取引・AI・Riskの重要イベントはPostgreSQLへ保存する。

## 必須IDとversion

- `run_id`, `experiment_id`, `decision_id`, `risk_check_id`, `order_id`, `trade_id`
- `chat_session_id`, `llm_call_id`, `manual_command_id`（該当時）
- `strategy_version`, `prompt_version`, `risk_policy_version`, `feature_version`, `data_version`
- `model_provider`, `model_name`, `model_revision`（取得可能な場合）
- application commit SHA、config hash、環境（backtest/demo/real）

## Decision記録

- timestampとmarket timezone、symbol/timeframe
- market snapshotまたはimmutable参照/hash
- 使用feature、regimeタグ、データfreshness
- sanitized prompt/messages、schema、raw response参照
- action、rationale、signal tags、latency、token/cost、parse結果
- user intent、Context Builderが選んだdata/timeframe、context timestamp/freshness（Chat時）
- baseline/champion/challenger、shadow/liveの区別

秘密情報、口座資格情報、不要な個人情報は保存しない。promptへ含めない。

## Risk・Order・Trade記録

- requested action/lot/SL/TPと計算根拠
- PASS/REJECT、全rule結果、拒否コード、policy version
- pre-trade balance/equity/exposure/spread
- broker request/response、retcode、ticket、request/fill価格
- commission、spread cost、swap、slippage
- position lifecycle、close理由、gross/net PnL、R multiple

## Metrics

- net/gross PnL、expectancy、PF、Sharpe/Sortino、Max DD
- win rate、avg win/loss、exposure、turnover、trades/day
- fee/spread/slippageとgross edgeに占める割合
- Risk reject率/理由、invalid LLM output率、timeout、latency
- version別、regime別、symbol別、時間帯別の成績
- baselineとの差、rolling performance、calibration/Brier score（確率を出す場合）
- `llm_cost/day`, `llm_cost_per_decision`, `cost_per_trade`, `llm_cost/net_profit`
- input/output/cache token usage、model/provider別call数・費用・latency・error率

## アラート

- daily loss/DD/頻度/spread閾値
- feed stale、clock skew、MT5/DB切断、reconciliation不一致
- invalid schema/timeout急増、model/prompt version不明
- rolling expectancy/PFの悪化、cost比率急増、regime別drift
- LLM日次budget超過、decision当たり費用急増、想定外model routing

アラートは通知だけでなく、重大度に応じて新規取引を自動停止する。停止理由と解除操作を監査する。

## 再現性

datasetの期間、取得元、欠損補完、timezone、bar確定規則、cost modelをmanifest化する。実験結果はversionの組み合わせ単位で集計し、prompt/model変更前後を同じ戦略として混ぜない。
