# ESP32 T-Display Rev.A — Prototype発注基準（2026-11-24）

**状態：ユーザーによる基板発注済み申告。設計の現物試験・量産承認を示すものではない。**

## 主開発対象

VoiceMemoryの今後の主開発対象は、**ESP32 / T-Display（16MB Flash）仕様**とする。旧CH32V003版と旧v1/v2の資産を削除・上書きせず、履歴と比較対象として保持する。新規ファームウェア・実機試験・後続RevはこのPrototype基準を起点に管理する。

## 発注した資料と同一性

| 資料 | ファイル | SHA-256 |
|---|---|---|
| 今回のKiCad設計正本 | `VoiceMemory_TDisplay-2026-11-24_164508.zip` | `f81d32c1ff5159133aed2fd2ecadfa6d76ce97ed69fa2263f3d4d98e78146a19` |
| 発注に使用したGerber + Drill | `PCB.zip` | `687c858ae40807e0d26217c01bddc3cf3bbf9370301716aae13c61c121ad7811` |
| 発注前の比較基準 | `VoiceMemory_TDisplay-2026-11-24_161139.zip` | `bd1351872f4d337664d0818d76dbb4c1e1650072b96063b2279d5c885837d033` |

- [今回のKiCad原本](../../hardware/source-archives/tdisplay-prototype-ordered-2026-11-24/VoiceMemory_TDisplay-2026-11-24_164508.zip)
- [Gerber・ドリル一式](../../hardware/source-archives/tdisplay-prototype-ordered-2026-11-24/PCB.zip)
- [編集可能な展開KiCadデータ](../../hardware/kicad/voicememory_tdisplay/prototype_ordered_2026-11-24/)
- SHAと元ZIP内ファイルの照合情報は `SOURCE_MANIFEST_SHA256.json` に記録。

## 前版からの変更（PCBだけ）

- R27を Y=100.330mm から Y=98.806mmへ移動（X=90.805mmは維持）。
- `+3V3`・`SW_WAKE_N` の銅箔配線を引き直し、配線本数489→490、ビア101本維持。
- 表面シルクへ `VoiceMemoryUNIT / Prototype / Vir0.5β / T-Lab/JG1KGX / 2026/11/24` を追加。
- 裏面シルクへ `PTTGND/AUDIOGND 分離用` の注記を追加。
- 部品値・参照番号のシルク表示の微調整、およびゾーン再フィル。
- フットプリント52個、回路図、シンボル・フットプリント定義に変更なし。
- `.kicad_prl` は個人用設定であり、Git管理版へは採用しない（原本ZIPに保存）。

## Gerberジョブ情報（発注ファイルから直接取得）

- 生成：KiCad Pcbnew **10.0.6**、2026-11-24 16:46:23 +09:00。
- 構造：2層、FR4、板厚 **1.6mm**、銅厚 35µm（ジョブ記載）。
- 基板外形：ジョブ記載 X=64.45mm、Y=104.35mm（外形線幅を含む）。
- 銅箔、マスク、シルク、ペースト、外形、PTH/NPTHドリルのファイルを同梱。
- ジョブに記された最小設計ルールはトラック幅/間隔 **0.2mm**。
- GerberとPCBの完全な再生成一致検査は未実施。今回ユーザーが発注に使用したファイルを**そのまま保存**する。

## 検証ステータス

- 前版16:11のERC 0・DRC 0は、ユーザー提出の検査レポートで確認済み（検査除外設定あり）。
- 今回16:45の手直し後は新しいERC/DRCレポート未提出のため、**今回版のERC/DRC 0とは記載しない**。
- 回路図・部品ピン・フットプリント定義は前版とbyte一致。PCBの修正位置は座標・配線データから抽出。
- 基板の発注/製造開始と、実機機能検証（録再、PTT、Deep Sleep等）の完了は区別する。

## 凍結方針

このPrototype発注版は変更・上書きしない。以降の修正は新しいブランチ・コミットへ追加する。main統合は別途許可時のみ行う。
