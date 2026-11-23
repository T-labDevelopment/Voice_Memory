# VoiceMemory T-Display ESP32 Rev.A — ERC U2 フットプリント警告の再修正（2026-11-24）

## 原因と過去の対応が失敗した理由

ユーザー提示のKiCad 10 ERC画面では、エラー0件・警告1件・テストしない項目4件。
警告はU2 `W25Q32RVCSJM` の未解決フットプリント。

失敗した従来の指定：
1. `Package_SO:SOP-8_5.28x5.23mm_P1.27mm`
2. `Package_SO:SOIC-8_5.23x5.23mm_P1.27mm`

両方ともユーザーのKiCad 10 `Package_SO` ライブラリからロードできなかった。
公的に閲覧可能な古いKiCadライブラリ（GitHub mirror / kicad.github.ioは旧版の案内を含む）で「存在する」ことと、手元にインストールされているKiCad 10の標準 `Package_SO` に収録されていることは異なる。

**このため、システム側ライブラリの名前変更で追従する方式を撤回し、実体のあるプロジェクトローカルの完全なフットプリントを使用する。**

## 採用したフットプリント（回路定数・配線は無変更）

```text
VoiceMemory_TDisplay:SOIC-8_5.23x5.23mm_P1.27mm
```

実体：
```text
VoiceMemory_TDisplay.kicad_pro
fp-lib-table
VoiceMemory_TDisplay.pretty/
  SOIC-8_5.23x5.23mm_P1.27mm.kicad_mod
```

`fp-lib-table` には既に、以下のプロジェクトライブラリが登録されている。

```lisp
(lib (name "VoiceMemory_TDisplay") (type "KiCad") (uri "${KIPRJMOD}/VoiceMemory_TDisplay.pretty") (options "") (descr "..."))
```

**標準ライブラリの存在チェックに頼らず**、上記3ファイルと `VoiceMemory_TDisplay.kicad_sch` が同じフォルダーにあれば解決可能な配置。

配布フットプリントのデータは、KiCad公式のGitHub公開フットプリントを**図形・パッド構成を削除せず原文のまま同梱**したもの。これは独自の簡略化シンボルや仮の空フットプリントではない。

- 元の公開データ：
  https://github.com/KiCad/kicad-footprints/blob/master/Package_SO.pretty/SOIC-8_5.23x5.23mm_P1.27mm.kicad_mod
- 出典Blob SHA-1：
  `d1999ca5e8ce259e69e2d75c363f95640f15a802`
- KiCad公式ライブラリの著作権・使用許諾：
  https://www.kicad.org/libraries/license/
- 8パッド（1～8）、1.27mmピッチ、左右X=±3.6mm、パッド寸法1.6×0.6mm（roundrect）。Winbond W25Q32RVCSJMの208mil SOP-8の実装候補。
- KiCad 5系由来の公式 `(module ...)` レガシーフットプリント構文を保持。**KiCad 10 GUIによる読み込み、ライブラリ移行・PCB上の動作検証は未実施。** もし現行環境で構文移行を求められた場合はFootprint Editorで「名前をつけて保存」して最新版形式に変換する。
- 元データの3Dモデル参照はそのまま。存在しない場合はKiCad 10向けの3Dモデルを再設定する。**ERCの未検出警告とは別**の問題。

## 実際に変更したファイル

1. `VoiceMemory_TDisplay.pretty/SOIC-8_5.23x5.23mm_P1.27mm.kicad_mod` — KiCad公式完全フットプリントを追加。
2. `VoiceMemory_TDisplay.kicad_sch` — U2インスタンスと埋め込みシンボル定義（計2箇所）をローカル指定に変更。
3. `Voice_Memory.kicad_sym` — U2標準シンボルのフットプリント指定を一致させた。
4. `bom_draft.csv` — U2フットプリントの指定名を一致させた。

`fp-lib-table` は既存のローカル `VoiceMemory_TDisplay` ライブラリ定義が適切なので**変更不要**。他のコンデンサ、AZ8462-3リレー、GPIO、ネット接続、無線機・マイク対応仕様は変更しない。

## 確認したこと／残る確認

静的照合で確認できること：
- `fp-lib-table` にローカルライブラリ定義が存在。
- 指定先 `.kicad_mod` の実ファイルがGitに存在。
- フットプリント内のパッド番号1～8が一意で全て存在。
- 回路図／シンボルライブラリ／BOMのフットプリント名が一致。
- 既存のネット・部品定数は一切変更していない。

未実施：
- **KiCad 10での実際のライブラリロード・ERC再実行**（本環境にKiCad CLI無し）。
- PCBのフットプリント更新・DRC・現物端子1番・極性と外形照合。
- 無効化されたERC項目4件の内容確認。

## ユーザー環境での確認

1. 新しい作業ブランチのZIPをダウンロードして、**フォルダー構造を保ったまま全ファイルを展開**する。
2. `VoiceMemory_TDisplay.kicad_pro` をプロジェクトとして開く。
3. 回路図U2のプロパティで `VoiceMemory_TDisplay:SOIC-8_5.23x5.23mm_P1.27mm` を確認。
4. **設定 → フットプリントライブラリを管理 → プロジェクト固有ライブラリ**で `VoiceMemory_TDisplay` と `${KIPRJMOD}/VoiceMemory_TDisplay.pretty` を確認。
5. フットプリント選択画面から `VoiceMemory_TDisplay` ライブラリを開き、SOIC-8の8個のランドが表示されるか確認。
6. ERCを再実行する。U2の警告が消えた場合でも、残る警告・除外項目は別途確認。

## 最終判定

フットプリント解決先の実ファイルまで同梱した初期修正版は完成。ただし**ユーザーのKiCad 10でERC警告0件になったことは未確認**。
