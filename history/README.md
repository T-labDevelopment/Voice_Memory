# VoiceMemory v1 original Git history backup

このディレクトリには、ローカルで作成された VoiceMemory v1 の**元のGit履歴とタグ**を収めたGit bundleを、GitHubアップロード用に4分割して格納しています。

- 分割ファイル: `VoiceMemory_v1_git.bundle.part01` ～ `part04`（番号順に連結）
- 元のバンドルファイル名: `VoiceMemory_v1_Cap_Min0805_Review_2026-11-10_git.bundle`
- 元バンドルのSHA-256: `677bc6f9998d67196d175fe80836b7aa592cea07f17e47a3af77cc02e0dca9ff`
- 元の最終コミット: `c046a9c71d5fb17172cf048e0ef63aef2eb75111`

## 復元（Linux/macOS/Git Bash）

```bash
cat VoiceMemory_v1_git.bundle.part0{1,2,3,4} > VoiceMemory_v1_history.bundle
sha256sum VoiceMemory_v1_history.bundle
git bundle verify VoiceMemory_v1_history.bundle
```

## 復元（Windows PowerShell）

```powershell
$parts = 1..4 | ForEach-Object { "VoiceMemory_v1_git.bundle.part{0:D2}" -f $_ }
$out = [System.IO.File]::Create("VoiceMemory_v1_history.bundle")
try {
  foreach ($part in $parts) {
    $inputFile = [System.IO.File]::OpenRead($part)
    try { $inputFile.CopyTo($out) } finally { $inputFile.Dispose() }
  }
} finally { $out.Dispose() }
Get-FileHash .\VoiceMemory_v1_history.bundle -Algorithm SHA256
git bundle verify .\VoiceMemory_v1_history.bundle
```

## 注意

このGitHub作業ブランチは**最新ファイルを1コミットで移したスナップショット**です。ローカルで作成された元のコミットSHAとタグをGitHub上の履歴として移植したわけではありません。元のGit履歴はこのbundleから復元できます。

当該設計はPCBレビュー段階です。コンデンサ大型化による干渉候補が残り、KiCad 10の正式ERC/DRCとゾーン再フィルは未実施です。製造承認済みではありません。
