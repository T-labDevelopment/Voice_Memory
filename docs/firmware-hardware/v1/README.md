# VoiceMemory v1 — ファームウェア開発者向けハード仕様資料

**作成日：2026-10-29／文書版：v1-FW-HW-1.0／図版補足：2026-11-11**

本ディレクトリにある文書の基準は2026-10-29の保存仕様であり、**製造用の最新回路仕様と同義ではありません**。

## 利用順序

1. [図版修復・原本欠落の一覧](FIGURES_RECOVERY_2026-11-11_JA.md) を確認する。
2. [開発者向け仕様書（Markdown版）](VoiceMemory_v1_ファームウェア開発者向けハードウェア仕様書.md) を読む。**図1～4のリンクは実在SVGへ差し替え済み**。
3. 配布・編集用の `VoiceMemory_v1_ファームウェア開発者向けハードウェア仕様書_CID.pdf` と `VoiceMemory_v1_ファームウェア開発者向けハードウェア仕様書.docx` は2026-10-29作成時点の歴史的版であり、今回の図版修復を反映した再出力ではない。
4. [最新KiCadプロジェクト](../../../hardware/kicad/voicememory/) と [2026-11-10コンデンサ監査](../../../hardware/reports/CAP_MIN_0805_2026-11-10_JA.md) を正として照合する。

## 今回GitHubへ追加した再構成図

- [システムブロック図](figures/01_system_block.svg)
- [録音／再生の信号経路](figures/02_audio_paths.svg)
- [リレー接点／自動PTT](figures/03_relay_ptt.svg)
- [RJ45現行KiCadフットプリント座標図](figures/rj45_footprint_layout.svg)

**これらは図の意図を最新資料と保存SCHネット名から再構成した解説図で、旧PNGファイルの原本ではありません。** 回路配線の製造検証・実物の向き確認の代用にはできません。

## 未回収の旧原本

- `figures/legacy_block_diagram_20261025.png`
- `figures/legacy_network_details_20261025.png`
- `sources/RJ45_PCB_LAYOUT_寸法図.png`
- `sources/RJ45_部品裏面参考写真.jpeg`

元の `figures/01_system_block.png`、`figures/02_audio_paths.png`、`figures/03_relay_ptt.png`、`figures/rj45_footprint_layout.png` も**別名のSVGで代替**しただけで、元PNG自体は取得できていません。

`manifest_sha256.json` は元の文書ZIPの期待ハッシュを記録した史料として変更していません。

## その他の仕様と状態

- 現PCBと、2026-09-30保存SCHを用いた当時のピン表 `pinmap_CH32V003F4P6_legacySCH.csv` は完全一致未検証。
- U2、U3、C11/C19、R20等は回路世代差があるので、2026-11-10現行KiCadを優先する。
- キー操作、PTT動作、RTC等はファームウェア側で実装前照合。
- **ERC/DRC、ゾーン再フィル、物理ジャック端子番号の現物照合は未完了。製造可能とは判定しない。**
- [GitHub同期監査記録](../../GITHUB_SYNC_AUDIT_2026-11-11_JA.md) を参照。
