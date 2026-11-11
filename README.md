# Voice_Memory — v1試作資料とv2製造承認基準

**現在の製造・開発基準：v2（2026-11-11製造承認済み）**

| 版 | 位置付け | 参照 |
|---|---|---|
| **v1** | 旧試作・製造検証用の資料。費用計算は行わない | [v1専用ページ](releases/v1-prototype/README.md) |
| **v2** | **製造承認済み（ユーザー承認・2026-11-11）** | [v2製造承認記録](releases/v2-manufacturing-approved-2026-11-11/README.md) |
| v2技術 | 現行の回路・PCB・開発仕様 | [v2仕様書](development/v2/README.md) |
| v2費用 | v2のみ費用を管理。総額は未見積 | [開発費・必要仕様](development/v2/DEVELOPMENT_AND_COST_SCOPE_JA.md) |

## 製造データ

- **承認原本ZIP：** [`voicememory-2026-11-11_164201.zip`](hardware/source-archives/v2-baseline/voicememory-2026-11-11_164201.zip)
- **承認原本SHA-256：** `a64d1d4d439a141a7048c7fe233227507cebeaa69209cd91ddddc90118438c7a`
- **KiCad 10設計ファイル：** [`hardware/kicad/voicememory/`](hardware/kicad/voicememory/)
- **受領・検証証拠：** [v2基準ZIPの照合記録](hardware/reports/V2_BASELINE_RECEIPT_2026-11-11_JA.md)
- **製造承認：** プロジェクト責任者（ユーザー）の明示指示により承認済み。
- **ERC／DRC：** ユーザー側で実施済みと申告。正式検証レポート未収録、独立再実行は未実施であり、エラー0／警告0という個別結果の確認は未完了。

2026-11-10以前のECOレポートは過去のPCBに関する**履歴資料**であり、現行製造承認版に対する未解決不良の判定には使用しない。

## Git運用

- 現行開発ブランチ：`develop/v2`。
- [v2製造承認データ](releases/v2-manufacturing-approved-2026-11-11/README.md)は固定ZIPのハッシュで同定。設計変更は別コミットで扱う。
- `main` 統合、旧v1タグ改変、過去コミットの書換えは実施していない。
- [旧v1原本の受領・比較記録](hardware/reports/ECO_ZIP_RECEIPT_COMPARE_2026-11-11_JA.md)と[履歴バックアップ](history/README.md)は保管を維持する。
