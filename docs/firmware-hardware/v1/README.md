# VoiceMemory v1 — ファームウェア開発者向けハード仕様資料

**作成日：2026-10-29／文書版：v1-FW-HW-1.0**

> **2026-11-11追記**：本資料は作成当時のv1参照仕様であり、最新の2026-11-10レビュー用KiCadデータにすべて追従したものではありません。最新の部品変更・設計未解決事項は `../../../hardware/reports/CAP_MIN_0805_2026-11-10_JA.md`、回路・PCBの実ファイルは `../../../hardware/kicad/voicememory/` を優先してください。GitHubでの取込・欠落ファイル・元のGit履歴に関する状況は `../../GITHUB_SYNC_AUDIT_2026-11-11_JA.md` に記録しました。

## 最初に読むファイル

- `VoiceMemory_v1_ファームウェア開発者向けハードウェア仕様書_CID.pdf`：日本語CIDフォントを使用した配布用PDF。
- `VoiceMemory_v1_ファームウェア開発者向けハードウェア仕様書.docx`：編集できるWord版。
- `VoiceMemory_v1_ファームウェア開発者向けハードウェア仕様書.md`：Git差分管理用テキスト版。

## 作成時の添付資料一覧（旧ZIPの記録）

以下の `figures/` の画像6件は、**2026-11-11時点のGitHubブランチに独立ファイルとして格納されていません**。現行ツリーに存在するものとして参照しないでください。

- `figures/01_system_block.png`：回路ブロック／制御・信号経路。
- `figures/02_audio_paths.png`：録音ADC／再生PWM経路。
- `figures/03_relay_ptt.png`：K1の接点、PhotoMOS、PTT制御。
- `figures/legacy_block_diagram_20261025.png`：先行回路説明図（9月保存SCH参照）。
- `figures/legacy_network_details_20261025.png`：先行端子・ネット接続詳細図。
- `figures/rj45_footprint_layout.png`：RJ45修正フットプリント図。

確認済みの格納物・注意事項：

- `Voice_Memory.pretty/RJ45_8P8C_THT_15.91x15.10.kicad_mod`：当時の修正フットプリント。**最新のKiCadプロジェクト内蔵版を優先**。
- `sources/`：`KICAD_APPLICATION_STATUS_JA.md` および `V1_BASELINE_JA.md` が存在する。旧ZIPで列挙したRJ45寸法図PNGと部品写真JPEGは現行GitHubブランチで**未収録**。
- `pinmap_CH32V003F4P6_legacySCH.csv`：旧SCHネット名を抽出した20ピン表。**現PCBとは未照合**。
- `manifest_sha256.json`：旧ZIPで意図したファイル一覧とチェックサム。**現在のGitHubツリーと一致しない項目がある**。

## 重要な制約

作成当時の文書ZIPには、2026-10-05基準のKiCad正本 `.kicad_sch` / `.kicad_pcb` / 全ライブラリが含まれていませんでした。その後、ユーザー提供KiCadデータが別途受領・GitHubブランチへ格納され、現在は `../../../hardware/kicad/voicememory/` に存在します。ただし正式ERC/DRCおよび実機検証は未実施です。

特にU2（AT25SF321B／W25Q32RV）、U3（AQV212／TLP592A）、U4（NJM2732D／MCP6002）、R20値、C2・C4・C18等の回路世代差は本文書で明記しています。ファームウェア確定実装前に、最新KiCadと現物を照合してください。

## バージョンとGit

- ハードウェア基準タグ `v1` は当時の参照仕様記録。元のローカル履歴は `history/` のGit bundle分割ファイルとして保存しています。
- この文書を含む設計のGitHubスナップショットは `fix/v1-cap-min0805-2026-11-10` に登録済みです。
- 元のローカルGit履歴のコミットSHAとタグがGitHubの通常の履歴へすべて移植されたわけではありません。
- `main` への統合は未実施。設計の製造可能性を保証しません。
