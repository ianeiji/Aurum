# Commit Convention

Aurumでは、コミットメッセージに **Conventional Commits** を採用する。

開発者は1人であり、Cursor + Claudeを利用するため、履歴の可読性とGitHub Issueとの追跡性を確保しつつ、過度に複雑な運用にはしない。

## Format

基本形式:

```text
<type>(<scope>): <description> (#<github-issue>)
```

- `type`: 英語
- `scope`: 英語
- `description`: 日本語
- GitHub Issueがない場合はIssue番号を省略可能

例:

```text
feat(mt5): M5ローソク足の取得を追加 (#13)
fix(order): 注文の重複送信を防止 (#43)
feat(risk): 最大合計Lotの制限を追加 (#18)
test(risk): 日次損失制限のテストを追加 (#19)
```

Issueに紐づかない変更:

```text
docs: 初期プロジェクトドキュメントを追加
chore: uvでPythonプロジェクトを初期化
```

## Type

主に以下を使用する。

| Type | 用途 |
| --- | --- |
| `feat` | 新機能 |
| `fix` | バグ修正 |
| `docs` | ドキュメントのみの変更 |
| `refactor` | 挙動を変更しない内部構造の改善 |
| `test` | テストの追加・変更 |
| `chore` | 開発環境、設定、依存関係など |
| `perf` | パフォーマンス改善 |
| `build` | ビルド・依存関係・パッケージング |
| `ci` | CI/CD関連 |
| `revert` | 既存コミットの取り消し |

新しいtypeを安易に増やさない。

## Scope

scopeは変更対象の主要コンポーネントを表す。

初期候補:

```text
mt5
market
strategy
llm
risk
order
chat
api
db
evaluation
ui
```

例:

```text
feat(mt5): ポジション取得処理を追加 (#14)
feat(market): M5ローソク足からATRを計算 (#27)
feat(llm): Anthropicプロバイダーを追加 (#31)
feat(strategy): ハイブリッド戦略を追加 (#35)
feat(chat): Market Contextの自動注入を追加 (#42)
fix(risk): 合計Lot上限を超える注文を拒否 (#48)
```

変更がプロジェクト全体にまたがる場合や、scopeを付ける意味が薄い場合は省略してよい。

```text
docs: アーキテクチャを更新
chore: gitignoreを更新
```

## Description

descriptionは**日本語**で記述する。

以下を基本ルールとする。

- 日本語で記述する
- 簡潔にする
- 「何を変更したか」が分かるようにする
- 原則として体言止めではなく、変更内容を表す動詞で終える
- 文末に句点 `。` を付けない
- コード上のクラス名、API名、ライブラリ名などは無理に日本語化しない

良い例:

```text
feat(mt5): M5ローソク足の取得を追加
fix(order): 注文の重複送信を防止
refactor(risk): Exposure計算を専用クラスへ分離
feat(llm): Anthropic APIへの接続を追加
```

避ける例:

```text
update
修正
いろいろ変更
MT5対応
バグ対応
```

## GitHub Issue

実装タスクはGitHub Issuesで管理する。

Issueに対応するコミットでは、コミットメッセージ末尾にIssue番号を付ける。

```text
feat(risk): 日次最大損失による取引停止を追加 (#21)
```

Issue番号は先頭には置かない。

採用しない形式:

```text
#21 feat(risk): 日次最大損失による取引停止を追加
AUR-21 feat(risk): 日次最大損失による取引停止を追加
```

Conventional Commitsの主要部分を先頭に保つ。

## Notionとの役割分担

Aurumでは以下のように役割を分離する。

```text
Notion
→ Roadmap
→ Kanban
→ Milestones
→ Phase
→ 人間向けのプロジェクト俯瞰

GitHub Issues
→ 実装単位のタスク

Git Commit
→ 実際のコード変更履歴
```

NotionのUnique ID等をコミットメッセージへ追加しない。

NotionとGitHub双方のIDをコミットへ含めると二重管理になるため、実装履歴はGitHub Issueへ紐づける。

## Commit Granularity

1コミットでは、原則として1つの論理的変更を扱う。

例えば以下は分けられる。

```text
feat(mt5): ローソク足取得処理を追加 (#13)

test(mt5): ローソク足取得処理のテストを追加 (#13)
```

ただし実装とそのテストが不可分で、小さな変更であれば1コミットにまとめてもよい。

コミット数を増やすこと自体を目的にしない。

## Breaking Changes

互換性を壊す変更では `!` を付ける。

```text
feat(strategy)!: StrategyのDecisionインターフェースを変更
```

必要であればコミット本文に理由や移行方法を記載する。

```text
BREAKING CHANGE: Strategy実装はTradingDecisionを返す必要があります。
```

Breaking Changeは頻繁に使用しない。

## Examples

```text
docs: 初期プロジェクトドキュメントを追加

chore: uvでPythonプロジェクトを初期化

feat(mt5): MT5への接続処理を追加 (#11)

feat(mt5): XAUUSDのTick取得を追加 (#12)

feat(mt5): M5ローソク足の取得を追加 (#13)

feat(risk): 最大合計Lotの制限を追加 (#21)

test(risk): 最大Lot制限のテストを追加 (#21)

feat(llm): Anthropicプロバイダーを追加 (#28)

feat(strategy): ハイブリッド戦略を追加 (#31)

feat(chat): 対話型トレーディングアシスタントを追加 (#40)

fix(order): 注文の重複送信を防止 (#43)

refactor(mt5): 同期MT5呼び出しをAdapterへ分離 (#46)

perf(market): ローソク足の重複取得を削減 (#52)
```

## Claude / Cursor

CursorおよびClaudeも本規約に従う。

`CLAUDE.md` から本ファイルを参照する。

```markdown
## Commit Convention

コミットメッセージは `COMMIT_CONVENTION.md` に従うこと。

- type / scope: 英語
- description: 日本語
```

Claudeがコミットメッセージを提案・作成する場合も同じ形式を使用する。

## Summary

Aurumの基本コミット形式:

```text
<type>(<scope>): <日本語の変更内容> (#<github-issue>)
```

例:

```text
feat(risk): 最大Lot制限を追加 (#18)
```

Issueがない場合:

```text
docs: アーキテクチャドキュメントを更新
```

**type / scopeは英語、descriptionは日本語**で統一し、Git履歴を見ただけで「どの領域に、どの種類の変更を行ったか」を素早く把握できる状態を維持する。