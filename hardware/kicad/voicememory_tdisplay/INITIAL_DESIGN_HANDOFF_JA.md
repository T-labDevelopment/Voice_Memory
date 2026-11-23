# VoiceMemory_TDisplay_ESP32 Rev.A — KiCad 10 初期回路図 一式

2026-11-23／初期案／**未試作・未検証**。既存CH32V003マイコン版とは独立開発。

## 1. データ構成と開き方

このディレクトリをそのまま同一階層に展開する。KiCad 10.xで `VoiceMemory_TDisplay.kicad_pro` を開き、`VoiceMemory_TDisplay.kicad_sch` を回路図エディタで編集する。

```
VoiceMemory_TDisplay.kicad_pro
VoiceMemory_TDisplay.kicad_sch
VoiceMemory_TDisplay.kicad_sym
Voice_Memory.kicad_sym
sym-lib-table
fp-lib-table
VoiceMemory_TDisplay.pretty/
    TTGO-T-Display.kicad_mod
    Relay_Zettler_AZ8462_DIP8.kicad_mod
Voice_Memory.pretty/
    RJ45_8P8C_THT_15.91x15.10.kicad_mod
bom_draft.csv
pinmap.csv
tdisplay_header_pinmap.csv
TFT_DISPLAY_SPEC_JA.md
PROJECT_SCOPE_JA.md
README_JA.md
README.md
INITIAL_DESIGN_HANDOFF_JA.md
```

KiCad標準ライブラリを使用する正式シンボル定義は既存の回路図に埋め込んだ正式データを引き継いでおり、必要な既存カスタムシンボルは`Voice_Memory.kicad_sym`内にある。LILYGO基板を表すカスタムシンボルは`VoiceMemory_TDisplay.kicad_sym`に格納。編集用データであり、図形画像ではない。

PCBはまだ作っていない。KiCadの基板エディタで新規基板を作成する際に、上記2個の追加フットプリントをローカルライブラリから選択できる。

## 2. システム構成

- Classic LILYGO T-Display 1.14インチ ST7789V TFT 240×135＋内蔵ESP32を使用。T-Display S3と混同しない。
- 内蔵TFTに全インジケーターを集約。表示LED・ブザー・外部表示器の追加なし。TFT表示・操作用マイコンファームウェアは未作成。
- マイク側 RJ45（J1）と無線機側 RJ45（J2）を継続採用。
- K1 = Zettler AZ8462-3（3Vコイル／2回路切替、機械式リレー）。Q1ドライバ、D1フライバックダイオード。
- U3 = Toshiba TLP592A(F)（PhotoMOS、自動PTT）。
- U2 = Winbond W25Q32RVCSJM（32Mbit、SPI Flash；4メモリに録音データ保存）。
- U4 = MCP6002（録音用アンプ、再生用バッファ）。
- 追加RECスイッチSW1は現時点の回路では存在（内蔵2ボタンだけでは操作割当未確定）。インジケーター用の部品ではない。
- 電源はT-DisplayのUSB-Cまたは指定1セルLiPo。旧3×単3をLiPo端子へ直接接続しない。

## 3. リレーK1の電気的動作

| モード | GPIO33/RELAY_EN | K1音声 (4 COM) | K1手動PTT (9 COM) | U3自動PTT |
| --- | --- | --- | --- | --- |
| 通常／電源OFF | LOW／コイルOFF | 3 NC：MIC_AUDIO | 10 NC：MIC_PTT | OFF |
| 録音待機／録音中 | HIGH／コイルON | 5 NO：PLAY_OUT | 8 NO：未接続 | OFF |
| 再生準備 | HIGH／コイルON | 5 NO：PLAY_OUT | 8 NO：未接続 | OFF |
| 再生中 | HIGH／コイルON | 5 NO：PLAY_OUT | 8 NO：未接続 | ON |
| 停止／復帰 | LOW／コイルOFF | 3 NC：MIC_AUDIO | 10 NC：MIC_PTT | OFF |

K1コイルは1=+3V3、12=Q1コレクタ。D1はカソード=+3V3、アノード=RELAY_COIL_LOW。GPIO33をR11=820ΩからQ1のベースへ入力し、R12=100kΩでプルダウンする。U3はGPIO26からR13経由でLED駆動する。K1の外部8端子は1/3/4/5/8/9/10/12、未使用8番接点は設計上開放。

**要注意：** 録音中はK1が音声線を無線機から切り離すため、エレクトレットマイクが無線機MIC端子からDCバイアスを受けている場合、録音できない可能性がある。実機・対象マイクのバイアス仕様が確定するまでユニバーサル対応を主張しない。

**送信シーケンス：** 再生開始前に自動PTT OFF→K1 ON→接点安定待ち→U3 ON→DAC再生。停止時はDAC停止→U3 OFF→K1 OFF。録音中にU3をONにしてはいけない。電源断時のリレー復帰とマイク経由の通常PTTはハードウェア側で確保する設計。

## 4. GPIOとフットプリント

- GPIO21=FLASH_MOSI／GPIO22=FLASH_SCK／GPIO17=FLASH_CS／GPIO27=FLASH_MISO
- GPIO32=AUDIO_ADC／GPIO25=AUDIO_DAC
- GPIO33=RELAY_EN／GPIO26=AUTO_PTT_EN／GPIO39=PTT_SENSE_HIGH／GPIO13=SW_REC_N
- TFT専用：GPIO19/18/5/16/23/4。内蔵ボタン：GPIO0/35。
- **重要な訂正：** 初期ドラフトのT-Displayカスタムシンボルの端子番号は基板フットプリントのメーカー表記と逆順だったため、番号を `新番号 = 25 - 旧番号` で対応づけた。GPIOネットと物理端子接続位置は維持し、端子番号だけ正規に合わせた。
- LILYGO公式KiCad `TTGO-T-Display.kicad_mod`（原本をそのまま使用）に対応するパッドの電気名は `tdisplay_header_pinmap.csv` に記載。基板リビジョンごとの現物印字を確認すること。
- K1には旧`Relay_THT:Relay_DPDT_Kemet_EC2_NU`を使用しない。メーカーデータシートの8ホール穴位置に基づくローカル `VoiceMemory_TDisplay:Relay_Zettler_AZ8462_DIP8` を使用する。リレー端子番号と実物方向の最終機械照合は未実施。
- JPG等の見た目だけの図面ではなく回路シンボル・ネット・フットプリント割当の実データが揃っている。

## 5. 検証状況と未解決

| 検証項目 | 状況 |
|---|---|
| 回路図・シンボルライブラリ構文の括弧整合 | 静的チェックPASS |
| グローバルラベル38ネット、全ネット2箇所以上 | 静的チェックPASS |
| ラベル座標の50mil格子 | 静的チェックPASS |
| LILYGO公開KiCadフットプリント24端子への番号対応 | 静的チェックPASS |
| AZ8462用専用フットプリント8パッド番号照合 | 静的チェックPASS |
| KiCad 10 CLIでの正式ERC | **未実施** |
| KiCad 10 GUIでの回路図表示確認 | **未実施** |
| PCB作成、配線、DRC | **未実施** |
| 実機リレー動作、3.3V供給電流／電圧降下、音声録再、マイクバイアス | **未実施** |
| 専用ESP32ファームウェア | **未作成** |

本プロジェクトには独立版の製造承認はない。旧CH32V003版の承認結果は適用しない。

## 6. 参照元

1. LILYGO公式ボード資料： https://wiki.lilygo.cc/products/t-display-series/t-display/
2. LILYGO公式KiCadフットプリント： https://github.com/Xinyuan-LilyGO/TTGO-T-Display/tree/master/kicad/TTGO_T_Display/footprints/TTGO_T_Display.pretty
3. AZ8462メーカー部品仕様： https://akizukidenshi.com/goodsaffix/AZ8462.pdf
4. 既存設計ドキュメント：`PROJECT_SCOPE_JA.md`、`TFT_DISPLAY_SPEC_JA.md`、`README_JA.md`

開発ブランチ：`work/tdisplay-reva-kicad-initial-2026-11-23`
