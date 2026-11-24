# Voice_Memory — 現行主開発：ESP32 T-Display Rev.A

> **2026-11-24以降の主開発対象は `VoiceMemory_TDisplay_ESP32 Rev.A` です。**
> 旧CH32V003 / v1 / v2 は履歴・比較・保守用として保持します。旧v2の製造承認をESP32版へ流用するものではありません。

## 現行の開発・製造基準

| 区分 | 現在の扱い | 参照 |
|---|---|---|
| **ESP32 / T-Display Rev.A** | **主開発・基板製造／試作基準（2026-11-24ユーザー確認）** | [ESP32版の製造基準](releases/esp32-tdisplay-reva-2026-11-24/README.md) |
| 旧CH32V003 v2 | 旧系統、過去の製造承認データを保存 | [v2記録](releases/v2-manufacturing-approved-2026-11-11/README.md) |
| 旧v1 | 旧試作・資料 | [v1記録](releases/v1-prototype/README.md) |

ESP32版の**最新の編集可能なKiCad回路図・基板・ローカルライブラリ**は
[`hardware/kicad/voicememory_tdisplay/revA_manufacturing_2026-11-24/`](hardware/kicad/voicememory_tdisplay/revA_manufacturing_2026-11-24/) にあります。
以前の `hardware/kicad/voicememory_tdisplay/*.kicad_sch` と古いREADMEは**旧ドラフト**であり、製造基準ではありません。

- **承認済み受領原本ZIP**：[`VoiceMemory_TDisplay-2026-11-24_161139.zip`](hardware/source-archives/tdisplay-reva-2026-11-24/VoiceMemory_TDisplay-2026-11-24_161139.zip)
- **原本SHA-256**：`bd1351872f4d337664d0818d76dbb4c1e1650072b96063b2279d5c885837d033`
- **受領検証報告**：[ERC](releases/esp32-tdisplay-reva-2026-11-24/ERC_2026-11-24_161128.rpt) / [DRC](releases/esp32-tdisplay-reva-2026-11-24/DRC_2026-11-24_161113.rpt)
- **ERC**：ユーザー実行結果エラー0件・警告0件。**DRC**：ユーザー実行結果違反0件・未接続0件・フットプリントエラー0件。除外された検査項目は報告書参照。こちらではKiCad 10の再実行は未実施。
- **実機の録音再生・充電・Deep Sleep・USB検出は未試験**。製造承認と実機動作保証を混同しないこと。

## ESP32仕様（現行）

- 16MiB Flash搭載のESP32 classic T-Display（候補：TENSTAR 16MB版）。LCDはT-Display内蔵表示器。
- W25Q32RVCSJM外付けFlashは**不採用**。録音はT-Displayのフラッシュへ保存する設計（領域定義はファームウェアで確定）。
- CH1～CH4、録音用REC、起床／手動Deep Sleep用SW6の**12mm角タクトスイッチ6個**。
- REC GPIO13、CH1 GPIO21、CH2 GPIO22、CH3 GPIO17、CH4 GPIO27、SW6起床 GPIO36、USB給電検出 GPIO38（暫定実機確認事項）。
- USB-Cまたは1セルLi-ion/LiPo電池で給電。USB給電中は自動Deep Sleepを無効化、電池運用中は一定時間無操作で移行。Deep Sleepは電池の物理遮断ではありません。
- PTTの安全制御（機械リレー／PhotoMOS）・音声入出力・4ch録音再生は試作検証対象。

## Git運用

- ESP32系とCH32V003系は同じリポジトリに明確なディレクトリ・履歴区分を設けて管理します。
- ESP32 Rev.A製造基準の変更は、元ZIPのハッシュと差分が追跡できる別コミットで管理します。
- 旧v2の基準ファイルと製造記録は変更せず維持します。
- 作業ブランチで検証してから、**ユーザーの許可がある場合にのみ `main` に統合**します。
