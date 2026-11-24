# VoiceMemory T-Display ESP32 Rev.A — 12mm角5ボタン追加・PCB配置記録

- 改訂: 2026-11-24。変更元は `VoiceMemory_TDisplay_RevA_compact_PCB_2026-11-24.zip`（45部品、60.6×64.4mm、未配線）。
- 追加SW2～SW5の4ボタンとR23～R26（10kΩ/0805）の4抵抗を追加。録音SW1の6mm角を12mm角に交換。
- **PCB: 53部品、12mmタクト5個、外付けプルアップ抵抗4個、外形104.3×64.4mm**。T-Display本体、リレー、RJ45、増幅器、Flash等の元の位置は維持。
- 操作用スイッチ5個はユニット左側へ2列×2行＋REC下段。スイッチのCourtyardは互いに重ならず、基板端から2mm以上の間隔を確保（Pythonによる静的検査）。
- R23～R26は既存モジュール下の空き4セルへ配置。部品はすべてF.Cu側。既存の小型部品は変更しない。
- **KiCadの標準 `Switch:SW_Push` を使用**。フットプリントは KiCad公式 `Button_Switch_THT.pretty/SW_PUSH-12mm.kicad_mod` 完全版を、KiCad 10の環境差分で未解決にならないよう 
  `VoiceMemory_TDisplay.pretty/SW_PUSH-12mm.kicad_mod` に原本のまま追加（出典 Git Blob SHA: `6e8f066cfacb6b191768e98bb9497655634127f7`）。
- 12mm角タクトスイッチの実部品型番は未確定。**12.5mm×5mm の4端子配置・穴径1.3mm、B3F系の位置決めボス有無**を製造前に正式型番・メーカーのパターン図と照合する。
- GPIO: REC 13、CH1 36、CH2 37、CH3 38、CH4 15。すべて押下LOW、10kΩで+3.3Vへプルアップ。GPIO36～38は内蔵プルアップなし。
- GPIO15はストラップ端子MTDO。押しながらリセットするとROMログが出なくなるが、通常ブートは可能というEspressif資料あり。GPIO12とGPIO2は採用しない。
- 回路図はA3からA2へ用紙を拡大して追加部品を収録。グローバルラベルを50milグリッドへ配置し、元の4本の未接続マーカーを取り除いた。
- TFT表示インジケーター集約、AZ8462-3リレー、TLP592A、SPI Flash、音声回路等は不変。
- **未配線**。KiCad 10のERC、DRC、実機スイッチ導通・接点配置検査は未実施。位置だけの静的チェックでは製造可と判定しない。

## 対応表

| 基板Ref | 操作 | GPIO | 信号 | 抵抗 |
|---|---|---:|---|---|
| SW1 | REC | 13 | SW_REC_N | R19（既設） |
| SW2 | CH1 | 36 | SW_CH1_N | R23 10kΩ |
| SW3 | CH2 | 37 | SW_CH2_N | R24 10kΩ |
| SW4 | CH3 | 38 | SW_CH3_N | R25 10kΩ |
| SW5 | CH4 | 15 | SW_CH4_N | R26 10kΩ |

## ファームウェアへの影響

- CH1～CH4はそれぞれ選択先が固定の物理ボタン。長押し・複数同時押下の意味はまだ未定義。RECは既存のマイクPTT連動録音制御とは独立の録音操作（SW1）を継続。
- 外付けプルアップにより通常HIGH、押下LOWとなる。適切なチャタリング除去をファームウェアで実装する。
- 入力ピンを再割当する場合は、回路図・PCB・GPIO対応表・ファームウェアの全てを同時更新する。

## 参考資料

- LILYGO T-Display（初代）公式: https://wiki.lilygo.cc/products/t-display-series/t-display/
- Espressif GPIO15の起動時挙動: https://docs.espressif.com/projects/esptool/en/latest/esp32/advanced-topics/boot-mode-selection.html
- KiCad公式 12mm フットプリント: https://github.com/KiCad/kicad-footprints/blob/master/Button_Switch_THT.pretty/SW_PUSH-12mm.kicad_mod
- Omron B3Fシリーズ（比較用、最終採用品の指定ではない）: https://components.omron.com/amusement/products/pdf/b3f.pdf
