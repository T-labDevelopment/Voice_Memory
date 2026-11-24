# ESP32 T-Display Rev.A — 2026-11-24 製造・試作基準

**主開発対象（ESP32仕様）**。このディレクトリのKiCadデータは、ユーザーが2026-11-24 16:11に検証した版から編集用ソースを抽出したものです。

- 原本ZIP：`VoiceMemory_TDisplay-2026-11-24_161139.zip`
- ZIP SHA-256：`bd1351872f4d337664d0818d76dbb4c1e1650072b96063b2279d5c885837d033`
- KiCad 10.x 編集可能：`.kicad_pro`、`.kicad_sch`、`.kicad_pcb`、`.kicad_sym`、`.pretty/*.kicad_mod`、ライブラリテーブル。
- ERC：ユーザー実行の報告書でエラー0・警告0、DRC：違反0・未接続0・フットプリントエラー0。**こちらでは再実行していません**。
- 元ZIPに含まれるローカル個人設定 `.kicad_prl` はGit管理から除外しました。元ZIPに含まれる旧版の静的検査記録（過去ドラフト）は最新承認状況と異なるため、この編集用フォルダにはコピーしていません。原本ZIPは無加工で別途保存しています。
- 外付けW25Q32RVCSJMなし、タクトスイッチ6個、T-Display側USB-C充電対応の1セル電池入力を予定。
- Deep SleepとUSB検出はファームウェア・実機試験で検証が必要です。T-Display 16MB版のピン互換性と実機Flash容量も未試験です。
- **回路図・PCBはユーザー承認の製造基準。以後は無指示で既存設計を変更しない。**

詳細は [`releases/esp32-tdisplay-reva-2026-11-24/README.md`](../../../../releases/esp32-tdisplay-reva-2026-11-24/README.md) に記載します。
