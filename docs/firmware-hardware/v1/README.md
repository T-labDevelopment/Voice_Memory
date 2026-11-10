# VoiceMemory v1 — ファームウェア開発者向けハード仕様資料

**作成日：2026-10-29／文書版：v1-FW-HW-1.0**

## 最初に読むファイル

- `VoiceMemory_v1_ファームウェア開発者向けハードウェア仕様書_CID.pdf`：日本語CIDフォントを使用した配布用PDF。
- `VoiceMemory_v1_ファームウェア開発者向けハードウェア仕様書.docx`：編集できるWord版。
- `VoiceMemory_v1_ファームウェア開発者向けハードウェア仕様書.md`：Git差分管理用テキスト版。

## 添付資料

- `figures/01_system_block.png`：回路ブロック／制御・信号経路。
- `figures/02_audio_paths.png`：録音ADC／再生PWM経路。
- `figures/03_relay_ptt.png`：K1の接点、PhotoMOS、PTT制御。
- `figures/legacy_block_diagram_20261025.png`：先行回路説明図（9月保存SCH参照）。
- `figures/legacy_network_details_20261025.png`：先行端子・ネット接続詳細図。
- `figures/rj45_footprint_layout.png`：RJ45修正フットプリント図。
- `Voice_Memory.pretty/RJ45_8P8C_THT_15.91x15.10.kicad_mod`：修正済みKiCadフットプリント（v1設計方針、基板未反映）。
- `sources/`：v1参照仕様、KiCad反映状況、ユーザー提供RJ45寸法図・部品写真。
- `pinmap_CH32V003F4P6_legacySCH.csv`：保存SCHネット名を抽出した20ピン表。**v1現PCBとは未照合**。

## 重要な制約

本ZIPに **2026-10-05基準のKiCad正本 `.kicad_sch` / `.kicad_pcb` / 全ライブラリは含まれません**。これらは本作業環境で取得できず、正確な製造用回路図・ERC/DRC結果を再出力したものではありません。

特にU2（AT25SF321B／W25Q32RV）、U3（AQV212／TLP592A）、U4（NJM2732D／MCP6002）、R20値、C2・C4・C18等の回路世代差は本書で明記しています。ファームウェアの確定実装前に現物と正本との照合が必要です。

## バージョンとGit

- ハードウェア基準タグ `v1` は既存のまま保持。
- 本文書はv1基準に対する説明資料であり、**タグ `v1` の実体を変更しません**。
- ローカルGitに追加履歴を作成できますが、GitHub等のリモートへの反映は別途必要です。
