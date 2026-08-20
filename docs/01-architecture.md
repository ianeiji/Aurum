# Architecture

## 方針

開発支援AIにはClaudeを使用する。一方、実行時の売買判断LLMはClaude固定ではなく、OpenAI、Anthropic、ローカルモデル等を共通インターフェースで交換できる設計とする。開発ツールの選択と実運用モデルの採用判断を混同しない。

完成形は、人間がRisk上限、取引対象、稼働時間、Strategy、AUTO ON/OFF、緊急停止等のガードレールを設定し、その内側ではエントリー、position管理、決済、記録まで自動実行する。完全自動はAIへの全権委任を意味しない。Lot計算、最大損失、重複注文防止、Spread制限等は決定論的コードが強制する。

## Platformの二面と三層

Trading Platformを次の二面で設計する。

- **Live Trading:** 市場監視、Strategy判断、Risk審査、注文、position管理、決済、記録を行う。
- **Evaluation / Experiment:** Backtest、Replay、Shadow Trading、Forward Test、Metrics、Strategy Comparison、Experiment Tracking、Strategy degradation detectionを行う。

両面を、次の三層で一貫して捉える。

1. **Edge:** コスト控除前に正の期待値を生むStrategy仮説。
2. **Execution:** 判断を重複や状態不整合なく注文・約定・管理へ変換する能力。
3. **Risk:** 損失、exposure、頻度、異常状態を許容範囲へ制限する強制機構。

Safety対策の多くはExecution/Riskを改善するが、Edgeそのものは作らない。利益可能性はStrategy/Evaluationが、Spread、fee、slippage、swapおよびLLM費用控除後にも残るEdgeを発見・維持できるかに依存する。

```text
MT5 Market/Account State
          ↓
Market Data Adapter ─→ Feature/Regime Builder
          ↓                    ↓
    Market Snapshot ─→ Strategy Interface ─→ LLM Gateway
                         ├─ Rule-only baseline
                         ├─ LLM strategy/filter
                         └─ Shadow challengers
                                  ↓
                         StrategyDecision
                                  ↓
                    Deterministic Risk Engine
                                  ↓ PASS only
                         Order Manager → MT5
                                  ↓
                     Audit/Event/Metric Store

Chat Interface → User Intent → ContextBuilder → Market/Position Context
                                          ↓
                                      ChatLLM
                                          ↓
                     Analysis response / ManualTradeCommand
                                          ↓ command only
                              Deterministic Risk Engine
```

## 境界と責務

- **Market Data Adapter:** MT5から価格、spread、口座、positionを取得する。MT5の実状態を正とする。
- **Feature/Regime Builder:** MA、ATR、volatility等を決定論的に計算する。look-aheadを禁止する。
- **Strategy Interface:** 同一snapshotから構造化Decisionを返す。注文APIへアクセスしない。
- **LLM Gateway:** Trading Engine/Strategy/Chat側に共通interfaceを提供し、Claude、GPT、cheap model、local model等のroutingと差し替えを可能にする。
- **LLM Adapter:** Gateway配下でprovider固有API、timeout、schema validationを隔離する。失敗時はWAIT扱いにする。
- **Risk Engine:** lot、総exposure、SL、日次損失、DD、spread、頻度等を決定論的に検査する。
- **Order Manager:** PASS済みintentだけを送信し、idempotency、fill、reconciliationを扱う。
- **Observability:** 判断から約定/決済まで同一traceで追跡する。
- **ChatSession:** 会話状態、対象symbol、表示timeframe、権限、参照したsnapshotを管理する。
- **ContextBuilder:** User Intentに応じて現在価格、M1/M5/M15/H1等の必要足、MA、ATR、Spread、直近高安、position、含み損益、当日履歴を自動取得する。
- **ChatLLM:** 構築済みContextを使って即時分析する。口座値や指標を独自に推測・再計算しない。
- **ManualTradeCommand:** チャット注文を型付きintentへ変換する。直接発注せず、必ずRisk EngineとOrder Managerを通る。

AUTO StrategyとChat Assistantは、Market Data、Indicators/Feature、Position State、Risk Engine、Order Manager、Audit Storeを共用する。将来のWeb UIではチャート横にChatを配置し、表示中のGoldと現在のMT5状態を暗黙Contextとして相談できるようにする。

## 運用モード候補

| Mode | AI分析 | 注文主体 | Position管理 |
|---|---|---|---|
| OFF | なし | なし | 監視・安全な既存position処理のみ |
| ASSIST | あり | 人間がMT5等で注文 | 人間主体 |
| MANUAL+ | あり | 人間がChatから指示 | 指示と設定に従いシステムが実行 |
| AUTO | Strategy/LLM | システム | システムが管理・決済 |

MANUAL+を含む全注文でRisk Engineを迂回不可とする。OFF切替時の既存positionの扱いは、新規発注停止と一括決済を別操作にする。

## Interactive Trading Assistant

「今Goldどう？」「1分足も見て」「今のポジションどうする？」のような入力を受け、次の流れで処理する。

```text
User Intent
  → ContextBuilder
  → 必要データをMT5/feature storeから取得
  → current Market/Position Context
  → ChatLLM
  → 即時フィードバック
```

スクリーンショットや現在価格の手入力を要求しない。回答には参照時刻とdata freshnessを紐付け、古いContextで注文しない。

## StrategyDecision契約（概念）

```json
{
  "action": "BUY | SELL | WAIT",
  "symbol": "XAUUSD",
  "timeframe": "M5",
  "rationale": ["..."],
  "signal_tags": ["trend", "event-risk"],
  "valid_until": "timestamp",
  "decision_id": "uuid"
}
```

LLMはlot、最大損失、Risk上限を確定しない。不正schema、古いsnapshot、timeout、矛盾したactionはfail closedでWAIT/REJECTとする。

## 比較設計

同一snapshotをRule-only baseline、現行LLM、challengerへ配布できるようにする。shadow strategyは判断を記録するが発注しない。比較では同一のcost modelとrisk policyを使い、LLM追加による純増分を測る。

Rule A / Rule B / LLM / Hybrid等を同一市場・同一snapshotで並走させ、LLM追加がnet PF、expectancy、DD、安定性を本当に改善するか実測する。Production Strategyはrolling PF等を承認時の期待範囲と比較し、劣化時に新規取引停止、shadow降格、再評価を判断できるようにする。

## LLM呼び出し境界

通常監視、価格更新、指標計算、Spread/Risk判定、SL監視、注文状態確認はPythonの決定論的処理とする。5分足確定や機械的事前フィルタ通過後など、LLM判断が必要な時だけGatewayを呼ぶ。Chatもユーザー質問時だけ呼ぶ。将来はcheap/fast modelで事前判定し、必要な候補だけ高性能modelへ送る二段階routingを許容する。

## 実行モデル

全体は`asyncio`中心とし、同期のMT5 Python APIはAdapter内へ隔離する。Trading EngineはFastAPIから独立させ、API/将来の管理画面は操作・参照の入口に限定する。
