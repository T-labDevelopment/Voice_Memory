# Voice_Memory — GitHub同期・監査記録（2026-11-11）

## 対象と結論

- GitHub: https://github.com/T-labDevelopment/Voice_Memory
- 同期対象ブランチ: `fix/v1-cap-min0805-2026-11-10`
- 元のスナップショット取込コミット: `a7bf99665db25401f9d295c33bcf15de35999220`
- 取込元ローカルGit最終SHA（資料に記録）: `c046a9c71d5fb17172cf048e0ef63aef2eb75111`
- 参照元は2026-10-29に受領した `voicememory-2026-10-05_162836(2).zip`。後続の2026-10-30 ECOおよび2026-11-10コンデンサ見直しを**レビュー用**として含む。
- 2026-10-28に作成したファームウェア開発者向け仕様書（Markdown / Word / 日本語CID PDF）を `docs/firmware-hardware/v1/` に保存している。
- 上記のGitHubブランチには設計本体、仕様書、監査レポート、補助スクリプト、元ZIP、Git bundleの分割保管ファイルが実際に存在することをGitHub APIで確認。
- `main` は変更していない。設計の製造承認やmain統合を意味しない。

## 実際の格納先

| 分類 | GitHub上の相対パス |
|---|---|
| KiCad 10回路図・PCB・ライブラリ | `hardware/kicad/voicememory/` |
| 元の受領ZIP | `hardware/source-archives/voicememory-2026-10-05_162836(2).zip` |
| ファームウェア開発者向け資料 | `docs/firmware-hardware/v1/` |
| 電気・実装・干渉監査 | `hardware/reports/` |
| ECO・部品置換補助スクリプト | `scripts/` |
| 元ローカルGit履歴のバックアップ | `history/VoiceMemory_v1_git.bundle.part01`～`part04` |

## 履歴の扱い

このリポジトリの作業ブランチは、元ローカルGit開発履歴の各コミットを通常のGitHubコミットとしてpushしたものではなく、最終的な**ファイルスナップショットを1つの取込コミット**として登録したもの。元コミットのSHA・タグを通常のGitHub履歴として表示できる状態ではない。

元履歴は `history/README.md` に記載の手順で分割ファイルを連結し、`git bundle verify` で検証・復元できる構成で保存されている。連結後bundleの記録上のSHA-256は `677bc6f9998d67196d175fe80836b7aa592cea07f17e47a3af77cc02e0dca9ff`。この監査では連結バイト列を取得できていないため**SHA-256を再計算・照合したとは記載しない**。

## 資料の参照先に関する不足

`docs/firmware-hardware/v1/README.md` と `manifest_sha256.json` に列挙される `figures/*.png` の独立画像6件、および `sources/` に列挙されるRJ45寸法図PNG・参考写真JPEGの2件は、GitHubの最新ブランチのツリーに存在しない。したがって、**資料一式が完全なファイル単位でアップロード済みとは断言できない**。Word/PDFに図が埋め込まれているかどうかは本監査の検証対象外。元資料からの再取得・必要に応じた登録が残る。

## 製造・回路検証の状態

- KiCad 10の正式ERC/DRCは未実施。
- 2026-11-10の0805最小化／1206大型化の監査では、C7、C10、C16、C19の近傍に配線・ビアとの干渉候補を検出。
- PCBのゾーン再フィル、再配置・再配線、電気的動作および部品実装確認は未了。
- 本ブランチを**製造・発注可能な確定データとして扱わない**。

## 2026-11-11 GitHub API確認範囲

- GitHubリポジトリのpush権限およびブランチ存在を確認。
- `main` の基準SHA: `18db68bd812d28d3332150c28f7a15f3709870ae`
- 作業ブランチの取込コミット（上記）を確認。
- 作業ブランチの再帰ツリーおよび主要ファイルを確認。
- Git bundleの元バイト列、KiCadによる正式ERC/DRC、未収録画像の原本はこのチャットから取得・検証できていない。

この記録は同期と未完了点の監査であり、回路設計本体の変更を含まない。
