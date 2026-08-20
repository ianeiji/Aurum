# LLMトレーディング調査知見と設計アクション

最終更新: 2026-08-20

## 結論

感情を排除することは、ルール逸脱、損切り拒否、FOMO、ロット増加などによる期待値の毀損を減らす。しかし、それ自体は市場に対するedgeを作らない。LLMはもっともらしい説明を作る能力と将来価格を予測する能力が同じではなく、単独での収益性もモデルや期間により不安定である。

本アプリでは、LLMを交換可能なStrategy/Analysis componentとして通常コードで囲み、執行とリスク制御は決定論的にする。採用判断は「AIらしさ」ではなく、コスト控除後にbaselineを継続して上回るかで行う。

この整理は、システムをEdge / Execution / Riskの三層として扱うことを意味する。堅牢なExecutionとRiskはEdgeを守るが作らない。Rule A / Rule B / LLM / Hybridを同条件で比較し、取引コストとLLM費用控除後にも優位性が残る構成だけをProduction候補にする。

## 調査から得た示唆

### 1. LLM単独売買の成績は不安定で、モデル差が大きい

HKU Business Schoolが公表した短期の実市場実験では、同一条件でもモデルごとに成績と取引頻度が大きく異なった。短期間の好成績は長期的なedgeの証明ではない。Claudeを含む特定ベンダー・モデルを先験的に勝者としない。

**設計アクション:** 共通の`StrategyDecision`契約を設け、model/providerを交換可能にする。champion/challenger方式で比較し、モデル変更時は別バージョンとして評価をやり直す。

### 2. 説明力と予測力は違う

LLMは「MAが上向きだからBUY」のような一貫した説明を生成できるが、その流暢さは校正済み確率や正の期待値を保証しない。confidenceの自己申告も、そのままポジションサイズに利用できない。

**設計アクション:** LLM出力を構造化し、BUY/SELL/WAIT、理由、入力参照を記録する。LLM confidenceから直接ロットを決めず、予測の校正と実績を別途測る。

### 3. transaction costとslippageが小さなedgeを消す

個人検証ではgrossで僅かに正でも、feeとslippageを入れると負になる例が報告されている。XAUUSD M5のような短期売買では特に重要である。

**設計アクション:** backtest/forward/liveのすべてでspread、commission、swap、slippageを個別記録し、net expectancyを主指標にする。異常spread時は新規注文を拒否する。

### 4. 売買頻度は利益と同義ではない

積極性は機会を増やす一方、コスト、重複ポジション、障害時の被害を増やす。LLMが保守的すぎることだけが失敗原因ではない。

**設計アクション:** Risk Engineにcooldown、時間当たり/日当たりの最大注文数、最大同時ポジション数、最大総エクスポージャを実装する。拒否理由も保存する。

### 5. overfittingと多重試行が結果を作れる

多数のindicator、閾値、時間帯、prompt、modelを試し、最良結果だけを選ぶと偶然をedgeと誤認しやすい。LLMによる反復最適化も例外ではない。

**設計アクション:** 時系列を守ってin-sample、validation、完全未使用out-of-sampleを固定する。試行台帳を残し、OOSを見た後の変更は新しい実験として全工程をやり直す。

### 6. regime changeで過去の優位性が崩れる

trend/range、高/低volatility、news、risk-on/off、流動性などの状態が変われば、同じ戦略の期待値は変わる。

**設計アクション:** market snapshotにregime特徴を保存し、regime別成績とrolling指標を監視する。劣化時は自動でロットを増やさず、pauseまたは再評価へ戻す。

### 7. prompt/model/strategyの変更は戦略変更である

promptを途中変更すると前後比較が混ざる。モデル提供側の更新も挙動を変え得る。

**設計アクション:** 各判断に`prompt_version`、`model_provider`、`model_name`、取得可能なら`model_revision`、`strategy_version`、`risk_policy_version`、`data_version`を紐付ける。同一集計へ無条件に混ぜない。

### 8. LLMが有効なのは曖昧な文脈統合かもしれない

決定論的に算出できるMA、ATR、spread、position、損失額をLLMに再計算させる必要はない。一方、ニュース、相反する市場シグナル、イベント接近などの文脈統合は候補になる。

**設計アクション:** Pythonで計算した正規化済みMarket Contextを渡し、LLMの責務を解釈/分類へ限定する。計算、口座状態、リスク、発注は通常コードを正とする。

### 9. LLM費用もStrategyコストである

24時間の監視・指標・Risk処理をLLMへ送る必要はない。LLM費用が取引あたりEdgeを超えれば、売買前成績が良くても実運用価値はない。

**設計アクション:** 機械的filter後と対話要求時だけLLMを呼び、token/model/call単位の費用を記録する。Claude Code等の開発サブスクリプションとProduction inference課金を分離する。

## 懸念 → このアプリでの設計アクション

| 懸念 | 設計アクション | 検証方法 |
|---|---|---|
| LLM単独の収益性が不安定 | LLMを交換可能にし、WAIT可能な補助判断器として扱う | model別OOS/forward net成績 |
| モデル差・更新差 | provider非依存I/F、model version記録、champion/challenger | 同一snapshotのshadow比較 |
| 説明力と予測力の混同 | 構造化出力、確率校正、自己confidenceでlotを決めない | calibration、Brier score、expectancy |
| cost/slippage | 実コストモデル、spread gate、fill差の保存 | gross対net、cost/trade |
| overfitting | 時系列split、未使用OOS、全試行記録 | OOS degradation、試行数 |
| regime change | regimeタグ、rolling監視、kill/pause | regime別PF、DD、drift alert |
| prompt drift | promptをimmutable artifactとして保存 | version別集計と再現テスト |
| LLMのルール逸脱 | schema validation、許可action限定、fail closed | invalid/rejected率 |
| 過剰取引 | cooldown、rate limit、position/exposure上限 | turnover、trades/day、cost比率 |
| LLMがRiskを上書き | 決定論的Risk Engineを注文の必須ゲートにする | bypass不可能な統合テスト |
| AI追加の価値が不明 | Rule-only baselineを常設 | paired/A-B比較、差分CI |
| 短期好成績の誤認 | 段階的評価と昇格条件 | IS→VAL→OOS→forward→少額real |

## 評価指標

勝率だけを最適化しない。最低限、Net PnL、Profit Factor、Expectancy/trade、Sharpe/Sortino、Max Drawdown、平均利益/平均損失、exposure、trade数、turnover、spread/fee/slippageを追う。統計的不確実性、期間、相場regime、サンプル数を併記する。

期待値は概念的に次で評価する。

```text
E = P(win) × AvgWin - P(loss) × AvgLoss - TradingCosts
```

## 評価段階

1. **In-sample:** 仮説と実装を開発する。ここでの成績は採用根拠にしない。
2. **Validation:** パラメータ、prompt、model候補を選ぶ。
3. **Out-of-sample:** 完全未使用の時系列で一度評価する。変更したら新実験とする。
4. **Demo forward:** 実時間、実spread、遅延、拒否、障害を含めて評価する。
5. **少額real:** 損失許容額内でfill/slippageと運用挙動を確認する。段階的にのみ増額する。

各段階の詳細なゲートは[評価プロトコル](../03-evaluation-protocol.md)を参照する。

## 情報源と読み方

以下は設計仮説を作るための資料であり、収益保証や再現済み証拠ではない。Redditは自己申告、短期、小標本、選択バイアスを含む。論文もデータリーク、cost仮定、再現性を個別確認する。

- [HKU Business School: AI agents trading performance](https://www.hkubs.hku.hk/media/school-news/testing-ai-in-the-real-world-hku-business-school-released-ai-agents-trading-performance/)
- [Reddit: XAUUSD botの事例](https://www.reddit.com/r/algotrading/comments/1lgrb1f/finally_created_my_own_algo_using_ai_and_this_was/)
- [Reddit: 1か月・107取引のLLM agent報告](https://www.reddit.com/r/ai_trading/comments/1vqsyv4/i_ran_an_llm_trading_agent_247_for_a_month_107/)
- [Reddit: costs後にedgeが消えた報告](https://www.reddit.com/r/Trading/comments/1u8cunp/negative_results_my_ai_trading_bot_has_no_edge/)
- [Reddit: LLM tradingの実践議論](https://www.reddit.com/r/algotradingcrypto/comments/1uo87ng/has_anyone_actually_built_a_profitable_trading/)
- [SSRN: AgenTrade](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6998159)
- [ScienceDirect: multi-agent trading study](https://www.sciencedirect.com/science/article/abs/pii/S0306457325004078)
- [arXiv: LLM trading research review](https://arxiv.org/abs/2605.19337)
- [Reddit: prompt freezeを含むLLM比較](https://www.reddit.com/r/LocalLLaMA/comments/1rnvps2/im_benchmarking_10_llms_including_deepseek_llama/)
