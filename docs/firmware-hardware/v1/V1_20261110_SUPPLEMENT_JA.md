# VoiceMemory v1 — 2026-11-10現行KiCadに対するファームウェア資料補足（2026-11-11）

## 基準および優先順位

この補足は `VoiceMemory_v1_ファームウェア開発者向けハードウェア仕様書.md` （2026-10-29版）を**差分補足**する。旧版を改ざんせず、最新の部品値・型番・未検証点を明示する目的で作成した。

1. 正本：`../../../hardware/kicad/voicememory/voicememory.kicad_sch` と同ディレクトリの `.kicad_pcb`、フットプリント。
2. 2026-10-30の変更記録：`../../../hardware/reports/ECO_2026-10-30_JA.md`。
3. 2026-11-10のコンデンサ変更：`../../../hardware/reports/CAP_MIN_0805_2026-11-10_JA.md`。
4. 旧ファームウェア資料は回路思想と端子対応の参考だが、値／型番／実PCBの検証を代替しない。

## 現行SCHの静的読取りで確認した部品値とFootprint

| Ref | Value（現行SCHの表示） | Footprint（現行SCHの指定） | FWへの関連 |
|---|---|---|---|
| U1 | CH32V003F4P6 | MCUパッケージを現行プロジェクトで参照 | 端子リマップとピン初期状態を要照合 |
| U2 | W25Q32RVCSJM | `Package_SO:SOP-8_5.28x5.23mm_P1.27mm` | AT25SF321BではなくWinbond用JEDEC ID/書込み・消去・Status命令を確認 |
| U3 | TLP592A(F) | `Package_DIP:DIP-6_W7.62mm` | 自動PTT。出力pin4/6を使用し、pin5は外部未接続のECO方針 |
| U4 | NJM2732D | `Package_DIP:DIP-8_W7.62mm` | 3.3Vでの動作・ピン互換、録音/再生利得を実装前に確認 |
| U5 | AP7333-33SAG | `Package_TO_SOT_SMD:SOT-23` | 3.3Vロジック電源 |
| K1 | AZ8462-3 | `Relay_THT:Relay_DPDT_Kemet_EC2_NU` | NC/NO接点、リレー駆動の状態管理 |
| R20 | 270 | `Resistor_SMD:R_0805_2012Metric` | PhotoMOS駆動LED電流の確認 |
| C2,C4,C11,C19 | 1uF/25V PMLCAP | `Capacitor_SMD:C_1206_3216Metric` | 電源デカップリングおよび音声AC結合の素材変更、試作評価要 |
| C7,C8,C10,C14,C15,C16,C17 | 0.1uF/100V CH | `Capacitor_SMD:C_1206_3216Metric` | フィルタ/デカップリングの高周波・ノイズ性能を確認 |
| C5,C12 | 1nF / C0G | `Capacitor_SMD:C_0805_2012Metric` | 1nFを0.1uFと取り違えない |
| C18 | 10uF / X5R | `Capacitor_SMD:C_0805_2012Metric` | VREF平滑の実測推奨 |

この表の部品名・主要値は2026-11-11にGitHub上の現行`.kicad_sch`のReference/Value/Footprintを静的に検索したもの。**実物の一致、パッド配線導通、電気的妥当性を確認済みとするものではない**。一部表記は2026-11-10調達レビューにある定格を併記。

## 旧資料からの重要差分

- `U2=AT25SF321B` と記載されている旧BOM・説明は現行基板指定と一致しない。現行はWinbond W25Q32RVCSJM。SPI StandardモードでのJEDEC ID・Read・Page Program・Sector Erase・Status動作を実機検証する。
- `U3=AQV212` の説明は旧版。現行はTLP592A(F)、入力LED=pin1/2、出力=pin4/6、pin5外部未接続の設計方針。
- C11/C19を0603へ小型化した案は撤回し、2026-11-10版で**1206**に戻している。C2/C4の値も現行は**1uF PMLCAP**。旧文書の値と混用しない。
- 0.1uFの7箇所はX7RからCHへ素材変更。音声・ADC/PWM・リセット・SPIへの影響はまだ実測していない。
- `U4=NJM2732D` は現行SCH表示。旧検討のMCP6002とのピン・性能互換を無条件に仮定しない。
- 旧文書のU1ピン表は2026-09-30 SCH起源。最新基板への各ピンの完全照合を済ませた表ではないため、ファームウェア実装時はKiCad現行ネットを照合する。

## 安全状態の優先事項

- 起動・初期化・故障・録音中は `AUTO_PTT_EN` をOFF、PWMは無音を基本とする。
- マイクPTT入力の割込み・優先制御を含め、録音中には無線機側へPTTや音声を漏らさず、録音終了時はマイクPTT解放で録音確定する設計方針。
- 再生中／ループ中のマイクPTT優先解除を設計方針に維持。ただしK1の切替状態によってPTTセンス経路が変わるため、**常時検出できることは実測未検証**。
- 4ch SPI Flash、連続録音の安全上限120秒、ループ間PTT OFFを基本仕様とする。記録容量上限や寿命を120秒保証と混同しない。

## 2026-11-10 PCBレビューに残る未解決事項

C7のLED_R付近、C10のRELAY_COIL_LOW、C16のMIC_AUDIO/GND近傍、C19のGNDビア付近で**異ネット接近・重なりの静的検出結果**があり、少なくとも現段階のPCBは製造用に使えない。正式ERC/DRC、Zone再フィル、現物RJ45の向き・電源・音声・自動PTTの実機検証は未実施。

## 図版

図版の再構成と旧PNG/JPEGの原本未回収状況は `FIGURES_RECOVERY_2026-11-11_JA.md` を参照。新しいSVGは**説明用であり回路図の代わりではない**。

## この補足の検証範囲

- GitHub上の現行SCHから主要Ref/Value/Footprintの静的確認：実施。
- 元図版・バンドルの完全復元：未実施（元バイト取得不可）。
- KiCad 10 CLIによるERC/DRC、ゾーン再フィル：未実施。
- テスト基板の動作試験：未実施。
