# VoiceMemory_TDisplay_ESP32 Rev.A｜LILYGO T-Display簡易回路設計

> **プロジェクト区分（確定）**：本回路は既存のCH32V003試作版とは別製品・別ファームウェアとして管理する **VoiceMemory_TDisplay_ESP32 Rev.A** の設計ドラフトです。AZ8462-3機械式リレーを維持し、PhotoMOS置換案は標準に採用しません。詳細は [PROJECT_SCOPE_JA.md](PROJECT_SCOPE_JA.md) を参照してください。既存v1/v2の検証・製造承認を本製品へ流用しません。現在はGitHubリポジトリ内の専用ブランチによる暫定分離であり、専用リポジトリの作成・移行は未実施です。

**設計日：2026-11-22／状態：回路図ドラフト・実機未検証・PCB未作成**

この資料は、製造承認済み VoiceMemory v2（`develop/v2`、基準コミット `d69a0664f0994633a5732053ea11fa3172edfa56`）の機能仕様をT-Display版へ移植するための新規回路設計である。v2の承認データ、BOM、ソースZIPは変更していない。新しい回路の承認やERC/DRC合格を意味しない。

## 1. 基本方針

- 4チャンネルM1～M4、録音最大120秒、8kHz/8bit/モノラル、ループ再生、自動PTT、手動PTT優先を維持する。
- マイク・無線機は旧仕様のRJ45 8P8C×2（J1/J2）を維持する。メーカー別ピン割当は外付け変換ケーブルで対応する。
- 制御部は **初代／Classic LILYGO T-Display、ESP32、1.14インチST7789**。T-Display S3とは端子構成が異なるので混用しない。
- 旧CH32V003と専用書込みヘッダ、独立表示LEDを廃止。T-Display標準のUSB-C、液晶と2つのボタンを利用する。
- 音声再生はESP32内蔵8bit DAC（GPIO25）で生成し、旧PWM出力フィルタを簡略化する。録音はADC1 GPIO32、前段はMCP6002。
- 記録容量は外付けW25Q32RVCSJM（32Mbit/4MiB）を維持。T-Display上の4MiBプログラムFlashを4メモリ分の録音領域として共用する設計にはしない。
- K1=AZ8462-3（3Vコイル、2回路c接点）、U3=TLP592A（自動PTT）の誤送信防止構成は維持。電源はT-DisplayのUSB-Cまたはメーカー仕様に沿った1セルLiPo、外付け回路は3.3V給電。旧単3×3本をLiPo端子に直結しない。

## 2. 信号の流れ

```text
J1 マイク ──────┬─→ K1 NC ──────────→ J2 無線機マイク入力
                 │
                 └─→ 録音アンプU4A → ESP32 GPIO32(ADC)
                                               │ SPI
                                         W25Q32RVCSJM
                                               │
J2 無線機マイク入力 ← K1 NO ← 出力音量 ← U4B/RC ← GPIO25(DAC)

J1 マイクPTT ─────→ K1 NC ─→ J2 無線機PTT
       │
       └─→ Q2絶縁レベル検出 → GPIO39（HIGH=PTT押下）

GPIO33 ─→ Q1 ─→ K1コイル（録音待機／録音／再生中は切替）
GPIO26 ─→ R13 ─→ TLP592A入力LED → その出力接点でRIG_PTT/PTT_GNDを短絡
```

**通常時：** K1は非励磁（NC）で、マイク音声とマイクPTTがJ1からJ2へ通過する。起動直後、異常時、停止時に自動PTT出力はOFF。

**録音操作：** REC操作で録音待機へ入り、まずK1を励磁してJ1側マイクPTTをJ2から切り離す。TLP592AはOFF。マイクPTT押下中だけADCを記録し、PTT解放で録音確定。RECボタンの操作法はファームウェアで実装する。

**再生操作：** K1を励磁し、GPIO25の音声をJ2へ注入。TLP592Aは再生中だけON。ループ間には必ずPTT OFFの休止区間を入れる。手動マイクPTTが押された場合は自動再生を中断し、PTTは手動優先とする。

## 3. ESP32端子割当（Classic T-Display）

| GPIO | ネット名 | 接続先 |
|---:|---|---|
| 21 | `FLASH_MOSI` | Flash U2-5 |
| 22 | `FLASH_SCK` | Flash U2-6 |
| 17 | `FLASH_CS` | Flash U2-1（10kΩプルアップ） |
| 27 | `FLASH_MISO` | Flash U2-2 |
| 32 | `AUDIO_ADC` | U4A出力（録音） |
| 25 | `AUDIO_DAC` | 2段RC・U4B（再生） |
| 33 | `RELAY_EN` | Q1経由でK1を駆動 |
| 26 | `AUTO_PTT_EN` | R13経由でTLP592A入力LEDを駆動 |
| 39 | `PTT_SENSE_HIGH` | Q2コレクタ、HIGH=押下 |
| 13 | `SW_REC_N` | 外付けRECボタンSW1、LOW=押下 |
| 0 | 本体ボタン | 再生／停止／ループ選択の提案。起動時BOOT兼用 |
| 35 | 本体ボタン | M1～M4選択の提案 |
| 4/5/16/18/19/23 | LCD関連 | T-Display内蔵LCD専用 |

ESP32のSPI信号はピンマトリクスで割当可能。ESP32 ADC1を選んでいるため、Wi-Fi利用時のADC2共用問題を避ける。液晶と同時動作したときのADCノイズとDAC歪みは実機で評価する。

## 4. 電源・音声・保護回路

- `+3V3` はT-Display基板から供給し、100µF＋10µF＋0.1µF系で平滑する。U4、U2、K1コイルの電流はT-Display電源レギュレータの能力を超えてはならない。3Vコイルに3.3Vを印加する条件について定格資料と実測で確認する。
- U4 MCP6002デュアルオペアンプで録音用増幅とDAC出力バッファを共通実装する。VREFは3.3Vの抵抗2分圧。周波数特性、増幅率、マイク負荷は部品の実装値で評価する。
- U2 W25Q32RVCSJMは208mil幅SOP-8フットプリントを使う。U3 TLP592Aは1/2をLED、4/6を出力接点に使用し、3/5は未接続。
- K1のコイル逆起電力対策D1：**1=K（カソード）→+3V3、2=A（アノード）→RELAY_COIL_LOW**。回路上の極性を静的に検査済み。製造前には実際のダイオードの極性とランドを再確認する。
- 標準 `power:PWR_FLAG` をGND_AUDに配置。MOD1の3V3はpower_outに設定し、KiCadで電源供給元を区別する。ERC合格済みではない。
- J1/J2のpin4 `PTT_GND` と `GND_AUD` はR18=0Ωで結ぶ仮設計。無線機によってPTTの接地条件が違う場合は見直す。

**未解決の本質的な制約：** エレクトレットマイクの動作電源を無線機側MIC_AUDIO経由で供給する機種では、録音待機中にK1でマイク音声を切り離すとマイクのバイアス電圧が消えて録音できない可能性がある。現時点の回路は独立給電マイクまたは適切なメーカー別変換アダプターを前提とする。汎用マイクに無条件対応する設計ではない。対象無線機側のDC給電仕様を確認し、必要な場合のみ保護付きバイアス回路を確定する。

## 5. Flash容量

8,000サンプル/秒 × 1byte × 120秒 = **960,000byte/メモリ**。4メモリ合計3,840,000byte。4MiB（4,194,304byte）の外付けFlashに収まる。暫定割当は先頭64KiB管理領域、残り4等分（各1,032,192byte）とし、記録完了時に有効フラグを安全に確定する。

## 6. 含まれる編集可能な設計データ

| ファイル | 目的 |
|---|---|
| `VoiceMemory_TDisplay.kicad_sch` | KiCad 10形式・A3・グローバルラベル配線の回路図ドラフト |
| `VoiceMemory_TDisplay.kicad_sym` | Classic T-Display基板の24端子カスタムシンボル |
| `Voice_Memory.kicad_sym` | v2から無改変で複製した既存の個別部品ライブラリ |
| `sym-lib-table`, `fp-lib-table` | KiCadプロジェクト用ライブラリ参照 |
| `Voice_Memory.pretty/*.kicad_mod` | v2から複製したRJ45フットプリント |
| `pinmap.csv` | 接続端子一覧 |
| `bom_draft.csv` | 45種類のRef（U4は3ユニットで1部品）を収録した暫定BOM |
| `README.md` | 英語版の接続・留意事項 |

KiCad標準シンボルはv2のKiCad 10回路図に含まれる**正式なシンボル定義全体を無改変で使用**。T-Display基板のシンボルのみ新規作成。グローバルラベル座標とシンボル端子座標は50mil格子へ整列している。

## 7. 現在の検証状況

- **実施済み（静的）**：回路図S式の括弧整合確認、全38ネットに2個以上のグローバルラベルを確認、U4のBOM多重カウントを修正、D1論理極性を補正、GND用PWR_FLAGを設置。
- **未実施**：KiCad 10の正式ERC、PCB作図、DRC、フットプリント/実装部品の実寸照合、T-Display 3.3V負荷試験、録再・PhotoMOS・リレーの実機検証、無線機接続。
- **製造可否**：未承認。KiCad回路図はドラフトであり、ERCエラー0・警告0とは記載しない。

## 一次情報・確認資料
- LILYGO: https://wiki.lilygo.cc/products/t-display-series/t-display/
- Espressif ESP32 DAC: https://docs.espressif.com/projects/esp-idf/en/v6.0.3/esp32/api-reference/peripherals/dac.html
- Winbond W25Q32RV: https://www.winbond.com/hq/product/code-storage-flash/qspi-nor/w25q-rv/?__locale=en&partNo=W25Q32RVCSJM
- Toshiba TLP592A: https://toshiba.semicon-storage.com/info/TLP592A_datasheet_ja_20190624.pdf?did=17082&prodName=TLP592A
- v2既存回路・製造承認：`../voicememory/`、`../../../releases/v2-manufacturing-approved-2026-11-11/README.md`
