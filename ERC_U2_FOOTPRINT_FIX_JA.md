# U2（W25Q32RVCSJM）のERCフットプリント未検出警告 — 修正記録

- 記録日: 2026-11-24
- 対象: VoiceMemory_TDisplay_ESP32 Rev.A（CH32V003版には適用しない）
- 根拠: ユーザー提示のKiCad ERC画面。エラー0件、警告1件、テストしない項目4件
- 作業ブランチ: `work/tdisplay-reva-u2-footprint-erc-2026-11-24`
- **修正は適用済み、KiCad 10でのERC再実行は未実施**

## 原因

U2のフットプリント欄に指定されていた

```
Package_SO:SOP-8_5.28x5.23mm_P1.27mm
```

は正式なKiCad `Package_SO`フットプリント名ではなく、KiCad ERCが「フットプリントをライブラリに見つけられない」と警告していた。

Winbond公式型番 `W25Q32RVCSJM` はSOP-8、208milを指定する。Winbond W25Q32RV Revision B (2024-01-29)の8-pin SOIC 208-mil（SS）は、ボディ寸法名目 D=5.28mm/D1=5.23mm、E=5.28mm/E1=5.23mm、ピンピッチ1.27mm、外脚間幅H=7.90mm。KiCad標準 `Package_SO` にはWinbond W25Q32JVに基づく以下の8ピンフットプリントが存在する。

```
Package_SO:SOIC-8_5.23x5.23mm_P1.27mm
```

この標準フットプリントはW25Q系の208milパッケージに適合する設計候補であり、今までの実在しないカスタム表記に代えて採用する。

## 変更したデータ

| ファイル | 内容 |
|---|---|
| `VoiceMemory_TDisplay.kicad_sch` | U2のシンボルインスタンスと回路図内埋め込みシンボル定義の2箇所を新しい名前へ置換 |
| `Voice_Memory.kicad_sym` | W25Q32RVCSJMシンボルの既定Footprintを同じ名前へ修正 |
| `bom_draft.csv` | U2のFootprint列を新しい名前へ修正 |

U2の型番・SPI配線・端子番号・他部品値・TFT・リレー回路は変更していない。

## 判定と未実施

- 標準フットプリント名がKiCad公開 `Package_SO`一覧に存在：**確認済**
- パッケージ分類（208mil SOP-8）、ボディ寸法、8ピン1.27mmピッチ：**Winbondメーカー資料から確認済**
- ファイル内の旧フットプリント参照：**更新済**
- 対象3ファイルの参照名一致：**静的照合済**
- KiCad 10の `ERC` で警告0件になること：**まだ実行しておらず未検証**
- KiCad 10での基板パッド・3D外形・実装クリアランスの実機比較：**未実施**
- 現在の「テストしない項目（4）」はERCルール設定で意図的にチェック対象外となる4分類であり、修正された警告1件の内訳には含めない。内容を確認したうえで検査対象へ戻すか判断する。

## 端末上の再確認手順

1. このブランチのデータをZIPで取得し、展開する。
2. KiCad 10の `VoiceMemory_TDisplay.kicad_pro` を開く。
3. 回路図でU2のシンボルプロパティを開き、`Package_SO:SOIC-8_5.23x5.23mm_P1.27mm` と表示されることを確認。
4. ERCを再実行し、「フットプリントが見つからない」警告が解消することを確認。残る違反があれば別途対応。
5. PCB設計開始前にU2のパッド番号と位置、Pin1マーク、実際に調達した`W25Q32RVCSJM`の外形（208mil）を比較。

## 出典

- Winbond製品情報（`W25Q32RVCSJM`, SOP-8, 208mil）: https://www.winbond.com/hq/product/code-storage-flash/qspi-nor/w25q-rv/?__locale=en&partNo=W25Q32RVCSJM
- Winbond W25Q32RVデータシート Rev.B（2024-01-29、Section 10.2 p.76）: https://resources.ampheo.com/static/datasheets/winbond-electronics-corporation/w25q32rvsnjq.pdf
- KiCad公開標準フットプリント `Package_SO` 一覧: https://kicad.github.io/footprints/Package_SO.html
