# Voice_Memory — ESP32 T-Display版を主開発

**今後の主開発対象はESP32 T-Display（16MB Flash）版です。**

- **現在の外形短縮案（100.0mm、未発注）：** [Rev.A 100mm版](releases/esp32-tdisplay-reva-100mm-2026-11-24/README.md)
- **既発注のPrototype（104.3mm）：** [発注時の正本とGerber](releases/esp32-tdisplay-prototype-ordered-2026-11-24/README.md)
- **発注前の16:11設計基準：** [初期Rev.A検証基準](releases/esp32-tdisplay-reva-2026-11-24/README.md)
- **旧CH32V003版：** v1/v2の設計・製造履歴として保全する。ESP32側の変更では旧版を変更しない。

100mm版はGNDゾーン再充填・KiCad 10 DRC再実行・Gerber再生成が必要な設計変更案です。旧発注Gerberは使用できません。`main`は変更せず、作業ブランチで管理します。
