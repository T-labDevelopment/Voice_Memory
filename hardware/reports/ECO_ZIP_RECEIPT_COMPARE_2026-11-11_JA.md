# VoiceMemory 旧v1リリース版（2026-10-30）— 受領・Git照合記録

- 受領日: 2026-11-11（本チャット）
- 元ファイル名: `VoiceMemory_v1_ECO_2026-10-30_KiCad10(1).zip`
- ファイルサイズ: 134456 bytes
- **元ZIP SHA-256**: `4701e9fb30755c0f9fe3589d3cfbdebf8b4f2a751e774f449c357264064692ce`
- ZIPの展開健全性: `zipfile.testzip() == None`（検査OK）
- ZIP内: 15ファイル、ディレクトリエントリを除く
- 対象GitHub: `T-labDevelopment/Voice_Memory`
- 比較ブランチ: `fix/v1-cap-min0805-2026-11-10`
- 照合時GitHub HEAD: `9655217df6163b9f9dcf9159ef22c5b14afeb534`
- 照合方法: ZIP内の各エントリに対しGitのBlob SHA-1（`git hash-object --stdin`）を算出し、GitHub再帰ツリーにある対応ファイルのBlob SHA-1と比較（Git object内容の一致確認）。
- **判定: 15件中13件は現在GitHubとバイト単位で同一。相違は `.kicad_sch` と `.kicad_pcb` の2件のみ。**

## バージョン区分（2026-11-11ユーザー確定）

- 本ZIPは**旧v1のリリース版**であり、途中のECO作業ファイルという位置付けではない。ファイル名中の `ECO` はこのリリース版の名称の一部として維持する。
- 2026-11-10のコンデンサ見直し版は**後続の現行開発／レビュー版**として区別する。
- リリース基準として、旧v1 ZIPを変更せず保存する。現行SCH/PCBへ置換したり、旧v1を遡って変更することはしない。
- ただし同梱の `RELEASE_CHECKLIST_JA.md` は評価版・製造未承認と明記しており、**「旧v1としてリリースされた」ことは「ERC/DRC済み・製造承認済み」を意味しない**。
- ZIPの原バイト列をGitHubへアップロードできていないため、現状はチェックサムと差分・所在の登録のみ。GitHub側に旧v1の独立した完全スナップショットがあると誤認しないこと。

## 対応表（元ZIP側のGit Blob SHA）

| 元ZIPのパス | 現行リポジトリ格納先 | 元ZIP SHA-1 | 現行GitHubとの一致 |
|---|---|---|---|
| `CHANGELOG_JA.md` | `hardware/reports/ECO_2026-10-30_JA.md` | `3d01aa7aab3efdd1aaee03a9368caff24073c378` | 一致 |
| `ECO_NEW_TRACK_CLEARANCE_2026-10-30.json` | `hardware/reports/ECO_NEW_TRACK_CLEARANCE_2026-10-30.json` | `4f013f66d705763f3dcc9f51d185417ddba8d21d` | 一致 |
| `ECO_PROXIMITY_2026-10-30.json` | `hardware/reports/ECO_PROXIMITY_2026-10-30.json` | `568728d8c367130e9afd13690d624ee2b1cf79a2` | 一致 |
| `ECO_STATIC_CHECK_2026-10-30.json` | `hardware/reports/ECO_STATIC_CHECK_2026-10-30.json` | `cb0645291c3e4e678ab7d6b1749e3b7df511f88e` | 一致 |
| `RELEASE_CHECKLIST_JA.md` | `hardware/reports/ECO_RELEASE_CHECKLIST_2026-10-30_JA.md` | `7c3348ac82a40859dbbe1df2c2d37bf545f06eaa` | 一致 |
| `voicememory/README_ECO_2026-10-30.md` | `hardware/kicad/voicememory/README_ECO_2026-10-30.md` | `1d0df0c924c5c27c8854a8a5401da0675af13b39` | 一致 |
| `voicememory/README_JA.md` | `hardware/kicad/voicememory/README_JA.md` | `ab524d9f1c018886f48b3b68658ed76e2dfd4ec3` | 一致 |
| `voicememory/Voice_Memory.kicad_sym` | `hardware/kicad/voicememory/Voice_Memory.kicad_sym` | `d38f9d96ca4d28daab41a06ad6bf111ac086f62f` | 一致 |
| `voicememory/Voice_Memory.pretty/RJ45_8P8C_THT_15.91x15.10.kicad_mod` | 同名の現行ローカル.pretty | `e1beed3853ac4e4ee1dbef2f68797cdccf3ba65f` | 一致 |
| `voicememory/Voice_Memory.pretty/SW_TVGP01_G73BB_12mm.kicad_mod` | 同名の現行ローカル.pretty | `e55dee6f3a4767a77554ca6a7985a23296c3b7c3` | 一致 |
| `voicememory/fp-lib-table` | `hardware/kicad/voicememory/fp-lib-table` | `214258393e82941d1225cc7ece745e07410248b0` | 一致 |
| `voicememory/sym-lib-table` | `hardware/kicad/voicememory/sym-lib-table` | `ca2b85b3abcf1a36e3cf59cad7fd219e34dec101` | 一致 |
| `voicememory/voicememory.kicad_pro` | `hardware/kicad/voicememory/voicememory.kicad_pro` | `170ea58a31880414d74a9d0d8bd8459d7280034b` | 一致 |
| `voicememory/voicememory.kicad_sch` | `hardware/kicad/voicememory/voicememory.kicad_sch` | `d89d0239feee846daab59fac5c4e6ccccd39f915` | 不一致（現行 `f2c2ad4c95c1bbfe8efd0bdcc41c656cf681282f`） |
| `voicememory/voicememory.kicad_pcb` | `hardware/kicad/voicememory/voicememory.kicad_pcb` | `f2f1f8cd4dcaf055b804fdf0c9a9b5317ccf80ac` | 不一致（現行 `f34114da0dfa6d8d0ee14b56dd1fa90c935d5f08`） |

## 差分の内容（回路図から確認）

10/30受領版の回路図ではC11/C19=1µF/25V・0603、C2/C4=1µF/25V X5R・0805、0.1µF群=50V・0805。現在のGitHub設計ではC11/C19/C2/C4が1µF/25V PMLCAP・1206、該当0.1µF群が100V CH・1206。これは別途記録された11/10の調達・フットプリント変更方針と整合している。

その他、U2=W25Q32RVCSJM、U3=TLP592A(F)、U4=NJM2732D、R20=270Ωおよび部品ライブラリは旧ZIPと現行一致。回路図差分は上記に限定されると**断定はしない**（現行SCHとの全行diffは未実施）。

## 不足資料との関係

- このZIPに図版 `figures/*.png` やユーザー提供RJ45参考画像は**含まれていない**。先の8件の原本画像欠落は解消しない。
- Git bundleや`.git`履歴はZIPに含まれていない。通常GitHub履歴への移植も進まない。
- 本ZIPは2026-10-30の**旧v1リリース版**であり、既存の2026-11-10レビュー用SCH/PCBを上書きしない。
- 今回行ったのは元ZIPのローカル読取り・ハッシュ照合と**本監査テキストのGitHub登録**。ZIP自体のバイナリをこのGitHubブランチへアップロードしたわけではない。
- 旧ZIPはユーザー提供添付として保持されているが、GitHubに同一の元ZIPをアーカイブ登録する工程は**未実施**。元ZIPの保管場所とSHA-256を明示する。
- KiCad正式ERC/DRC、PCBゾーン再フィル、実機検証は実施していない。

## 出典

- 今回アップロードされた `VoiceMemory_v1_ECO_2026-10-30_KiCad10(1).zip` の実バイト列
- GitHubブランチ `fix/v1-cap-min0805-2026-11-10` の再帰ツリー（各Blob SHA）
- `hardware/reports/CAP_MIN_0805_2026-11-10_JA.md`
