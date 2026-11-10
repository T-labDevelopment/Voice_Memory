# VoiceMemory v1 — KiCad基準データとファームウェア仕様資料

**最新受領KiCadデータ: 2026-10-29**

- `hardware/kicad/voicememory/`: 今回ユーザーから受領したKiCad 10プロジェクト（回路図・PCB・ライブラリ）。
- `hardware/source-archives/voicememory-2026-10-05_162836(2).zip`: ユーザー提供の元ZIP。元データをそのまま保存。
- `hardware/kicad/voicememory/README_JA.md`: 実データと過去の設計指示との差分・注意事項。
- `hardware/reports/RECEIPT_2026-10-29_JA.md`: 受領記録とチェックサム。
- `docs/firmware-hardware/v1/`: 旧資料によるファームウェア開発者向け仕様書。最新KiCadと差分があるため再照合必須。
- `Voice_Memory.pretty/`: **旧参照用**のRJ45フットプリント。最新受領プロジェクトを開く際は `hardware/kicad/voicememory/Voice_Memory.pretty/` を使用する。

`v1` は過去の部分的な参照仕様のGitタグ。`v1-data-2026-10-29` が最新受領された**実KiCadデータを含む**記録タグ。既存タグは書き換えない。

**ERC/DRC未実施。実基板の製造適合・実機動作を保証しない。**

## 2026-11-11 図版の追加補完

旧ファームウェア仕様書でリンク切れになっていた主要な4図について、KiCadと仕様書を基に説明用SVG図を追加した。**旧PNGやRJ45現物写真の原本を復元したものではない。** 補完・未回収画像の一覧は [FIGURES_RECOVERY_2026-11-11_JA.md](docs/firmware-hardware/v1/FIGURES_RECOVERY_2026-11-11_JA.md) を参照。仕様書のMarkdown版の図リンクは更新済み、歴史的版PDF/DOCXは未再出力。

## 旧v1リリース版の区分（2026-11-11確定）

ユーザー指定により `VoiceMemory_v1_ECO_2026-10-30_KiCad10(1).zip` は**旧v1のリリース版**とする。現行の2026-11-10コンデンサ見直し版とは別基準として保存し、旧版を現行設計へ上書きしない。旧版の同定・SHA-256・登録状況は [旧v1リリース版の保存基準](releases/legacy-v1-2026-10-30/README.md) を参照。元ZIPのGitHub登録は未完了。製造適合は未検証。
