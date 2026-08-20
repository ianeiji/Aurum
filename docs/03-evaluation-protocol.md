# Evaluation protocol

## 原則

- 時系列を維持し、未来情報をfeatureや正規化へ混ぜない。
- benchmarkはbuy-and-hold等だけでなく、同一risk/cost条件のRule-only baselineとする。
- grossではなくnetを主要判定にする。
- 1回の好成績や勝率だけで昇格しない。
- OOSを見た後の修正は新しいversion/experimentとして最初から評価する。

## 段階とゲート

Evaluation/Experiment面はBacktest、historical Replay、Shadow Trading、Demo/Real Forward Testを同一Decision契約とMetric定義で実行する。全試行をExperiment Trackingへ登録し、Strategy Comparisonとdegradation detectionへ接続する。

### 1. In-sample

仮説、実装、feature、prompt候補を開発する。look-ahead、重複発注、Risk bypassのテストを通す。成績は昇格根拠にしない。

### 2. Validation

候補数を制限し、事前定義した指標でmodel/prompt/parameterを選ぶ。全試行をexperiment registryへ残す。

### 3. Out-of-sample

完全未使用期間で一度だけ主要評価を行う。net expectancy、PF、DD、cost耐性、regime別頑健性、baseline差と不確実性を確認する。

OOS期間は単一ブロックとして使い切らず、OOS-A/OOS-B等の複数区間に分けて予約する。OOS-Aを見てstrategyを修正した場合、OOS-Aはdevelopment dataとして消費済み扱いにし、次の主要評価は未消費のOOS-Bで行う。同一OOS区間を見ては直し見ては直しを繰り返すと、OOS自体が事実上のdevelopment dataとなり評価そのものが過学習する。

### 4. Demo forward

十分な期間とtrade数を事前に設定し、実時間のspread、slippage相当、遅延、API障害、再起動、reconciliationを検証する。shadow baseline/challengerを並走させる。

### 5. 少額real

失っても許容できる固定上限で開始する。実fill、commission、swap、運用障害を確認する。増額は時間経過、trade数、net成績、安全指標のすべてを満たした場合だけ段階的に行う。

## 事前に固定する項目

- 対象symbol/timeframe/期間とsplit境界（OOS-A/OOS-B等の予約区間を含む）
- strategy/model/prompt/risk/data version
- cost/slippage仮定とstress条件
- primary/secondary metrics
- 最低trade数/期間、最大DD、停止条件
- baseline、昇格基準、失格/ロールバック条件

具体的な数値は実装・broker・口座規模の確定後に設定する。結果を見てから閾値を都合よく変更しない。

## Baseline比較

同一snapshot、同一execution assumptions、同一Risk Engineで以下を比較する。

1. Rule-only
2. Rule + LLM filter
3. LLM strategy（研究用、初期はshadow）
4. Rule A / Rule B / LLM / Hybrid等のchallenger群

LLM版がnet指標、DD、安定性を含めbaselineより実質的に改善しない場合は採用しない。モデル間比較も同じ条件で行う。

## Production劣化検知

Production Strategyはrolling PF、net expectancy、DD、cost/trade、trade頻度、regime別成績を承認時のOOS/forward分布と比較する。事前登録した閾値を割った場合は、新規取引停止、shadowへの降格、直前の承認済みversionへのrollback、再評価のいずれかを行う。小標本の一時変動と構造的劣化を区別するため、最低trade数・観測期間と重大な即時停止条件を別に定義する。

## Cost stress

通常想定に加え、spread/slippage拡大ケースを評価する。APIを使うStrategyではLLM費用もnet評価へ含める。僅かなcost増加でexpectancyが負になるstrategyはrealへ昇格しない。
