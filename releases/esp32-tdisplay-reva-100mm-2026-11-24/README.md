# ESP32 T-Display Rev.A — 100mm外形設計案

**状態：未発注／KiCad正式DRC未実施。** 104.3mm版のPrototypeが既に発注済みであり、本100mm版は製造費の低減を狙う後続設計です。

- 基準：16:45発注用正本 `VoiceMemory_TDisplay-2026-11-24_164508.zip`（SHA-256: `f81d32c1ff5159133aed2fd2ecadfa6d76ce97ed69fa2263f3d4d98e78146a19`）。発注用`PCB.zip`は旧基板用であり、変更せず保管。
- 修正：下端を4.3mm詰めて64.4×100.0mm、SW4/5・M4下2箇所・シルクCH3/4・該当配線を変更。GND via2箇所移動。
- [100mm版KiCad編集データ](../../hardware/kicad/voicememory_tdisplay/revA_100mm_2026-11-24/)
- [100mm版ZIP](../../hardware/source-archives/tdisplay-reva-100mm-2026-11-24/VoiceMemory_TDisplay_RevA_100mm_2026-11-24.zip)
- [変更詳細](../../hardware/kicad/voicememory_tdisplay/revA_100mm_2026-11-24/README_100MM_JA.md)
- 旧発注版の記録：[104.3mm Prototype](../esp32-tdisplay-prototype-ordered-2026-11-24/README.md)。**歴史を上書きしない。**
- 製造前：KiCadでGNDゾーンを再塗りつぶし、ERC/DRCを再チェックし、Gerber/Drillを新規生成。静的な近傍異ネット間クリアランス簡易評価のみ実施済み。
