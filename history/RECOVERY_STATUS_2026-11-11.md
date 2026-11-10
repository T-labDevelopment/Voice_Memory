# Original local Git history — restoration status (2026-11-11)

The GitHub branch `fix/v1-cap-min0805-2026-11-10` stores a complete **file snapshot** and a split local-history backup, but does **not** expose the source local commits as the native GitHub commit ancestry.

- Four parts: `VoiceMemory_v1_git.bundle.part01` through `part04` are present in GitHub.
- Source local head noted in prior audit: `c046a9c71d5fb17172cf048e0ef63aef2eb75111`.
- SHA-256 of the original concatenated bundle recorded in `README.md`: `677bc6f9998d67196d175fe80836b7aa592cea07f17e47a3af77cc02e0dca9ff`.
- Attempts to access binary data for local reconstruction were blocked by the available artifact and GitHub read paths (binary blob not decodeable as UTF-8); the concatenated bytes were not available to `git bundle verify` during this audit.
- **Not completed:** new verification of concatenated SHA-256, Git refs/tags inventory, pushing all former commits and tags as GitHub-native history.
- No history rewriting or forced updates were done. Existing bundle parts remain untouched.
- To recover the source history, follow `README.md` to concatenate parts, check SHA-256, run `git bundle verify`, then inspect `git bundle list-heads` in a local environment with bytes available. Do **not** force-push or rewrite main.

This records a real limitation rather than asserting that normal Git history migration is complete.
