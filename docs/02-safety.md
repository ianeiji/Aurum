# Safety and deterministic Risk Engine

## 不変条件

1. Strategy/LLMからMT5へ直接発注しない。
2. 全注文はRisk EngineのPASSと一意なrisk-check IDを必要とする。
3. LLM出力でRisk設定、lot上限、損失上限を変更しない。
4. 新規注文には有効なstop lossを必須とする。
5. データ欠損、stale、LLM timeout、schema不正、状態不一致ではfail closedとする。
6. MT5の実position/order/balanceを正として定期reconciliationする。
7. Risk拒否と手動介入を監査ログに残し、握りつぶさない。
8. Chat/ManualTradeCommandを含む全経路で同じRisk Engineを通し、手動指示を例外にしない。

## 注文前チェック

- trading enabled / kill switch
- market/session、news blackout（有効時）
- snapshot freshness、symbol/timeframe整合
- spread上限、想定slippage/最小期待値
- SL距離、broker stop level、risk per trade
- max lot、max total lot、max positions、symbol/currency exposure
- daily loss、rolling drawdown、連敗/異常検知
- cooldown、最大trades/hour、最大trades/day
- 重複decision/order、既存注文との衝突
- terminal接続、market可用性、口座モード

## 注文後安全性

- idempotency keyによる重複発注防止
- request価格、fill価格、slippage、feeを保存
- partial fill/reject/timeout後にMT5を再照合
- orphan positionを検知し、新規発注を停止
- heartbeat欠落、DB障害、時計ずれで新規発注停止
- emergency stopは新規発注を止める。既存positionを閉じるかは別の明示操作とする

## 設定変更

Risk上限はLLMやStrategyが変更できない。管理操作には認証、型/範囲検証、変更前後、操作者、理由、時刻、policy versionを残す。上限緩和は即時自動適用せず、必要に応じて再起動または二段階承認を導入する。

人間が設定する範囲は、Risk上限、取引対象、稼働時間、Strategy割当、OFF/ASSIST/MANUAL+/AUTO、緊急停止等とする。自然言語の曖昧な依頼だけでRisk設定や運用モードを緩和しない。MANUAL+のlot指定が上限を超える場合は縮小せず明示的にREJECTする方針を既定とする。

## 昇格とロールバック

評価ゲート未通過のstrategy/model/promptをreal executionへ割り当てない。監視閾値超過、version不明、drift、想定外コストでは現行championを停止または直前の承認済みversionへ戻す。自動でriskを増やして回復を狙わない。
