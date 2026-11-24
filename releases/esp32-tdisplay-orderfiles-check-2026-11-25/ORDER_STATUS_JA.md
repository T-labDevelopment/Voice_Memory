# ESP32 T-Display Rev.A — 2026-11-25 発注データ点検

- **状態：発注用Gerber ZIPが空のため、発注準備は未完了。注文実行は確認できない。**
- 主開発対象：ESP32 16MB T-Display版。従来CH32V003版・2026-11-24の発注済みPrototype旧版は変更しない。
- 受領した設計正本：`VoiceMemory_TDisplay-2026-11-25_003943.zip`（内部の `.kicad_prl` はGitに展開しないがZIP原本は保持）
- 発注用として受領した `PCB(1).zip` は **162バイト**。ZIP内には空の `PCB/` ディレクトリエントリ1件だけで、Gerber・Excellonドリルファイルが **0件**。
- 基板外形：Edge.CutsのXY範囲 X=65.151..145.161、Y=34.780..134.780mm、約80.01×100.00mm。
- 設計：KiCad 10 PCB。2層（F.Cu/B.Cu）、板厚設定1.6mm、部品52個、表面/裏面GNDゾーン2個。
- MOD1（24pin）/SW1..SW6のPad-Net対応を簡易静的検査。GPIO割当の前回版からの機能変更なし。
- 今回のZIPには新しいERC/DRC実行レポートが含まれていないため、この版のERC/DRC 0件を独立には確認していない。
- 前回のGerberは別の改訂版であり、本版の製造には流用不可。
- **必要な作業：** 最新KiCad PCBでゾーン再充填→DRC→Gerber（F.Cu/B.Cu、F.Mask/B.Mask、F.SilkS/B.SilkS、Edge.Cuts）およびPTH/NPTHドリルを出力し、ファイル一式をZIPに収め、JLCPCBで表示寸法・穴・シルク・層構成を確認する。
- **今回の登録は発注データの準備状況を保存する作業ブランチであり、出荷/製造承認や発注完了を意味しない。**
