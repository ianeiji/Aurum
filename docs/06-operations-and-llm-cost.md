# Operations and LLM cost policy

## 人間と自動化の責務

人間はRisk上限、取引対象、稼働時間、Strategy、運用モード、AUTO ON/OFF、緊急停止を設定・承認する。その範囲内では、Live Tradingが監視、エントリー、position管理、SL/TP、決済、記録を自動で行う。

完全自動はAIへの全権委任ではない。Lot、最大損失、Spread、頻度、重複、exposure、停止条件、注文状態整合は通常コードが強制する。LLMがこれらを変更したり、Risk拒否を再解釈したりできない。

## 開発AIとProduction LLMを分ける

Claude CodeのPro/Max等の定額枠を、24時間稼働するTrading BackendのProduction inference APIとして流用する設計にはしない。

- **開発・研究:** Claude Code定額枠をコード作成、テスト、ログ解析、バックテスト分析、Strategy/Prompt改善へ最大限利用する。
- **実運用:** Anthropic/OpenAI等の正式な従量API、または承認済みlocal modelをLLM Gateway経由で必要時のみ利用する。

開発支援AIがClaudeであることは、売買判断LLMをClaudeへ固定する理由にならない。Provider、model、revisionはStrategyの一部として比較・version管理する。

## API呼び出し方針

次はPython/通常コードだけで処理し、LLMを呼ばない。

- 通常監視、価格・bar更新、MA/ATR等の指標計算
- Spread、market hours、data freshness、Risk判定
- Lot計算、SL監視、position/order状態確認、reconciliation
- kill switch、loss/DD上限、重複注文防止

LLMを呼ぶのは、5分足確定、機械的事前filter通過、曖昧な市場文脈の分類等、Strategy上の判断が必要な場合だけとする。Interactive Chatはユーザーが質問した時だけ呼ぶ。回答前にContext BuilderがMT5の最新状態を取得する。

将来候補として、cheap/fast modelが検討価値を判定し、必要なcaseのみ高性能modelへ送る二段階routingをLLM Gatewayに実装できる。ただし二段階化もbaseline比較、latency、false negative、総費用で採否を決める。

## Budget・KPI・停止

最低限、次をmodel/provider/strategy/environment別に計測する。

- `llm_cost/day`
- `llm_cost_per_decision`
- `cost_per_trade`（取引コストとLLM費用を区別・合算）
- `llm_cost/net_profit`
- input/output/cache token usage
- model usage、call数、latency、timeout、invalid response率

日次budgetと異常な費用増加にalertを設定する。Budget超過時は、暗黙に安価modelへ切り替えてStrategy意味を変えず、新規LLM判断を停止または承認済みfallbackへ切り替え、記録する。費用を含めたnet expectancy/PFでProduction継続を判断する。
