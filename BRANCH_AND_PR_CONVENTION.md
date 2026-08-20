# Branch and PR Convention

Aurumでは、課題管理をGitHub Issuesで行う前提で、Issue単位の軽量GitHub Flowを採用する。

開発者は1人であり、Cursor + Claudeを利用するため、`COMMIT_CONVENTION.md`と同様に過度に複雑な運用にはしない。

## 基本方針

- Issueに対応する実装は、Issueごとにブランチを切りPRを作成してmainへマージする。
- ドキュメントのみの軽微な変更（typo修正、文言調整等）は、Issueを起票せず直接mainへコミットしてよい。
- ソロ開発でもPRは作成する。理由は以下の2点。
  - 変更の差分をレビュー画面でまとめて見返し、セルフレビューの区切りにできる。
  - 将来テストやCIを導入した際に、マージ前のチェックポイントとして機能する。

## ブランチ命名

```text
<issue番号>-<英語の簡潔なslug>
```

例:

```text
21-daily-loss-limit
31-anthropic-provider
43-order-duplicate-fix
```

Issueに紐づかない変更（ドキュメントのみ等）はブランチを切らず直接mainにコミットしてよい。

## PR運用

- PRのdescriptionに対応Issueを記載し、マージでIssueが自動closeされるようにする。

  ```text
  Closes #21
  ```

- PRタイトルはコミットメッセージと同じ形式（`COMMIT_CONVENTION.md`）に合わせる。
- 1PR = 1Issue = 概ね1つの論理的変更を基本とする。Issueが大きい場合は分割を検討する。
- マージ方法は squash merge を基本とし、mainの履歴を1Issue=1コミットに近い形へ揃える。ただしIssue内で意味のある複数コミットに分けたい場合はregular mergeでもよい。

## 安全性が絡む変更のPRチェック

Risk Engine、Order Manager、LLM Gateway等、`CLAUDE.md`の絶対ルールに関わる変更を含むPRでは、マージ前に`CLAUDE.md`の「変更時チェック」を確認する。

- Risk bypass経路を増やしていないか
- look-ahead/data leakageを入れていないか
- versionとdecision/order traceが欠落していないか
- retryで重複発注しないか
- error/partial fill/restart後にMT5と再照合できるか
- cost込みのテストとbaseline比較があるか

ソロ開発のため他者レビューは無いが、PRの差分を挟むことでこのチェックリストを実行するタイミングを明確にする。

## この運用のトレードオフと懸念

- **懸念:** 全ての変更にブランチ+PRを要求すると、ソロ開発では単なる作業コストの追加になり、開発速度を落とす可能性がある。特にPhase 0〜1のような設計・調査段階では、細かい変更ごとにPRを作る意味が薄い。
- **対応方針:** Issueに紐づく実装（Phase 1のMT5取得処理、Phase 2のRisk Engine等）はブランチ+PRを必須とし、Issueに紐づかないドキュメント微修正やchoreは直接mainコミットを許容する。安全性が絡む変更ほどPRを厳格に使い、そうでない変更ほど省略を許すというメリハリを付ける。
- **見直しのタイミング:** Phase 1着手時に実際の作業単位を見ながら、ブランチ命名やsquash方針が実情に合っているか再確認する。運用が形骸化する場合はルール自体を簡略化する。

## Notionとの役割分担

`COMMIT_CONVENTION.md`と同様、Notion（Roadmap/Kanban/Milestone）、GitHub Issues（実装単位のタスク）、Git（ブランチ/PR/コミット）の役割分担を維持する。ブランチ名やPRにNotionのUnique ID等は含めない。
