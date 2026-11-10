---
title: "VoiceMemory v1｜ファームウェア開発者向けハードウェア仕様書"
subtitle: "HK829代替・4チャンネル録音／再生ユニット"
author: "T-labDevelopment｜設計資料整理"
date: "2026-10-29"
lang: ja-JP
---

# 文書の位置付けと読み方

**文書版：v1-FW-HW-1.0（2026-10-29）／対応するハード設計呼称：VoiceMemory v1**

本書は、回路設計を担当していないファームウェア開発者が、MCUのGPIO、音声入力／出力、SPI Flash、リレー、PTT、電源の関係を把握し、安全にソフトウェア設計・実機検証できるよう整理した引き継ぎ仕様書である。回路記号や部品の役割を説明し、接続先の**物理ピン番号とネット名**を掲載する。作業者はまず「2.システム構成 → 4.MCUピン割当 → 5～8.各回路 → 10.起動・安全 → 12.検証手順」の順に参照する。

**重要：本書は製造用回路図の代替ではない。** 2026-10-05基準のKiCadプロジェクト一式はこの資料作成環境で再取得できず、ピン／接点の詳細は2026-09-30に保存された `voicememory.kicad_sch` から読み取った。10月5日基準BOMとの差異は本文で明示する。添付の回路系統図は説明用で、全ネットの配線保証ではない。現時点で「完全なv1のERC/DRC検証済み」「実機動作確認済み」とは扱わない。[H01–H04]

## 1. 表記・確度・変更管理

| 表記 | 意味 | 実装者の扱い |
|---|---|---|
| **v1方針** | ユーザーが2026-10-28に指定した仕様 | 変更する場合は別途指示が必要 |
| **BOM** | 2026-10-05基準プロジェクトから抽出した2026-10-19部品表 | 採用予定品・現基板の参考基準 |
| **SCH参照** | 2026-09-30保存のKiCad回路図の端子・ネット名 | 実PCBとの一致が確認されるまで参考実装情報 |
| **要照合** | 型番・端子・定数・パッケージに設計世代差がある | ファーム書き込み・通電前の確認項目 |
| **推奨／案** | ソフトウェア実装方針の提案 | 確定仕様や実機試験結果ではない |

v1では **R1～R20をSMD 2012（0805）、1/8W、基本±5%** とし、コンデンサもSMD主体とする。C3／C6／C9／C13の100µF電解は既存THTを維持する。抵抗・コンデンサの全面THT化案は撤回済み。C1は10µF・3216、C11とC19は1µF・1608化が設計方針（基板反映未確認）。J1／J2のRJ45は固定穴の修正フットプリントを採用するが既存PCBへの適用は未確認。[H03]

## 2. 回路全体の構成

![図1：システムのブロックと音声・制御系](figures/01_system_block.png){width=16cm}

| ブロック | ハードウェア | ファームウェアが担当すること |
|---|---|---|
| 電源 | BT1（単3×3）、SW1、U5（3.3V LDO） | 電源投入時の安全初期化。電池電圧測定用ADC線は**現回路にない** |
| 中央制御 | U1：CH32V003F4P6 | 入力走査、ADC録音、PWM再生、SPI通信、リレー／PTT／LED制御 |
| 録音前段 | J1、C11、RV1、U4A、R/C群 | PC4（ADC）の定周期サンプリング、飽和回避と音量試験 |
| 再生後段 | PC3、R9/R10、C15/C16、U4B、C19、RV2 | PWM生成、サンプル更新、音声開始／停止制御 |
| 不揮発記録 | U2：32Mbit SPI NOR Flash | JEDEC識別、消去、書込み、読出し、4chデータ管理 |
| 接点切替 | K1：AZ8462-3（3V、DPDT） | 録音時のマイク経路切替、再生音声のRIG側接続 |
| 自動送信 | U3：PhotoMOS、Q2 | RIG側PTTの自動制御、意図しない送信を禁止 |
| 操作・表示 | SW2～SW6、LED1、J3 | REC/M1～M4、LED赤/緑、WCH-Link書込み・デバッグ |

**基本電源:** 新品単3×3本で概ね4.5～4.8V → SW1 → `VBAT_SW` → U5の3.3V出力 `+3V3`。グランドは `GND_AUD`。U5 AP7333のメーカー公表入力動作範囲は2～6V、最大300mAのLDOだが、**電池終止電圧やリレー動作余裕を保証するものではない**。[E02]

## 3. 主要部品の構成と世代差

| Ref | 構成・現行基準 | 役割／FWへの影響 | 注意 |
|---|---|---|---|
| U1 | CH32V003F4P6／TSSOP-20 | 16KBプログラムFlash、2KB SRAM、10bit ADC、タイマ、SPI等 | 端子は表4-1。ADC/PWMの周辺機能リマップはSDKと照合 [E01] |
| U2 | 32Mbit（4MiB）SPI NOR | 4ch音声記録 | **10/05 BOM=AT25SF321B-SSHB／旧SCH=W25Q32RVCSJM**。後者は208mil幅で現PCBの約150milランドと非互換 [H02][E03] |
| U3 | 1a PhotoMOS（PTT用） | MCUの自動送信要求を絶縁接点へ変換 | **10/05基板=AQV212表記／後続選定=TLP592A(F)**。端子2・4・6と3・5の接続を通電前に照合 [H02][E04] |
| U4 | デュアル音声用オペアンプ／DIP-8 | 録音増幅・PWM再生バッファ | **10/05 BOM=NJM2732D／旧SCH=MCP6002-I/P**。シンボル機能・電源電圧・ピン互換性を要照合 [H02] |
| U5 | AP7333-33SAG-7／SOT-23 | 単3×3から3.3Vへ安定化 | 1:IN、2:OUT、3:GND（保存SCHネット名ベース） [E02] |
| K1 | AZ8462-3／3Vコイル、2c接点 | 音声とマイクPTTの2系統切替 | リレーは定常時NC。コイル約47mA級、MCU直結駆動不可 [E05] |
| Q1/Q2 | 2SC1815系NPN／TO-92 | リレーコイル、PhotoMOS LED駆動 | MCUからベース抵抗経由で制御 |
| LED1 | LT6CU7R／共通アノード | 赤・緑の状態表示 | 共通アノードは+3V3。MCUはLEDカソードをLOWにして点灯 |
| J1/J2 | 8P8C RJ45（MIC/RIG） | マイクと無線機の接続口 | 端子表は9章。固定穴修正はv1方針だが実基板未反映 |
| J3 | WCH-Link 3ピン | SWIO、GND、3.3V | 給電の多重接続と書込み中PTTに注意 |

**重要な整合性検査:** 実装するU2がAT25系かW25系かはソフトの初期化コマンド／JEDEC ID／書込み保護手順へ影響する。チップ種をソース上で推測固定せず、初期化時に読み取ったIDを許可テーブルで評価すること。未知のIDへ書込み・消去をしない。

## 4. U1（CH32V003F4P6）物理ピン割当

以下は**保存SCH（2026-09-30）のネットを抽出した端子対応表**である。**ピン番号はTSSOP-20のICパッケージ番号**であり、GPIO番号そのものではない。現v1実PCBとの完全一致は未検証。[H01]

| U1ピン | GPIO／機能 | ネット名 | FWでの用途・方向 | 初期化時の扱い |
|---:|---|---|---|---|
| 1 | PD4 | LED_G | 緑LED制御／出力 | HIGH相当で消灯（共通A） |
| 2 | PD5 | RELAY_EN | K1リレー駆動／出力 | **LOWでリレー非励磁** |
| 3 | PD6 | AUTO_PTT_EN | 自動PTT／出力 | **LOWで自動送信OFF** |
| 4 | PD7/NRST | （未接続） | リセット兼用端子 | 基板接続を照合するまで未使用 |
| 5 | PA1 | SW_M3_N | M3押しボタン／入力 | プルアップ。LOW=押下 |
| 6 | PA2 | SW_M4_N | M4押しボタン／入力 | プルアップ。LOW=押下 |
| 7 | VSS | GND_AUD | MCU GND | - |
| 8 | PD0 | SW_REC_N | REC押しボタン／入力 | プルアップ。LOW=押下 |
| 9 | VDD | +3V3 | MCU電源 | 3.3V |
| 10 | PC0 | LED_R | 赤LED制御／出力 | HIGH相当で消灯（共通A） |
| 11 | PC1 | FLASH_CS | U2 SPI CS／出力 | **HIGHでFlash非選択** |
| 12 | PC2 | PTT_SENSE_MCU | マイクPTT状態／入力 | 回路内の接点条件とプル回路を要照合 |
| 13 | PC3 | AUDIO_PWM | 再生PWM／出力 | 無音レベルへ初期化、出力開始時刻制御 |
| 14 | PC4 | AUDIO_ADC | 録音ADC／入力 | ADCチャネル選択をSDKで照合 |
| 15 | PC5 | SPI_SCK | SPIクロック／出力 | 初期は非選択状態 |
| 16 | PC6 | SPI_MOSI | SPI出力（Flash DI） | 書込み用 |
| 17 | PC7 | SPI_MISO | SPI入力（Flash DO） | 読出し用 |
| 18 | PD1/SWIO | SWIO | デバッグ／プログラム | 通常GPIOへ転用しない |
| 19 | PD2 | SW_M1_N | M1押しボタン／入力 | プルアップ。LOW=押下 |
| 20 | PD3 | SW_M2_N | M2押しボタン／入力 | プルアップ。LOW=押下 |

**GPIO動作の補足:** LED1は共通アノード（pin2=`+3V3`、pin1=`LED_G_K`、pin3=`LED_R_K`）。MCU PC0／PD4とLEDカソードの間にR18／R19（1kΩ）の電流制限抵抗がある。[H01] K1コイルとPhotoMOS LEDはトランジスタを介するため、**PD5／PD6はHIGHで駆動ON、LOWでOFF**が想定される。ただしピンリマップ・実機配線・リセット直後の入出力状態は未確認なので試験で確定する。

## 5. 録音系：マイクからADCまで

![図2：録音・再生の音声経路](figures/02_audio_paths.png){width=16cm}

1. J1 pin2の `MIC_AUDIO` が録音系へ分岐する。マイクの通常通話経路はK1のNC接点へ向かう（録音開始まで接続を維持）。
2. 録音入力はC11（BOM上1µF）で交流結合し、RV1（47kΩ）の録音レベル調整とVREFバイアスを経由してU4Aの正入力 `REC_LEVEL` へ入る。[H01][H02]
3. U4Aの出力 `REC_AMP_OUT` からR8（470Ω）を経て `AUDIO_ADC`／U1 PC4へ入る。C14はADC線とVREFとの間で高周波成分を減衰させる（10/05 BOMでは0.1µF）。
4. R4/R5（各10kΩ）により `VREF`（基準電位、理想的には約1.65V）を生成し、C18で平滑する。VREFは安定した直流中心電位であり、**0V基準の符号なしサンプル値へ直接変換するわけではない**。
5. U4AにはR6（22kΩ）、R7（4.7kΩ）、C5（1nF C0G）の帰還網がある。ゲイン・帯域は回路値と実機周波数応答により決まるため、ソフト側の固定ゲインを実測前に決めつけない。

**ADC実装上の注意:** 10bit ADCで読み取る場合、中央値を測定／補正し、8bit PCMへ圧縮する。PC4入力に負電圧や3.3V超過電圧を印加しない。録音無信号時のセンター値・雑音・過大入力クリッピングを測定し、必要ならDCオフセットとレベルをデジタル補正する。

## 6. 再生系：PWMからRIG_AUDIOまで

1. U1 PC3が `AUDIO_PWM` を出力。R9（470Ω）・C15、R10（470Ω）・C16による2段ローパスを通り、`PWM_F2` へ進む。
2. U4Bが再生信号をバッファし、`PLAY_BIASED` へ送る。C19（BOM上1µF）で交流結合し、RV2（10kΩ）によって出力音量を調整して `PLAY_OUT` を得る。
3. K1を再生側（NO）へ切替えると `PLAY_OUT` が `RIG_AUDIO`、すなわちJ2 pin2へ接続される。
4. 再生の前後ではPWMデューティを無音値に寄せ、必要なら短いフェード／待機時間を設け、接点切替時のポップ音を抑える（推奨）。

**PWMの重要点:** MCUはDACを搭載しないため**PWM→アナログフィルタ**を使用する。PWM搬送周波数は可聴帯域より十分高くし、タイマ分周・分解能・8kHzサンプル更新周期を同時に満たす設定を選ぶ。**PWM周波数の確定値はv1回路資料だけでは定まらない**。また、U4の実装ICが3.3Vで正常動作することを通電前に確認する。

## 7. K1切替接点・PhotoMOS・PTT

![図3：リレー、センス、自動PTTの接点関係](figures/03_relay_ptt.png){width=16cm}

### 7.1 K1の接点表（保存SCH）

| 系統 | K1番号 | ネット名 | 意味 |
|---|---:|---|---|
| A | 3 | MIC_AUDIO | NC（通常側） |
| A | 4 | RIG_AUDIO | COM（共通） |
| A | 5 | PLAY_OUT | NO（切替側） |
| B | 10 | RIG_PTT | NC（通常側） |
| B | 9 | MIC_PTT | COM（共通） |
| B | 8 | PTT_SENSE_LOCAL | NO（切替側） |
| coil | 1 | +3V3 | コイル＋ |
| coil | 12 | RELAY_COIL_LOW | コイル－（Q1） |

**通常・電源OFF（K1非励磁）:** MIC_AUDIO→RIG_AUDIO、MIC_PTT→RIG_PTT。**K1励磁時:** PLAY_OUT→RIG_AUDIO、MIC_PTT→PTT_SENSE_LOCALとなり、マイクPTTのRIG側接続は切れる。この切替は録音時の無線機への音声・PTT漏れ防止と再生注入に関係する。録音中にNO側へ再生音が出ないよう、必ず再生PWMは無音維持とする。

### 7.2 制御トランジスタ・PhotoMOS

- `PD5 → RELAY_EN → R11(1kΩ) → Q1`。Q1はK1コイルのローサイドスイッチ。D1（1N4148）はコイル逆起電力抑制。
- `PD6 → AUTO_PTT_EN → R13(4.7kΩ) → Q2`。Q2はU3入力LEDのカソード側電流を制御。U3の出力は `RIG_PTT` と `PTT_GND` 間を短絡する送信要求接点となる。
- U3の入力LED側は `+3V3 → R20 → U3 pin1 → pin2 → Q2 → GND_AUD`。**R20は旧保存SCHで330Ω、10/05 BOMで270Ω**と相違する。現物値・LED電流・部品型番を必ず照合する。[H01][H02]
- 旧SCHでU3=AQV212の出力側はpin6=`RIG_PTT`、pin4=`PTT_GND`。TLP592Aのメーカー図ではpin1=A、pin2=K、pin4・5・6は内部MOSFET側（pin5も内部接続端子）。**TLP592A実装時の3/5番パッド配線・接続方式の確認が必須**。[E04]

### 7.3 送信安全ルール（ファームウェア要件）

- **起動時、リセット時、停止時、異常時は `AUTO_PTT_EN=OFF` が最優先。** GPIO出力状態が未定の期間を短くし、最初にPD6/PD5を安全側へ設定する。
- 録音中は自動PTTを必ずOFF。再生終了時はPWM無音化→自動PTT OFF→接点復帰の順序でポップ音・意図しない送信を低減する。
- 送信開始時はK1切替・出力安定を確認してから自動PTTをONにすることを推奨。**ミリ秒単位の遅延値は未確定**（リレー仕様と実機で決める）。
- Flash読出し失敗、停止入力、WDTリセット、電池低下が疑われる状況では**PTT OFFを優先**。ソフトだけで外部無線機の送信状態を完全保証できないため実機確認を必須とする。
- `PTT_SENSE_MCU` はK1の接点状態に依存するため、「常にマイクPTTを検出できる」と仮定しない。録音状態ごとの真理値表を実測する。

## 8. SPI Flash・記録フォーマット設計

### 8.1 U2の配線表（保存SCH）

| U2ピン | 信号 | MCUネット／ピン | 動作 |
|---:|---|---|---|
| 1 | /CS | `FLASH_CS`／PC1（U1 pin11） | LOWで選択 |
| 2 | DO/IO1 | `SPI_MISO`／PC7（pin17） | MCUへ受信 |
| 3 | /WP/IO2 | `FLASH_WP_N`／R2で+3V3へプルアップ | 通常は書込み禁止解除 |
| 4 | GND | `GND_AUD` | 共通GND |
| 5 | DI/IO0 | `SPI_MOSI`／PC6（pin16） | MCUから送信 |
| 6 | CLK | `SPI_SCK`／PC5（pin15） | SPIクロック |
| 7 | /HOLD/IO3 | `FLASH_HOLD_N`／R3で+3V3へプルアップ | 通常は保持解除 |
| 8 | VCC | `+3V3` | 電源 |

**`FLASH_CS` はR1（10kΩ）で+3V3へプルアップされ、リセット中はFlash非選択を意図する。** U2は3.3V系のため5V SPI信号を加えない。[H01]

### 8.2 容量計算・4チャンネル

- 設計方針：**8kHz／8bit／モノラルPCM**、M1～M4の4chを基本とする。
- 1ch 120秒あたり：8,000 sample/s × 1byte × 120秒 = **960,000byte**。
- 4ch合計：3,840,000byte。32Mbit（4,194,304byte）Flashとの差は **354,304byte**（未使用領域・メタデータ等に充当可能）。
- この単純計算は音声データのみ。管理ヘッダ、セクタ境界、書込み保護、録音中断復旧、損傷対策を考慮した領域割当を別途定義すること。

**推奨ストレージ設計（未確定案）:** 先頭にバージョン・検査情報を持つ管理領域を確保し、M1～M4をセクタ境界に揃えた固定領域へ割り当てる。録音中のデータ欠損を避けるため、録音開始前に消去を完了するか、書込みに間に合う先行消去・バッファ方式を設ける。Flashの書込み可能条件・消去時間・ページ境界は**実搭載品のデータシート**に従う。高頻度書換えと電源断による管理情報破損を考慮する。

### 8.3 実装リソースの目安

CH32V003はメーカー公表で**プログラムFlash 16KB、SRAM 2KB、48MHz上限、10bit ADC、SPI**を搭載。[E01] 8kHzのサンプル周期は125µs。PWM/ADCの時刻管理は割込みまたはタイマを用い、SPI書込み中も音声更新を妨げない設計が必要である。サンプルバッファを256B×2本用意すると512Bを占めるため、スタックと割込み負荷を含めてRAM予算を管理する（このサイズは**例**であり確定要件ではない）。

## 9. RJ45 J1／J2・操作部・デバッグ端子

### 9.1 J1=マイク側、J2=無線機側（保存SCH）

| Pin | J1（MIC側） | J2（RIG側） | 接続上の扱い |
|---:|---|---|---|
| 1 | GND_AUD | GND_AUD | 音声基準GND、直結 |
| 2 | MIC_AUDIO | RIG_AUDIO | K1接点Aで切替 |
| 3 | MIC_PTT | RIG_PTT | K1接点Bで切替 |
| 4 | PTT_GND | PTT_GND | PTT接点GND、直結系 |
| 5 | MIC_UP | MIC_UP | 直結 |
| 6 | MIC_DOWN | MIC_DOWN | 直結 |
| 7 | UD_COMMON | UD_COMMON | 直結 |
| 8 | MIC_DC_PASS | MIC_DC_PASS | 直結 |

**重要:** RJ45番号は本基板の8P8C基準であり、Icom・Yaesu・Kenwood等のマイク端子ピン割当がこの表と一致することを意味しない。メーカー別変換ケーブルで対応する。ファームウェアからUP/DOWN等を操作・検出する線は**存在しない**。また、RJ45の挿し込み向き・実装の鏡像はコネクタ図面と製作ケーブルのピン番号で確認する。[H01][H03]

![図4：RJ45修正フットプリントの固定穴・信号ピン位置](figures/rj45_footprint_layout.png){width=14cm}

固定穴φ3.20mm×2・中心間12.70mm、信号ピン8本φ0.90mm、ピン間1.02mm・列間1.78mm、固定穴と信号列のオフセット4.32mm（ユーザー提供寸法図準拠）。**フットプリントデータは同梱するが、KiCad原本への適用・端子向きの最終照合は未完了**。[H03]

### 9.2 ボタン・LED・書込み

| Ref | MCU信号 | 動作 | 注意 |
|---|---|---|---|
| SW2 REC | PD0 / `SW_REC_N` | GNDへ落ちるモーメンタリ入力 | LOW=押下、デバウンス必要 |
| SW3 M1 | PD2 / `SW_M1_N` | 同上 | チャンネル選択 |
| SW4 M2 | PD3 / `SW_M2_N` | 同上 | 同上 |
| SW5 M3 | PA1 / `SW_M3_N` | 同上 | 同上 |
| SW6 M4 | PA2 / `SW_M4_N` | 同上 | 同上 |
| LED1 RED | PC0 / `LED_R` | LOWで点灯 | 抵抗R18 1kΩ |
| LED1 GREEN | PD4 / `LED_G` | LOWで点灯 | 抵抗R19 1kΩ |
| J3 pin1 | +3V3 | WCH-Link給電・基準 | 接続環境により供給衝突注意 |
| J3 pin2 | PD1 / SWIO | ダウンロード・デバッグ | GPIO兼用しない |
| J3 pin3 | GND_AUD | GND | GND共有 |

**操作意味の区別:** `REC`は録音操作、`M1～M4`は録音・再生対象のメモリ選択ボタンである。録音開始／停止を短押し／長押しのどちらで割り当てるか、ループ再生のトリガ、複数ボタン同時押しの優先度、LED点滅パターンは**ファームウェアUI仕様として別途確定すべき事項**。本書では回路から断定しない。

## 10. ファームウェア状態設計と安全初期化

| 状態（案） | K1 RELAY_EN | U3 AUTO_PTT_EN | ADC/PWM | 運用上の意味 |
|---|---|---|---|---|
| POWER_ON / INIT | OFF | **OFF** | PWM無音・ADC待機 | GPIOを最初に安全状態へ設定 |
| IDLE / PASS_THROUGH | OFF（NC） | OFF | ADC停止、PWM無音 | マイクを無線機へ通過 |
| RECORD_PREP | ON（NO） | **OFF** | ADC開始準備、PWM無音 | マイクからRIGを遮断して録音 |
| RECORDING | ON（NO） | **OFF** | PC4 ADC収録、SPI保存 | M1～M4に記録、最大120秒 |
| PLAY_PREP | ON（NO） | OFF | PWM無音→安定化 | PLAY_OUTをRIG_AUDIOへ接続 |
| PLAYING | ON（NO） | ON（送信時） | SPI読出し→PC3 PWM | 音声を送信。ループ時は終了判定制御 |
| STOP / FAULT | 最終的にOFF | **直ちにOFF** | PWM無音、SPI書込停止 | 安全に通話パススルーへ復帰 |

これは**ハード接続に沿った実装推奨ステートマシン**であり、ボタンの押し方・待ち時間・録音中の手動PTTの許可等は未確定。とくに `PTT_SENSE_MCU` の接点状態依存性があるため、実機で入力表を測定してから操作判定を決める。

起動順序の推奨：①割込み・PWMを不用意に有効化しない、②PD6=OFF・PD5=OFF・PC1=HIGHを先に設定、③LED消灯、④ボタン入力／プルアップ初期化、⑤タイマ・ADC・SPI初期化、⑥JEDEC ID・自己診断、⑦IDLEへ移行。FAULT処理は**送信OFFを最優先**とし、その後に記録停止・LEDエラー表示を行う。

**電源断時の限界:** 外部無線機のマイク/PTTが基板NCへ戻ることは機械的接点の特性だが、コネクタ配線不良・接点溶着・周辺故障まで保証しない。録音中のFlash書込み途中に電池が外れた場合、未コミット音声と管理情報の破損が生じ得る。

## 11. 部品値・接続ネットの参照表

**本章のネット関係は保存SCH（2026-09-30）基準、値は2026-10-05 BOMに近い最新版を優先して記載。** 9月回路図ではC2/C4等の容量が異なり、10月値への置換後の位相・フィルタ計算は未検証。配線照合用として使う。[H01][H02]

### 11.1 抵抗（R1～R20、SMD 2012／1/8W／基本±5%）

| Ref | 値（10/05 BOM） | 端子間ネット（保存SCH） | 役割 |
|---|---:|---|---|
| R1 | 10k | FLASH_CS ↔ +3V3 | SPI CSプルアップ |
| R2 | 10k | FLASH_WP_N ↔ +3V3 | WP非アサート |
| R3 | 10k | FLASH_HOLD_N ↔ +3V3 | HOLD非アサート |
| R4 / R5 | 各10k | +3V3 ↔ VREF / VREF ↔ GND_AUD | 1/2電源基準電位 |
| R6 / R7 | 22k / 4.7k | REC_AMP_OUT ↔ REC_FB / REC_FB ↔ VREF | U4A帰還 |
| R8 | 470 | REC_AMP_OUT ↔ AUDIO_ADC | ADC入力直列 |
| R9 / R10 | 各470 | AUDIO_PWM ↔ PWM_F1 / PWM_F1 ↔ PWM_F2 | PWMローパス |
| R11 | 1k | RELAY_EN ↔ Q1_BASE | K1駆動抵抗 |
| R12 | 100k | Q1_BASE ↔ GND_AUD | Q1プルダウン |
| R13 | 4.7k | AUTO_PTT_EN ↔ Q2_BASE | U3駆動抵抗 |
| R14 | 100k | Q2_BASE ↔ GND_AUD | Q2プルダウン |
| R15 | 220k | +3V3 ↔ PTT_SENSE_LOCAL | PTTプルアップ系 |
| R16 | 22k | PTT_GND ↔ GND_AUD | PTT基準GNDとの間 |
| R17 | 4.7k | PTT_SENSE_LOCAL ↔ PTT_SENSE_MCU | MCU入力直列 |
| R18 / R19 | 各1k | LED_R_K ↔ LED_R / LED_G_K ↔ LED_G | LED電流制限 |
| R20 | **270Ω（10/05 BOM）** | +3V3 ↔ AQV_LED_A | U3 LED電流制限（旧SCH値330Ω） |

### 11.2 コンデンサ・可変抵抗

| Ref | 値（10/05 BOM） | 端子間ネット（保存SCH）／扱い |
|---|---|---|
| C1 | 10µF/35V SMD 3216 | VBAT_SW ↔ GND_AUD |
| C2 | **1µF/25V X5R SMD2012** | VBAT_SW ↔ GND_AUD（9月SCHは0.1µF） |
| C3 | 100µF/16V THT | VBAT_SW ↔ GND_AUD |
| C4 | **1µF/25V X5R SMD2012** | +3V3 ↔ GND_AUD（9月SCHは0.1µF） |
| C5 | 1nF/50V C0G SMD2012 | REC_AMP_OUT ↔ REC_FB |
| C6 | 100µF/16V THT | +3V3 ↔ GND_AUD |
| C7 / C8 | 各0.1µF/50V SMD2012 | +3V3 ↔ GND_AUD |
| C9 | 100µF/16V THT | +3V3 ↔ GND_AUD |
| C10 | 0.1µF/50V SMD2012 | +3V3 ↔ GND_AUD |
| C11 | 1µF/25V（v1方針：1608化） | MIC_AUDIO ↔ REC_AC |
| C12 | 1nF/50V C0G SMD2012 | REC_LEVEL ↔ VREF |
| C13 | 100µF/16V THT | +3V3 ↔ GND_AUD |
| C14 | 0.1µF/50V SMD2012 | AUDIO_ADC ↔ VREF |
| C15 / C16 | 各0.1µF/50V SMD2012 | PWM_F1 ↔ GND_AUD / PWM_F2 ↔ GND_AUD |
| C17 | 0.1µF/50V SMD2012 | PTT_SENSE_MCU ↔ GND_AUD |
| C18 | **10µF/6.3V X5R SMD2012** | VREF ↔ GND_AUD（9月SCHは0.1µF） |
| C19 | 1µF/25V（v1方針：1608化） | PLAY_BIASED ↔ PLAY_AC |
| RV1 | 47kΩ THT | 端子1=VREF、端子3=REC_AC、ワイパ2=REC_LEVEL |
| RV2 | 10kΩ THT | 端子1=GND_AUD、端子3=PLAY_AC、ワイパ2=PLAY_OUT |

**音声ライン変更不可の注意:** C11/C19の1608化はサイズの変更であって、録音・再生の電気信号経路を変更するものではない。部品が未確定のままソフト側で入力値の異常を補正し続けるのではなく、まず現物の容量、実装、バイアスを確認する。

## 12. ファームウェア担当者向け検証手順

| 優先 | 検証項目 | 期待する状態／記録する値 | 合格の判断 |
|---:|---|---|---|
| 1 | 電源投入と安全出力 | PD5・PD6初期OFF、Flash CS HIGH、+3V3実測 | 無操作でPTTがONにならない |
| 2 | SWIO書込み | J3 pin2 SWIO、GND共通、適切な給電 | 書込み・リセット安定 |
| 3 | GPIO入力 | REC/M1～M4のLOW検出、チャタリング | 各ボタン単独認識 |
| 4 | LED | PC0/PD4をLOWにして赤/緑点灯 | 極性が表と一致 |
| 5 | SPI | JEDEC ID、基本Read、Status、Write/Erase | 実チップを同定し範囲内の可逆テストが成功 |
| 6 | ADC無信号 | VREF中心値、サンプリング周期、ノイズ | 8kHz・飽和しない |
| 7 | 録音 | MIC→C11→U4A→PC4 | 音声が再生可能なデータで記録される |
| 8 | PWM出力 | PC3から無音→テスト波形、U4Bの振幅 | 波形の直流偏移・歪みを確認 |
| 9 | K1接点 | 非励磁NC／励磁NOの導通、接点切替 | J1→J2、PLAY_OUT→J2を切替可能 |
| 10 | PTT | PD6出力とU3接点、絶縁・漏れ電流 | 想定と逆の送信をしない |
| 11 | 録音/再生統合 | 4ch、停止、無録音再生、ループ | 各状態から安全にIDLE復帰 |
| 12 | 障害時 | Flashエラー、突然の電源断、WDT、スイッチ連打 | 自動PTTを残さず停止・復帰 |

**無線機につないだ初回検証は、送信を伴わない抵抗負荷・テスター・模擬PTT負荷から始めること。** いきなり無線機のマイク端子へ配線すると、端子番号違いによるPTT連続ONやマイクラインの電圧印加が起こり得る。RIGの機種別結線表と外部変換ケーブルは別文書扱いだが、本書の9章が基板側の一次情報となる。

## 13. 未照合事項／引き継ぎチェックリスト

- [ ] 正本 `voicememory-2026-10-05_162836.zip` を受領し、`.kicad_sch`、`.kicad_pcb`、シンボル・フットプリントを保存。
- [ ] v1方針（C11/C19サイズ、RJ45固定穴、全面THT化撤回）の**実PCB反映状況**を確認。
- [ ] U2の実装品AT25SF321B／W25Q32RVのいずれかを型番・パッケージ・JEDEC IDで確定。
- [ ] U3の実装品AQV212／TLP592Aのピン1/2/3/4/5/6、R20の値（270/330Ω）を実基板に照合。
- [ ] U4実装品NJM2732D／MCP6002の電源条件・ピン互換性・入出力範囲を確認。
- [ ] K1接点Bと `PTT_SENSE_MCU` の状態別論理を実測。
- [ ] J1/J2実物のピン1向き・固定穴・ケーブル側端子を最終確認。
- [ ] 録音／再生UI（短押し・長押し・ループ）とLED表示仕様を確定。
- [ ] KiCad 10.xでERC 0／DRC 0を目標に検査（現時点では**未実行**）。
- [ ] 実機を用い電源・SPI・ADC・PWM・PTT安全試験を完了。

## 14. 添付図面と参照先の索引

| 資料番号 | 同梱・参照資料 | 中身／注意 |
|---|---|---|
| D01 | `figures/01_system_block.png` | v1回路系統図。本書2章 |
| D02 | `figures/02_audio_paths.png` | ADC録音／PWM再生の経路。本書5～6章 |
| D03 | `figures/03_relay_ptt.png` | K1／U3／PTT・センス回路。本書7章 |
| D04 | `figures/legacy_block_diagram_20261025.png` | 先行説明図。**9月保存SCHベース**のため型番・値をv1確定扱いしない |
| D05 | `figures/legacy_network_details_20261025.png` | 先行詳細接続図。**9月保存SCHベース**、ピン表の補助 |
| D06 | `figures/rj45_footprint_layout.png` | ユーザー寸法図に基づくRJ45穴・端子配置 |
| D07 | `Voice_Memory.pretty/RJ45_8P8C_THT_15.91x15.10.kicad_mod` | v1で採用するRJ45修正フットプリント（PCB未反映） |
| D08 | `sources/RJ45_部品裏面参考写真.jpeg` | 提供された実部品の裏面写真、固定突起の確認用 |
| D09 | `sources/RJ45_PCB_LAYOUT_寸法図.png` | 提供された寸法図、穴径・穴間距離・ピン列の根拠 |
| H01 | `voicememory.kicad_sch`（2026-09-30保存） | 保存SCHのネット名・U1割当。**本書の外にある参照資料** |
| H02 | `HK829_VoiceMemory_10set_BOM_Procurement_2026-10-19.xlsx` | 2026-10-05実回路抽出BOM／部品差分。**本書の外にある参照資料** |
| H03 | `VoiceMemory_v1_reference_source.zip` 内 `docs/V1_BASELINE_JA.md` | 2026-10-28のv1設計仕様・未適用事項。原本参照文書を本ZIPに写しで同梱 |
| H04 | `voicememory-2026-10-05_162836.zip` | **基準KiCad正本のファイル名**。今回未取得、添付不可 |

### メーカー一次資料（開発時の照合元）

| ID | 発行元 | 仕様・リンク | 確認内容 |
|---|---|---|---|
| E01 | WCH | [CH32V003製品情報](https://www.wch-ic.com/products/CH32V003.html)、[公式Datasheet](https://www.wch-ic.com/downloads/CH32V003DS0_PDF.html)、[Reference Manual](https://www.wch-ic.com/downloads/CH32V003RM_PDF.html) | 48MHz、16KB Flash、2KB RAM、ADC、SPI、SWIO |
| E02 | Diodes Inc. | [AP7333製品情報](https://www.diodes.com/part/view/AP7333)、[データシート](https://www.diodes.com/datasheet/download/AP7333.pdf) | 3.3V LDO・電源条件 |
| E03 | Winbond | [W25Q32RVCSJM製品情報](https://www.winbond.com/hq/product/code-storage-flash/qspi-nor/w25q-rv/?__locale=ja&partNo=W25Q32RVCSJM) | 32Mbit、2.7–3.6V、SOP-8 208mil |
| E04 | Toshiba | [TLP592Aデータシート](https://toshiba.semicon-storage.com/info/TLP592A_datasheet_ja_20190624.pdf?did=17082&prodName=TLP592A) | PhotoMOSの入力LEDと出力端子（代替時照合必須） |
| E05 | American Zettler | [AZ8462-3製品情報（代理店表示）](https://www.digikey.jp/ja/products/detail/american-zettler/AZ8462-3/18340735) | 3V・DPDT・コイル約46.7mA級 |

**引用規則:** 本文の `[Hxx]` は内部設計資料、`[Exx]` はメーカー一次資料の追跡番号。本文だけでは明らかにできない配線・実機状態は「未確認」と記載した。文書と図面は本ZIP内で完結する説明を提供するが、**KiCad正本の未収録という制約を解消したものではない**。

---

**付録A：保存SCHに基づく先行回路説明図（v1照合前）**

![付録A-1 主要回路接続・動作説明図（9月保存SCHベース）](figures/legacy_block_diagram_20261025.png){width=16cm}

**付録B：保存SCHに基づくネット接続説明図（v1照合前）**

![付録B-1 U1、J1/J2、K1、U2、U3等の先行接続説明図](figures/legacy_network_details_20261025.png){width=16cm}

**END / 本書の管理単位：文書版 v1-FW-HW-1.0。Gitのハード基準タグ `v1` は変更しない。**
