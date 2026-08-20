# fx-ai-trader documentation

FX/貴金属向けの、自動売買・戦略評価・対話型売買支援を統合したTrading Platformの設計資料です。LLMは交換可能な分析・判断コンポーネントとして利用します。

> [!CAUTION]
> 本プロジェクトは利益を保証しません。LLMの流暢な説明は予測精度の証拠ではなく、実売買は段階評価と損失上限を通過した場合だけ許可します。

個人利用限定のプロジェクトであり、OSS化・販売・第三者への公開は想定しない。最優先事項は実利益を出すことであり、安全設計はその手段として維持する。

## 設計の要点

- 人間がRisk上限、対象、時間、Strategy、AUTO ON/OFF、緊急停止を設定し、その範囲内ではエントリーから決済・記録まで自動化する。
- 「完全自動」と「AIへ全権委任」を分け、Lot、最大損失、重複注文、Spread制限は通常コードで強制する。
- PlatformをLive TradingとEvaluation/Experimentの両面で設計し、Edge / Execution / Riskを分離する。
- LLMからMT5へ直接発注しない。全注文を決定論的なRisk Engineへ通す。
- 開発支援AIはClaudeを想定するが、売買判断LLMはClaude固定ではない。
- Rule-only baselineとLLM併用版を、同一データ・同一コスト条件で比較する。
- MT5接続済みChatから、スクリーンショットや価格入力なしで相場・positionを相談できる。
- Claude Code定額枠は開発・分析へ使い、本番推論は必要時だけ従量APIを呼ぶ。
- spread、fee、slippageを含むnet成績で判断する。
- prompt、model、strategy、data、設定をバージョン管理する。
- in-sample → validation → out-of-sample → demo forward → 少額realの順で昇格する。

## ドキュメント

- [研究知見](docs/research/llm-trading-findings.md)
- [アーキテクチャ](docs/01-architecture.md)
- [安全設計](docs/02-safety.md)
- [評価プロトコル](docs/03-evaluation-protocol.md)
- [データと観測性](docs/04-data-and-observability.md)
- [ロードマップ](docs/05-roadmap.md)
- [運用・LLMコスト方針](docs/06-operations-and-llm-cost.md)
- [Claude向け開発規約](CLAUDE.md)
- [コミット規約](COMMIT_CONVENTION.md)
- [ブランチ・PR運用](BRANCH_AND_PR_CONVENTION.md)
