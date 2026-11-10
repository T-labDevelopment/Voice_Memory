# VoiceMemory v1 最新データ受領記録

2026-10-29にユーザーがアップロードした `voicememory-2026-10-05_162836(2).zip` を現時点の**最新受領KiCad実ファイル**として指定。

- **原本のZIPは無変更でGitに保存**: `hardware/source-archives/voicememory-2026-10-05_162836(2).zip`
- **展開したKiCadプロジェクト**: `hardware/kicad/voicememory/`
- **SHA-256**: `b34d0f4ad92e3c439bdc9cf07ba6ea58b797cbf73fb96d74d4353c6b7bf29787`
- **構成**: `.kicad_sch` `.kicad_pcb` `.kicad_pro`、カスタムシンボル/フットプリント、ライブラリテーブル、操作環境依存の `.kicad_prl`（原本ZIP内のみ保管）
- **Gitタグ**: `v1-data-2026-10-29`。既存 `v1` タグは移動させない。

### 取り扱いルール

今後回路設計やファームウェア資料を確認する際は、この保存スナップショットを実データの出発点とする。ただし設計上の決定とファイル未反映変更は区別する。違いの詳細は `hardware/kicad/voicememory/README_JA.md` および `hardware/reports/inspection_2026-10-29.json` を参照する。

本作業では回路図・PCBへの変更、ERC、DRC、実測を実施していない。
