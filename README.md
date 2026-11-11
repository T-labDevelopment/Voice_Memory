> **v2正本更新（2026-11-11 16:44 JST）**：アップロードされた `voicememory-2026-11-11_164201.zip` を現在のv2基準とした。元ZIPは [無変更原本](hardware/source-archives/v2-baseline/voicememory-2026-11-11_164201.zip)、採用状況と検証証跡は [受領記録](hardware/reports/V2_BASELINE_RECEIPT_2026-11-11_JA.md)。**ERC/DRCはユーザー側で実施済みとの申告。ChatGPTによる再実行や結果0件の確認は未実施。** 以前の11月10日干渉報告は旧PCBの履歴情報。

# Voice_Memory — バージョン別設計資料

**現在の開発対象：v2（2026-11-10基準のKiCad 10レビュー版）**

プロジェクトの設計データは**v1試作版**と**v2現行開発版**に分けて管理します。旧v1を現在の設計に上書きせず、製造検証のために独立参照します。

| 版 | 目的・状態 | 参照先 |
|---|---|---|
| **v1** | **試作・製造検証用の旧基準版**。2026-10-30リリースZIP。**費用計算不要**。未製造承認 | **[v1試作・製造検証資料](releases/v1-prototype/README.md)** |
| **v2** | **現在の開発・回路修正・検証対象**。11月10日コンデンサECOを含む。未製造承認 | **[v2開発・技術仕様](development/v2/README.md)** |
| v2費用 | v2の開発・試作費と必要条件。未確定額を分離 | [v2費用・必要仕様](development/v2/DEVELOPMENT_AND_COST_SCOPE_JA.md) |

## 設計データを開く場合

- **現行v2の回路図・PCB：** [`hardware/kicad/voicememory/`](hardware/kicad/voicememory/)
- **現行v2の技術監査：** [11月10日コンデンサ・フットプリント監査](hardware/reports/CAP_MIN_0805_2026-11-10_JA.md)
- **旧v1原本の照合記録：** [10月30日ZIPとのハッシュ比較](hardware/reports/ECO_ZIP_RECEIPT_COMPARE_2026-11-11_JA.md)
- **FW開発資料：** [旧版仕様書と更新補足](docs/firmware-hardware/v1/README.md)。旧版資料には世代差があり、v2の実装時は回路図を優先する。
- **履歴バックアップ：** [`history/`](history/README.md)

> **注意：** v1の原本ZIP `VoiceMemory_v1_ECO_2026-10-30_KiCad10(1).zip` 自体はまだGitHub上へ同一バイナリとして保存されていません。原本のSHAと内容はv1索引に記録済み。GitHubの現行 `.kicad_sch`・`.kicad_pcb` は**v2の改修データ**なので、v1原本として流用しないでください。

## Gitの取り扱い

- 開発ブランチ：`develop/v2`。このブランチの `version.json` は `v2`。
- 従来の `fix/v1-cap-min0805-2026-11-10` は変更履歴として残す。過去コミット、bundle、既存タグの書換えはしない。
- `main` は未統合。統合は明示的な指示後に行う。
- **KiCad 10 ERC/DRC、GNDゾーン再フィル、実機検証は未完了。Gerber出力や製造適合の判定は保留。**
