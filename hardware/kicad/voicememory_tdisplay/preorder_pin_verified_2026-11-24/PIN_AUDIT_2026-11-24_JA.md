# VoiceMemory T-Display Rev.A 23:41製造直前ピン監査記録

- 基準アーカイブ：`VoiceMemory_TDisplay-2026-11-24_234138.zip`
- アーカイブSHA-256：`188de5bfed730062eddecdf40f88ef4d4e4edc54cd06bbaf31864980c419eac3`
- 現物KiCadからの静的解析：T-Display 24ピンの回路図定義、PCBネット、モジュールフットプリント一致 **24/24 PASS**
- 外部ボタン6個：各GPIO信号とGND接続一致 **6/6 PASS**
- Wake用R27=10kΩ：3V3→GPIO36；USB検出R28/R29=100kΩ：5V→ADC(GPIO38)→GND **PASS**
- PCB外形：X=65.151..145.161mm、Y=34.780..134.780mm、外接寸法 **80.010 × 100.000mm**。内側に別のEdge.Cuts矩形あり（ケーブル通し穴）
- ERCレポート（2026-11-24 23:09:45）：エラー0、警告0。複数項目を除外。
- DRCレポート（2026-11-24 23:41:29）：違反0、未接続0、フットプリントエラー0。複数項目を除外。
- GPIO2/12/15（strapping）：外部回路は未接続。液晶用GPIO4/5/16/18/19/23は割当なし。
- 既存のRTCピンGPIO36はEXT0によるLOWウェイク、GPIO38はADC1_CH2（入力専用）、GPIO32はADC1_CH4、GPIO25はDAC1。

## 調達・実機検証上の条件

1. GPIOヘッダのピン配置はLILYGO初代T-Display V1.1の公開Pinoutと一致するが、採用予定TENSTAR 16MB実機の完全なピン互換はメーカー純正回路図では未保証。実品のシルクと向きを照合すること。
2. USB 5Vヘッダ端子が電池単独運用で0V相当となるか、3.3V出力がDeep Sleep中も供給されるかは実機未検証。USB監視とWake機能はハードロジックとして成立するが、動作保証ではない。
3. ADCに5Vを直結せず100kΩ/100kΩ分圧による約2.5Vを予定。ADC入力インピーダンスと閾値・ノイズ・ADC減衰設定はFW・実機試験対象。
4. Deep SleepではTFTバックライトをOFF、AUTO_PTT_ENとRELAY_ENをOFFにしてから休止へ移ること。復帰後は安全初期化を要する。
5. 16MB Flashの実容量と録音パーティションはファームウェアで別途確認すること。
6. 23:41 PCBデータを元に新しいGerberとドリルを生成すること。過去版のPCB.zipは流用しないこと。

## 情報源
- ユーザー添付KiCadデータ・ERC(4).rpt・DRC(2).rpt
- LILYGO初代T-Display資料：https://wiki.lilygo.cc/products/t-display-series/t-display/
- LILYGO Pinout参照：https://www.espboards.dev/esp32/lilygo-ttgo-t-display-1-14/
- Espressif GPIO/RTC仕様：https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/gpio.html
- Espressif Sleep仕様：https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/sleep_modes.html
