# Unity WebGL Game (Working Title)

A first-person exploration game across five surreal spaces, with environmental puzzles and two endings.

The title is temporary. This repository contains release/deployment files only; it does not contain the Unity source project or raw asset packs.

## Play

The GitHub Pages site is published by the **Deploy tested WebGL release** workflow after a tested release archive has been uploaded.

Designed for desktop browsers with a keyboard and mouse. The initial download is approximately **667 MiB**; allow time for downloading and unpacking.

- **WASD** — move
- **Mouse** — look
- **E** — interact / read
- **F** — place a carried crystal
- **Esc** — close a panel / release the mouse
- Use the page's **Fullscreen** button when supported.

Click **Load game**, wait for the progress indicator, then click inside the game to capture the mouse.

## Release deployment

1. Keep the complete tested Unity Web output together, including `Build`, `StreamingAssets`, and `TemplateData`.
2. Preserve Gzip + Decompression Fallback and all matching loader/data/framework/Wasm files. Do not mix files from different builds.
3. Package the publish-ready site as a ZIP with `index.html` at its root. The archive must include `release-manifest.json` with each file's size and SHA-256.
4. Upload the archive as a **GitHub Release asset**, not a Git commit or LFS pointer.
5. Update `release.json` with the fixed release tag, asset name and archive SHA-256; commit only these small release/deployment files.
6. Run **Deploy tested WebGL release** from the Actions tab. The workflow verifies the archive and site hashes, uploads an official Pages artifact, and deploys it.

`release.json` deliberately pins a specific version instead of following `latest`. To roll back, restore a previously tested release configuration and run the workflow again.

No changes to Unity scenes, models, input code or graphics settings are made by this repository. The tested Web-only mouse-delta fix is included in the binary release. Camera diagnostics are hidden/off by default on the public page; the fix remains active.

For updates, `python scripts/package-site.py --build <tested-site-folder> --output <new-archive.zip> --tag <new-fixed-tag>` applies the same small web template and refreshes `release.json`. Upload the new archive, commit the changed config, and run the workflow.
