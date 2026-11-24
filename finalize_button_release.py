from __future__ import annotations
import csv,json,hashlib,io,zipfile
from pathlib import Path
p=Path(__file__).resolve().parent
bpath=p/'bom_draft.csv'
with bpath.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fn=r.fieldnames;rows=list(r)
byref={x['Ref']:x for x in rows}
# Preserve the previous capacitor selection audit; user did not request any change.
info={
'C11':('Rubycon','25MU105MA23216','秋月電子','107397','https://akizukidenshi.com/catalog/g/g107397/','25V','PMLCAP (polymer-film)','1206 imperial (3216 metric), revised by user request','秋月個別ページで在庫あり、数量は前回確認','3.2x1.6x1.4mm (1206)','±20%','秋月個別ページ確認済','未再取得'),
'C12':('Murata','GRM2195C1H472JA01D','千石電商','EEHD-5PLP','https://www.sengoku.co.jp/mod/sgk_cart/detail.php?code=EEHD-5PLP','50V','C0G','0805 imperial (2012 metric)','個別ページ・価格・購入欄確認。購入可能実数は不明','2.0x1.25x0.85mm','±5%','千石個別商品ページ確認・数量未確認','非公開'),
'C14':('Murata','GRM2191X1A473JA01D','千石電商','商品検索','https://www.sengoku.co.jp/mod/sgk_cart/search.php?cid=4442','10V','SL','0805 imperial (2012 metric)','千石カテゴリー一覧に型番・価格・仕様掲載。商品個別ページと購入可能実数は未取得','2.0x1.25x0.85mm','±5%','千石一覧＋村田2026年メーカー資料','非公開'),
'C15':('Murata','GRM2195C1H103JA01D','千石電商','商品検索','https://www.sengoku.co.jp/mod/sgk_cart/search.php?cid=4442','50V','C0G','0805 imperial (2012 metric)','千石カテゴリー一覧に型番・価格・仕様掲載。商品個別ページと購入可能実数は未取得','2.0x1.25x0.85mm','±5%','千石一覧＋村田メーカー資料','非公開'),
'C16':('Murata','GRM21B5C1H223JA01L','千石電商','EEHD-5S3S','https://www.sengoku.co.jp/mod/sgk_cart/detail.php?code=EEHD-5S3S','50V','C0G','0805 imperial (2012 metric)','個別ページ・価格・購入欄確認。購入可能実数は不明','2.0x1.25x1.25mm','±5%','千石個別商品ページ確認・数量未確認','非公開'),
'C18':('Samsung','CL21A106KOQNNNE','秋月電子','107542','https://akizukidenshi.com/catalog/g/g107542/','16V','X5R','0805 imperial (2012 metric)','個別ページに在庫あり・在庫限り表示。20個入550パック購入可能と表示','2.0x1.2x1.25mm','±10%','秋月個別商品ページで通販購入可能数確認','550パック（20個/パック）'),
'C19':('Rubycon','25MU105MA23216','秋月電子','107397','https://akizukidenshi.com/catalog/g/g107397/','25V','PMLCAP (polymer-film)','1206 imperial (3216 metric), revised by user request','秋月個別ページで在庫あり、数量は前回確認','3.2x1.6x1.4mm (1206)','±20%','秋月個別ページ確認済','未再取得'),
'C21':('Murata','GRM21B1X1A104JA01L','千石電商','EEHD-5PLU','https://www.sengoku.co.jp/mod/sgk_cart/detail.php?code=EEHD-5PLU','10V','SL','0805 imperial (2012 metric)','個別ページ・価格・購入欄確認。購入可能実数は不明','2.0x1.25x1.25mm','±5%','千石個別商品ページ＋村田メーカー資料','非公開'),
'C22':('Murata','GRM21B1X1A104JA01L','千石電商','EEHD-5PLU','https://www.sengoku.co.jp/mod/sgk_cart/detail.php?code=EEHD-5PLU','10V','SL','0805 imperial (2012 metric)','個別ページ・価格・購入欄確認。購入可能実数は不明','2.0x1.25x1.25mm','±5%','千石個別商品ページ＋村田メーカー資料','非公開'),
'C23':('Rubycon','16PX100MEFC5X11','秋月電子','110271','https://akizukidenshi.com/catalog/g/g110271/','16V','電解（有極性）','THT 5mm diameter 2.00mm pitch','個別ページで在庫僅少・通販購入可能数5510個と表示','直径5mm/高さ11mm/2mmピッチ','±20%','秋月個別商品ページで通販購入可能数確認','5510個（在庫僅少表示）'),
'C20':('Samsung','CL21A106KOQNNNE','秋月電子','107542','https://akizukidenshi.com/catalog/g/g107542/','16V','X5R','0805 imperial (2012 metric)','個別ページに在庫あり・在庫限り表示。20個入550パック購入可能と表示','2.0x1.2x1.25mm','±10%','秋月個別商品ページで通販購入可能数確認','550パック（20個/パック）')
}
keys=['Manufacturer','MPN','Supplier','SupplierCode','SupplierURL','RatedVoltage','Dielectric','SizeRule','ListingStatus','BodyDimensions','CapacitanceTolerance','SupplyVerification','StockQuantityDisplayed']
for ref,v in info.items():
 row=byref[ref]
 for k,val in zip(keys,v):row[k]=val
 row['InventoryCheckedOn']='2026-11-23';row['SupplierPageCheckedOn']='2026-11-23'
 row['Status']='LISTED_ONLY_CONFIRM_CART_BEFORE_ORDER' if ref in ('C14','C15') else 'PART_SOURCED_STOCK_RECHECK_AT_ORDER'
for k in ('R23','R24','R25','R26'):byref[k]['Status']='ADDED_0805_PULLUP'
with bpath.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fn,lineterminator='\n');w.writeheader();w.writerows(rows)

# Existing 45-part placement table; add new parts and record relocated switch.
origin=list(csv.DictReader((p/'PCB_PLACEMENT_JA.csv').open(encoding='utf-8-sig',newline='')))
assert len(origin)==45
for row in origin:
 if row['Reference']=='SW1':
  row.update({'Footprint':'VoiceMemory_TDisplay:SW_PUSH-12mm','X_mm':'71.26','Y_mm':'102','Angle_deg':'0','Placement':'Operator control left of TDisplay','Notes':'REC 12mm, active-low, confirm switch type/height'})
more=[
('SW2','CH1',61.76,67.0),('SW3','CH2',80.76,67.0),
('SW4','CH3',61.76,84.5),('SW5','CH4',80.76,84.5),
('R23','CH1 pullup',109.9,87.7),('R24','CH2 pullup',106.0,93.0),
('R25','CH3 pullup',109.9,93.0),('R26','CH4 pullup',106.0,98.3)
]
for ref,name,x,y in more:
 btn=ref.startswith('SW')
 row={k:'' for k in origin[0]}
 row.update({'Reference':ref,'Footprint':('VoiceMemory_TDisplay:SW_PUSH-12mm' if btn else 'Resistor_SMD:R_0805_2012Metric'),
    'X_mm':f'{x:g}','Y_mm':f'{y:g}','Angle_deg':('0' if btn else '90'),
    'Side':'F.Cu','Placement':('Operator control left of TDisplay' if btn else 'Under module'),
    'Notes':name+('; matching switch model drill/pads unconfirmed' if btn else '; 10k, external 3V3 pullup')})
 origin.append(row)
assert len(origin)==53
with (p/'PCB_PLACEMENT_JA.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=origin[0].keys(),lineterminator='\n');w.writeheader();w.writerows(origin)

note='''# VoiceMemory T-Display ESP32 Rev.A — 12mm角5ボタン追加・PCB配置記録

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
'''
(p/'BUTTON_CONTROL_SPEC_JA.md').write_text(note,encoding='utf-8')
# Retain previous note for traceability but link updated design.
original=(p/'PCB_LAYOUT_NOTE_JA.md').read_text()
original='> **改訂情報:** 旧45部品配置案の履歴。5ボタン追加後の現行正本は [BUTTON_CONTROL_SPEC_JA.md](BUTTON_CONTROL_SPEC_JA.md)。\n\n'+original
(p/'PCB_LAYOUT_NOTE_JA.md').write_text(original,encoding='utf-8')
# All data needed to reopen project as a directory.
zipname='/mnt/data/VoiceMemory_TDisplay_RevA_5x12mm_buttons_2026-11-24.zip'
paths=[
'VoiceMemory_TDisplay.kicad_pcb','VoiceMemory_TDisplay.kicad_sch','VoiceMemory_TDisplay.kicad_pro',
'VoiceMemory_TDisplay.kicad_sym','Voice_Memory.kicad_sym','fp-lib-table','sym-lib-table',
'VoiceMemory_TDisplay.pretty/Relay_Zettler_AZ8462_DIP8.kicad_mod',
'VoiceMemory_TDisplay.pretty/SOIC-8_5.23x5.23mm_P1.27mm.kicad_mod',
'VoiceMemory_TDisplay.pretty/TTGO-T-Display.kicad_mod',
'VoiceMemory_TDisplay.pretty/SW_PUSH-12mm.kicad_mod',
'Voice_Memory.pretty/RJ45_8P8C_THT_15.91x15.10.kicad_mod',
'pinmap.csv','bom_draft.csv','PCB_LAYOUT_NOTE_JA.md','PCB_PLACEMENT_JA.csv',
'BUTTON_CONTROL_SPEC_JA.md','PCB_BUTTONS_JA.csv','button_validation.json',
'add_12mm_switches.py','validate_buttons.py','finalize_button_release.py'
]
for x in paths:assert (p/x).is_file(),x
with zipfile.ZipFile(zipname,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 for x in paths:z.write(p/x,arcname=x)
with zipfile.ZipFile(zipname) as z:
 bad=z.testzip();assert not bad,bad
 print('ZIP',zipname,'bytes',Path(zipname).stat().st_size,'entries',len(z.namelist()))
 print('SHA256',hashlib.sha256(Path(zipname).read_bytes()).hexdigest())
