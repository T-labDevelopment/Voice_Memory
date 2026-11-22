# VoiceMemory v3: no mechanical relay (AQY412S NC PhotoMOS)

**DRAFT / KiCad 10 editable schematic. Native ERC/DRC, PCB and actual radio tests NOT done.** Preserves original v2 and the first mechanical-relay v3 unchanged.

- K1 AZ8462-3, coil driver Q1, D1 flyback and SW1 external REC button removed.
- U5/U6 AQY412S are 60V 500mA **1b normally closed** PhotoMOS. Pins: 1 LED anode, 2 LED cathode, 3/4 isolated NC output. LEDs at GPIO HIGH through 330ohm; 100k pulldowns for reset. GPIO13= AUDIO_ISO_EN controlling U5; GPIO33=PTT_ISO_EN controlling U6. Existing U3 TLP592A remains for auto PTT.
- OFF/unpowered: U5/U6 NC, microphone audio and manual PTT pass-through (hardware function, still must verify assembled board).
- RECORD: U6 LED ON -> manual PTT disconnected; U5 LED OFF -> MIC_AUDIO remains connected to RIG_AUDIO for radio microphone bias. U3 OFF. VOX **MUST BE DISABLED**: recording audio remains connected and can trigger VOX.
- PLAY: U5/U6 LEDs ON -> MIC and manual PTT disconnected; U3 ON for the actual message, OFF between loops.
- R22 revised to send DAC output through its 1k resistor to RIG_AUDIO. Playback source must be DC-silent when idle and power-on transient tested.
- R11=330ohm from GPIO33 to U6 LED A; R12=100k pulldown. R19=330ohm GPIO13 to U5 LED A; new R24=100k pulldown.
- Firmware use T-Display built-in 2 buttons for REC selection/play and loop; GPIO13 freed by deleting SW1.
- No relay coil supply, no flyback diode. Mechanical contact no longer exists. U5/U6 and U3 are still optical MOS **solid-state relays** (PhotoMOS), not entirely switch-free.
- Manufacturer recommended AQY412S input current 5–30mA, 330Ω yields ~6mA at 3V3. Ron typical 1Ω, max 2.5Ω. Output pins 3/4 independent of polarity.
- AQY412S 4-pin symbol created for this project; footprint is KiCad standard `Package_SO:SO-4_4.4x4.3mm_P2.54mm`. Check actual mechanical pads before PCB.
- Every pin via global labels or no-connect. All label nets have ≥2 instances in static check. Power flag retained from old draft.
- Do not treat this schematic as ERC or manufacturing certified. Check T-Display V1 header, mic bias voltages, PTT sense, relay leakage, VOX risk, output levels and power budget before building.
- Price: Panasonic AQY412S two units can exceed old mechanical relay cost substantially; Marutsu has ¥543 and ~¥1330/pc listings. Check availability at order.

Sources: Panasonic https://industry.panasonic.com/ap/en/products/control/relay/photomos/number/aqy412s
Panasonic datasheet https://docs.rs-online.com/f200/0900766b813ec2cd.pdf
KiCad standard footprint https://kicad.github.io/footprints/Package_SO
Seller https://www.marutsu.co.jp/pc/i/11479275/
