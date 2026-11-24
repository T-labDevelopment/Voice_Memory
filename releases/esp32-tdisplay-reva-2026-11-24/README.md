# VoiceMemory T-Display ESP32 Rev.A — 製造基準登録記録（2026-11-24）

## 承認・履歴

- 主開発対象：**ESP32 T-Display版ボイスメモリー（Rev.A）**。旧CH32V003 v1/v2は比較・履歴用として継続保存。
- ユーザーは2026-11-24、回路・PCB設計検証を完了し、本データを基準にPCB製造および実機試作へ進む旨を明示。
- 原本：`VoiceMemory_TDisplay-2026-11-24_161139.zip`。
- 原本SHA-256：`bd1351872f4d337664d0818d76dbb4c1e1650072b96063b2279d5c885837d033`。
- 編集可能な回路図・基板データ：[KiCad Rev.A ディレクトリ](../../hardware/kicad/voicememory_tdisplay/revA_manufacturing_2026-11-24/)。
- 原本ZIP保存：[source archives](../../hardware/source-archives/tdisplay-reva-2026-11-24/VoiceMemory_TDisplay-2026-11-24_161139.zip)。

## ユーザー実行の検査報告書

- `ERC_2026-11-24_161128.rpt`：ERCエラー0、警告0。
- `DRC_2026-11-24_161113.rpt`：DRC違反0、未接続0、フットプリントエラー0。
- KiCad 10.xの再実行は本登録作業では行っていません。
- ERC除外：「Global label only appears once」「Four connection points are joined together」「SPICE model issue」「Assigned footprint doesn't match footprint filters」。
- DRC除外：「Footprint has no courtyard defined」「Track endpoint not centered on via」「Tuning profile track geometries」「Footprint doesn't match symbol's footprint filters」「Footprint component type doesn't match footprint pads」。

## 主な設計要件

- Classic ESP32 T-Display 16MB版、内蔵LCD、USB-C給電＋単セルLi-ion系（T-Display搭載充電回路）。
- 外付けW25Q32RVCSJM不採用。録音データをT-Displayの16MiB Flashへ格納する方針。ファームウェアのパーティション分割は別途必要。
- 12mm角タクト6個：REC(GPIO13)、CH1(GPIO21)、CH2(GPIO22)、CH3(GPIO17)、CH4(GPIO27)、Wake/Sleep(GPIO36)。
- USB接続判定GPIO38（分圧回路）。USB接続中の自動スリープを無効化。電池運用は無操作時Deep Sleep（初期タイムアウト案5分）。
- 録音・再生・自動PTT、録音中の誤送信防止は実機検証対象。

## 未確認（PCB承認とは別）

- TENSTAR版T-Displayのピン配置・Flash容量・充電回路とUSB給電検出を実機で確認する。
- 自動Deep Sleep、外部ボタンによる起床・長押しの動作と待機電流を評価する。
- 録音・再生品質、リレー・PhotoMOS、マイクPTT入出力と無線機適合を確認する。

**設計凍結：** ユーザーが変更を指示するまでは、承認済みKiCad回路・PCBに手を加えず、試作検証結果は別の変更記録へ追加する。
