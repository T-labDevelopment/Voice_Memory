# VoiceMemory — ESP32 T-Display Prototype（主開発）

**主開発対象：ESP32 T-Display 16MB版。** 旧CH32V003設計は履歴として保持し、混在させない。

## 直近の発注準備データ

- [2026-11-24 23:41版 KiCad / MPUピン検証](hardware/kicad/voicememory_tdisplay/preorder_pin_verified_2026-11-24/README.md)
- [MPU 24ピン接続監査](hardware/kicad/voicememory_tdisplay/preorder_pin_verified_2026-11-24/PIN_AUDIT_2026-11-24_JA.md)
- [製造直前版受領・検証記録](releases/esp32-tdisplay-preorder-pin-audit-2026-11-24/README.md)

2026-11-24 23:41版はユーザーが基板サイズ・配置を調整した版。添付ERC/DRCは0件。基板製造用Gerberはこの版から新規出力する必要がある。

### 履歴管理

前回の100mm改訂版と16:45の発注履歴は保持。既存の v1/v2(CH32V003) 設計は保存したまま。`main` の統合はユーザーの許可があるまで実施しない。
