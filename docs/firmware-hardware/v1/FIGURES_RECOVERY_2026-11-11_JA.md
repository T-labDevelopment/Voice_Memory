# VoiceMemory v1 — 欠落図版の照合と再構成（2026-11-11）

## 確認した事実

2026-10-28作成の旧文書 `manifest_sha256.json` に存在する画像8件は、2026-11-11の作業ブランチのGitHubツリー上に存在しない。ライブラリの個別ファイル検索でも、当該ファイル名と一致する原本は発見できなかった。以前作成したZIPとbundleの元バイト列は、今回の実行環境では取得できないため、ZIP内部の画像ファイル有無は再検査できていない。

**重要：原本PNG/JPEGと同一バイト列を再取得できたとは扱わない。** 新たに生成した4枚のSVGは、すべて「解説図の再構成」であり、元画像と同一とは限らない。

## 補完した図版

| 旧画像名（未回収） | 新規登録した代替図 | 根拠・制約 |
|---|---|---|
| `figures/01_system_block.png` | [01_system_block.svg](figures/01_system_block.svg) | 2026-10-29仕様書2章および現行KiCadの部品・ラベル。概念ブロック図 |
| `figures/02_audio_paths.png` | [02_audio_paths.svg](figures/02_audio_paths.svg) | 同仕様書5-6章、録音ADCとPWM再生経路。部品値は現行レポート参照 |
| `figures/03_relay_ptt.png` | [03_relay_ptt.svg](figures/03_relay_ptt.svg) | 同仕様書7章、K1の保存SCH接点表、U3の後続ECO。実機真理値未検証 |
| `figures/rj45_footprint_layout.png` | [rj45_footprint_layout.svg](figures/rj45_footprint_layout.svg) | 現行KiCadフットプリントのPad座標・NPTH座標を忠実に図示。**ユーザー原寸図そのものではない** |

## 原本回収できず、捏造しなかった画像

| 元ファイル | 状態 | 補助手段 |
|---|---|---|
| `figures/legacy_block_diagram_20261025.png` | 旧説明図の原本未回収 | 現行ブロック再構成図と既存仕様書の説明で代替 |
| `figures/legacy_network_details_20261025.png` | 旧接続詳細図の原本未回収 | 現行KiCad回路図とPTT概念図へのリンクで代替 |
| `sources/RJ45_PCB_LAYOUT_寸法図.png` | ユーザー提供の原図未回収 | 新しいKiCad座標図とフットプリント数値を参照。原図との照合は未完了 |
| `sources/RJ45_部品裏面参考写真.jpeg` | ユーザー提供の実物写真未回収 | 実部品を撮影した写真としての代用品は作成しない。現物でPad1方向を要照合 |

**残る8件すべての旧原本が未回収。** うち4件は同等の説明目的に使う別形式SVGを作成できた。残り4件は新規図版で原本を置き換えると誤認の恐れがあるため、説明資料・最新KiCadへの参照で補足した。

## 実装・安全上の注記

- 旧文書作成時はU2 AT25SF321B／U3 AQV212等の回路世代差が存在したが、現在はW25Q32RVCSJM／TLP592A(F)が後続ECOで採用されている。
- 2026-11-10版はC7/C10/C16/C19の配線・ビア干渉候補が残るレビュー版。正式なKiCad 10 ERC/DRCおよびGND Zone再フィルは未実施。
- 本図版の信号フローは電気接続の厳密な全ネット証明ではない。図から部品やネットを自動生成しないこと。
- 画像リンクはGitHub Markdownのプレビューで使えるSVGに変更した。旧版DOCX/PDFは今回修正していないので、配布時は最新版Markdown資料を優先する。

## Git履歴の状態

通常のGitHubコミット履歴は元のローカルGit履歴ではない。元bundleは `../../../history/VoiceMemory_v1_git.bundle.part01` からpart04として保存されている。実バイト列を再取得できていないため、bundleの結合ハッシュ再検証、旧コミットのGitHub通常履歴としてのpush、タグ復元は未実施（`../../../history/README.md` に手順あり）。

## 出典・参照（このリポジトリ内）

- `VoiceMemory_v1_ファームウェア開発者向けハードウェア仕様書.md`（10月保存SCHとFW向け設計説明）
- `../../../hardware/kicad/voicememory/voicememory.kicad_sch`
- `../../../hardware/kicad/voicememory/Voice_Memory.pretty/RJ45_8P8C_THT_15.91x15.10.kicad_mod`
- `../../../hardware/reports/ECO_2026-10-30_JA.md`
- `../../../hardware/reports/CAP_MIN_0805_2026-11-10_JA.md`
- `manifest_sha256.json`（旧ZIPの元ハッシュ一覧／そのまま保持）
