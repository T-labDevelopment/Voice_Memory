# VoiceMemory v2 正本受領・検証状況記録（2026-11-11）

## 正本の指定
2026-11-11 16:44 JST、ユーザーからアップロードされた `voicememory-2026-11-11_164201.zip` を**v2現行設計の基準データ**として指定された。2026-11-10 の v2 開発PCBより、本ZIP内のKiCadファイルを優先する。

| 項目 | 確認結果 |
|---|---|
| ZIP | `voicememory-2026-11-11_164201.zip` |
| SHA-256 | `a64d1d4d439a141a7048c7fe233227507cebeaa69209cd91ddddc90118438c7a` |
| サイズ | 217,137 bytes |
| ZIP CRC検査 | `zipfile.testzip() == None`（検査合格） |
| KiCad設計 | 回路図・PCB・プロジェクト設定・シンボル・フットプリント・lib-table |
| 元ZIPファイル数 | 9件（`.kicad_prl`含む） |
| Gitに展開するKiCadファイル数 | 8件（個人設定 `.kicad_prl` は除外） |
| 既存v2 SCH | **バイト一致**（SHA256一致） |
| 既存v2 PCB | **差分あり**（部品再配置・配線更新・GNDゾーン塗りつぶしなど） |
| 既存v2 library | RJ45フットプリントのみ差分あり。SW、シンボル、fp-lib-table、sym-lib-tableは一致 |
| 既存v2 .kicad_pro | 差分あり |
| 過去v1の取り扱い | v1試作は別枠・費用計算対象外、変更せず |
| 設計ファイル読込み | ZIPのテキスト構造、JSON等を一部検査 |
| 現行Gitブランチ | `develop/v2` |
| ERC | **ユーザー申告：実施済み**。正式レポートは本ZIPに未収録 |
| DRC | **ユーザー申告：実施済み**。正式レポートは本ZIPに未収録 |
| ERCエラー0／警告0 | **未確認**。レポート不在のためゼロ件を裏付ける証跡なし |
| DRCエラー0／警告0 | **未確認**。レポート不在のためゼロ件を裏付ける証跡なし |
| ChatGPT側のKiCad CLI再実行 | **未実施**（利用環境に`kicad-cli`なし） |
| 実機検証・製造承認 | 未確認・未承認 |

## 変更・統合方針

- 本ZIPのSHA-256を**v2基準スナップショットの同一性識別子**とする。
- 元ZIPはGit `hardware/source-archives/v2-baseline/voicememory-2026-11-11_164201.zip` に**無変更保存**する。
- KiCadプロジェクトは `hardware/kicad/voicememory/` に同内容を展開するが、端末依存 `.kicad_prl` はGit管理から除外する。
- 設計と無関係な歴史的README、旧監査資料は削除しない。2026-11-10までのコンデンサ干渉候補の監査は**以前のPCBに対するもの**として保存し、今のPCBでも残るとは断言しない。
- 従来の旧ブランチ、`main`、旧v1タグやバックアップは書換えない。
- ユーザーからのERC/DRC済み申告は受け入れるが、**結果数値・実行環境・KiCadバージョン・DRC除外設定は未確認**であり、0件や製造可能との断定はしない。
- 本ZIPを再現可能な製造検証の入力基準とし、検証結果が後日入手できればこの正本に対する別の証跡ファイルとして登録する。

## ファイルごとの差分（2026-11-10 v2との比較）

| 入力ZIP内 | 差分 | 取り扱い |
|---|---|---|
| `voicememory.kicad_sch` | 既存v2と同一 | 変更なし |
| `voicememory.kicad_pcb` | 差分あり、長さ484,290→795,879 bytes | **今回のPCBを正本へ更新** |
| `voicememory.kicad_pro` | 差分あり | **今回の設定を正本へ更新** |
| `Voice_Memory.pretty/RJ45_8P8C_THT_15.91x15.10.kicad_mod` | 差分あり | **今回のFPを正本へ更新** |
| `Voice_Memory.pretty/SW_TVGP01_G73BB_12mm.kicad_mod` | 同一 | 変更なし |
| `Voice_Memory.kicad_sym` | 同一 | 変更なし |
| `fp-lib-table` / `sym-lib-table` | 同一 | 変更なし |
| `voicememory.kicad_prl` | 端末固有のUI状態 | 元ZIPのみに保管・展開しない |

PCB構造の静的比較（参考）:
- 前版 / 新版: footprints 65/65、segments 455/382、vias 154/121、zone定義1/1、filled polygons 0/10。KiCadアプリでのPCB整合は未評価。
- 元SCHが同一であることは、PCBの配線導通やネット割当が完全に一致するという意味ではない。

## アーカイブからの再現方法

- 元ZIPを解凍して`hardware/kicad/voicememory/`に配置（`.kicad_prl`は除外）。
- ローカルKiCadで開くときは `fp-lib-table` と `sym-lib-table` を同じディレクトリに置く。
- 正本以外の `scripts/` と `docs/` は**開発補助・参考資料**として扱い、当該ZIPの一部であると誤認しないこと。

## 出典

- ユーザー指定の添付 `voicememory-2026-11-11_164201.zip`（2026-11-11 16:44 JST）
- 比較元の `develop/v2`・2026-11-10 KiCadデータ（直前HEAD）
- GitHubに保存した元ZIP（上記パス）
