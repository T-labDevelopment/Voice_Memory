# VoiceMemory v3 T-Display ESP32 / Simplified Schematic Draft

> **Full capacitor recheck (2026-11-23):** The nine parts other than 1µF were reviewed for dimensions, capacitance, voltage rating, dielectric and shopping evidence; schematic instance metadata and BOM were updated. C14/C21/C22 are SL dielectric, not X7R. Akizuki 10µF 0805 shows 550 purchasable 20-piece packs; Rubycon 100µF THT shows "low stock" while 5510 units are listed as purchasable. Sengoku offers product/order listings but does not disclose confirmed purchasable piece counts. No electrical values, nets or footprints were changed. See [CAPACITOR_SIZE_AUDIT_JA.md](CAPACITOR_SIZE_AUDIT_JA.md).

## Capacitor sizing and sourcing (2026-11-23)

**C11 and C19 (1µF)** are now **1206 imperial / 3216 metric**, using Rubycon 25MU105MA23216 PMLCAP (1µF/25V; Akizuki 107397). The remaining eight SMD capacitors are 0805 imperial / 2012 metric, the permitted minimum. Akizuki's former 0805 1µF stock (107549) was also independently confirmed in stock, so this enlargement was a requested design choice, not proof of 0805 unavailability. The polarized THT C23 remains Rubycon 100µF/16V (Akizuki 110271) with the 5mm diameter, 2.0mm lead pitch footprint. Part MPNs and vendors are synchronized between schematic instance properties and BOM. See [CAPACITOR_SIZE_AUDIT_JA.md](CAPACITOR_SIZE_AUDIT_JA.md). KiCad ERC/DRC and bench tests remain pending.


> **First editable KiCad Rev.A handoff:** [INITIAL_DESIGN_HANDOFF_JA.md](INITIAL_DESIGN_HANDOFF_JA.md). The 24-pad T-Display header numbering and dedicated AZ8462 DIP relay footprint have been corrected for this branch. Official ERC/DRC and bench checks remain unrun.

> **Project boundary:** This is an independent **VoiceMemory_TDisplay_ESP32 Rev.A** design, NOT a revision of the CH32V003 prototype. Retain AZ8462-3 mechanical DPDT relay; do not adopt the PhotoMOS-only comparison design. See [PROJECT_SCOPE_JA.md](PROJECT_SCOPE_JA.md). Previous v1/v2 firmware, PCB validation and manufacturing approval do not carry over. The project is currently isolated by a Git branch and dedicated directory, not yet a distinct GitHub repository.

**Status: schematic design DRAFT, no native KiCad ERC/DRC execution, no PCB production approval.**
**2026-11-22 | Source: approved VoiceMemory v2 on `develop/v2` (SHA `d69a0664f0994633a5732053ea11fa3172edfa56`).**
This v3 project is independent. **Do not alter the approved v2 files or its source ZIP.**

## Design intent
- Keep four memory channels M1..M4, microphone-PTT-controlled recording, variable recording length capped at 120s, single and looped playback, automatic PTT, default pass-through and protection from accidental TX during recording.
- T-Display classical ESP32 (NOT T-Display S3). Integrated ST7789 display and two buttons GPIO0 / GPIO35. Optional external REC ARM switch SW1.
- 8kHz / unsigned 8-bit / mono PCM. External W25Q32RVCSJM 32Mbit (4MiB) standard SPI, 4x120s raw PCM requires 3,840,000 bytes plus metadata. Internal 4MB module Flash cannot simultaneously guarantee this capacity and firmware.
- GPIO32 ADC1 with MCP6002 audio front-end; GPIO25 ESP32 DAC1 plus 2-pole RC low-pass and MCP6002 follower. No PWM audio output circuitry.
- Power and firmware via the T-Display onboard USB-C or its documented 1S LiPo input. **Never connect AA3 battery to the T-Display 1S LiPo input.** Analog and relay circuitry powered from board `+3V3`, current limit / LDO temp / battery droop must be assessed.

## Project files
- `VoiceMemory_TDisplay.kicad_sch`: fully editable KiCad 10 draft schematic. Standard Device/Connector/Switch/Transistor/MCP6002 cache entries copied **unchanged from the approved v2 KiCad schematic**. Original v2 exact custom Flash/Relay/TLP/Diode/trim symbol entries are reused. Each electrical pin is connected at its endpoint by an explicit **global label** or is marked no-connect, on a 50mil grid. A standard-library **PWR_FLAG on GND_AUD** identifies the external common ground as an ERC power source; MOD1 +3V3 is modeled as power_out.
- `VoiceMemory_TDisplay.kicad_sym`: board module symbol newly authored for this branch only.
- `Voice_Memory.kicad_sym`: full, unmodified v2 **custom project symbol library**, not a substitute for official KiCad standard libraries.
- `Voice_Memory.pretty/RJ45_8P8C_THT_15.91x15.10.kicad_mod`: copied v2 legacy RJ45 footprint; mechanical and purchased connector fit verification needed.
- `pinmap.csv`, `bom_draft.csv`: editable pin map and **45 unique-reference component** draft register (MCP6002 U4 has three schematic units but one physical component).

## Connections and safety
| Function | ESP32 GPIO | External part or net |
|---|---:|---|
| FLASH_MOSI | 21 | U2 pin5 |
| FLASH_SCK | 22 | U2 pin6 |
| FLASH_CS | 17 | U2 pin1, 10k pull-up |
| FLASH_MISO | 27 | U2 pin2 |
| AUDIO_ADC | 32 | U4A output via R8 1k, C14 47nF to VREF |
| AUDIO_DAC | 25 | GPIO25 DAC1, R20/C15 and R21/C16 low-pass |
| RELAY_EN | 33 | Q1 via 820ohm R11, 100k pulldown |
| AUTO_PTT_EN | 26 | U3 LED via 330ohm R13, 100k pulldown |
| PTT_SENSE_HIGH | 39 | Q2 collector via 10k to 3V3; **HIGH = manual PTT pressed** |
| SW_REC_N | 13 | Optional switch SW1 to ground + 10k pull-up |
| Display | 4,5,16,18,19,23 | onboard only |
| UI buttons | 0,35 | onboard; GPIO0 is BOOT strap, do not hold during boot |
| Not used | 2,12,15,36,37,38 | no-connect by design; avoid risky strapping pins |

- K1 normally closed (unpowered): MIC_AUDIO -> RIG_AUDIO, MIC_PTT -> RIG_PTT.
- K1 energized: RIG_AUDIO -> PLAY_OUT (which is AC coupled), RIG_PTT manual path disconnected; B_NO open.
- During RECORD: K1 ON, PhotoMOS OFF, ADC ON. RECORD only while microphone PTT is pressed; release finalizes recording.
- During PLAY: K1 ON, PhotoMOS ON only during actual send. Between loop repetitions PhotoMOS MUST drop out for a nonzero configurable pause.
- On stop/error: first PhotoMOS OFF, then DAC mute, then K1 release. Do not release K1 during recording until mic PTT has been released if power remains available.
- Q2 is NPN sensing `MIC_PTT` via 47k resistor instead of feeding radio-side voltage into ESP32 directly. It assumes MIC_PTT pulls to PTT_GND when pressed; verify per radio.
- R18=0ohm links PTT_GND and GND_AUD for this **common-ground provisional** architecture; assess radio cables and common grounding before hookup. This is a change from legacy R16=22k reference.
- **Mic bias caveat:** some electret microphones receive DC supply on the audio lead, not on `MIC_DC_PASS`. When K1 breaks MIC_AUDIO/RIG_AUDIO during recording, these microphones can lose bias. The baseline assumes independently biased microphones or a manufacturer-specific adapter; add explicit DC mic-bias supply only after radio/mic electrical measurement. No universal bias compatibility is claimed.
- `+3V3` on MOD1 is a 3V3 source and power_out in the module symbol; validate actual regulator budget under relay coil 46.7mA and ESP32 load, particularly during Wi-Fi use. No required PWR_FLAG on this net while it is typed as a power source.
- U2 W25Q32RVCSJM is 208mil SOP-8, **not** interchangeable with 150mil SOP8 without land pattern change.
- U3 TLP592A uses LED pins 1/2 and dry-contact pins 4/6; pins 3/5 marked NC per legacy v2 library.
- **D1 flyback**: diode pin1 (K) to `+3V3`, pin2 (A) to `RELAY_COIL_LOW`. Logical polarity statically checked. Physical device and K1 footprint pinout still require validation.

## Firmware proposal
- Use on-board button GPIO35 short press to cycle M1..M4; onboard GPIO0 short press play/stop; long press toggles loop. SW1 arms recording, and physical microphone PTT controls record time. The UI is a proposal, firmware not implemented by this schematic.
- Sample 8kHz mono; use DMA / buffered ADC and DAC where supported by the chosen stable ESP32 Arduino Core or ESP-IDF; do not couple audio sample timing to TFT redraws. ADC1 chosen because ADC2 conflicts with Wi-Fi; RF noises remain a test issue.
- Flash sector layout: 64KiB metadata/reserved plus four slots of 1,032,192 bytes each, raw max record length 960,000 bytes per slot, remainder free. Mark validity only after PTT release and completed metadata commit. Implement erase-before-write and power-loss recovery.
- Boot GPIO26 AUTO_PTT_EN LOW, GPIO33 RELAY_EN LOW, GPIO17 FLASH_CS HIGH before other tasks; default no continuous transmit.

## Required verification (NOT DONE)
1. KiCad 10.0 stable open, official ERC report; target 0 errors / 0 warnings.
2. Check all schematic global-label positions/directions, relay diode pins, 2SC1815 ECB physical lead ordering, PhotoMOS exact output pins.
3. Check source regulator +3V3 during worst-case ESP32, TFT, Flash programming and 3V coil load.
4. Confirm recording microphone bias under K1 energized and radio-specific RJ45 adapter mapping, especially common PTT ground.
5. Bench simulate PTT loads before actual transceiver.
6. No PCB / manufacturing approval derived from this document.

## Sources
- Existing approved v2 KiCad: `hardware/kicad/voicememory/` in `develop/v2`; original approval: `releases/v2-manufacturing-approved-2026-11-11/README.md`.
- LILYGO T-Display: https://wiki.lilygo.cc/products/t-display-series/t-display/
- Espressif ESP32 DAC: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/dac.html
- Winbond W25Q32RVCSJM: https://www.winbond.com/hq/product/code-storage-flash/qspi-nor/w25q-rv/?__locale=en&partNo=W25Q32RVCSJM
- Toshiba TLP592A: https://toshiba.semicon-storage.com/info/TLP592A_datasheet_ja_20190624.pdf?did=17082&prodName=TLP592A
- AZ8462-3 coil 46.7mA: https://www.digikey.jp/en/products/detail/american-zettler/AZ8462-3/18340735

## All indicators consolidated to onboard TFT

**Requirement:** Every user-facing status indicator is rendered exclusively on the built-in 240×135 ST7789 TFT of the classic LILYGO T-Display. Status includes M1–M4 selection, REC/PLAY, loop, elapsed time, message saved, auto/manual PTT request, warnings and detected errors. No separate status LED, display module, 7-segment module, display driver or indicator GPIO is added.

The internal LED of TLP592A (U3, net `PTT_LED_A`) is a PhotoMOS control element—not a visible indicator. D1 is the relay flyback diode. Keep both. Preserve AZ8462-3 (K1) mechanical relay and the existing control wiring.

For screen-state requirements and priorities, see [TFT_DISPLAY_SPEC_JA.md](TFT_DISPLAY_SPEC_JA.md). TFT state indications are software commands, not verified RF transmission or relay physical feedback; the display is unavailable when the module is powered off. The hardware remains untested.

