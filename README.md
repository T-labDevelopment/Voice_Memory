# Voice_Memory — 主開発：ESP32 T-Display Rev.A

**2026-11-25時点の主開発対象はESP32 T-Display 16MB版。** CH32V003 v1/v2は履歴として保持します。設計世代や製造用スナップショットは上書きせず区別します。

- [2026-11-25 00:46 Gerber受領・差し替え確認（PCB(2).zipを発注用正本とする）](releases/esp32-tdisplay-orderfiles-check-2026-11-25/ORDER_STATUS_JA.md)
- [2026-11-25 00:39 KiCad設計正本](hardware/source-archives/tdisplay-order-candidate-2026-11-25/VoiceMemory_TDisplay-2026-11-25_003943.zip)
- [2026-11-24 23:41 発注前GPIO検証版](releases/esp32-tdisplay-preorder-pin-audit-2026-11-24/README.md)
- [2026-11-24 旧Prototype発注データ](releases/esp32-tdisplay-prototype-ordered-2026-11-24/README.md)
- [旧CH32V003版の製造履歴](releases/v2-manufacturing-approved-2026-11-11/README.md)

**発注用Gerber正本：** [PCB(2).zip](hardware/source-archives/tdisplay-order-candidate-2026-11-25/PCB(2).zip)（SHA-256は[検査記録](releases/esp32-tdisplay-orderfiles-check-2026-11-25/GERBER_MANIFEST_2026-11-25.json)に記載）。前に受領した `PCB(1).zip` は空であり**使用禁止**。

**ユーザー申告：PCB厚1.2mmで発注済み（2026-11-25）。** 注文番号・メーカー側の受注確定画面は未照合です。KiCad設計ファイルやGerberそのものの厚み設定は変更していません。基板認識寸法はGerberジョブファイル上80.06×100.05mmであり、見積価格・CAM外形・取付穴は注文画面で確認してください。

Git作業ブランチで管理し、`main`へは指示なく統合しません。
