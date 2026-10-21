# Where to find the project on GitHub

Repository: https://github.com/dandua602/Liquid-Crystal

- **Current-player safety fix:** [P002a-safety-fix.zip](patches/P002a/P002a-safety-fix.zip)
  blocks the old warehouse stair into the broken link stadium. Use a fresh current
  save backup with its offline tool to keep your earned progress. It stops if
  your newest save is inside the stadium or has invalid data.
- **Start here:** the repository's [README](README.md).
- **Play instructions:** [WALKTHROUGH.md](WALKTHROUGH.md), including screenshots,
  the Route59 map, puzzle, battle, Office entry/return and saving.
- **Download the current patch:** [P002-prototype.zip](patches/P002/P002-prototype.zip).
  Open that file and choose **Download raw file**, or use its download button.
- **Direct requested test save:** [P002-warehouse-test.sav](downloads/P002-warehouse-test.sav)
  (Download raw file). This generated128 KiB fixture matches the embedded test
  save; it is not a verified repair for the hardware Saving hang.
- **Easy warehouse test download:** [P002-easy-cartridge-test-v3.zip](patches/P002/P002-easy-cartridge-test-v3.zip).
  Choose Download raw file, extract, open Make-Test-ROM.html, select your original
  Liquid Crystal ROM, then click Create and download test ROM. No Python needed.
  It creates the tested warehouse image with test progress embedded, entirely offline.
  V3 also offers the matching raw save download; hardware saving is currently
  failing as reported, so this is a diagnostic copy, not a promised fix.
  The browser also accepts exact P001/P002. A changed-save cart dump needs the original
  five-badge save backup; unsupported code changes show size/hash diagnostics.
- **Real cartridge testing:** [HARDWARE_TEST.md](HARDWARE_TEST.md) and
  [P002-cartridge-tools.zip](patches/P002/P002-cartridge-tools.zip). The helper kit
  has patches/scripts/guides only; private ROM/save images are in the cloud
  workspace at `builds/P002-cartridge-test.zip`. Workspace file links are not
  downloadable in this chat; use the easy offline patcher above to create the
  warehouse image locally instead.
- **Patch instructions:** [P002-README.txt](patches/P002/P002-README.txt).
- **Progress and next work:** [PROJECT_STATE.md](PROJECT_STATE.md) and
  [remaining work](research/remaining_work.md).
- **Tools/tests:** [tools](tools/) and [tests](tests/).
- **Original project request:** [PROJECT_BRIEF.md](PROJECT_BRIEF.md).

The patch ZIP includes P001's warehouse content and P002's Office service room,
plus a standalone patch, a P001 upgrade patch, both rollback directions and the
walkthrough. It does not contain a game ROM or save file. Use your own exact
source ROM and a copy of your personal save as described in the patch README.

## GitHub and cloud publishing are separate

Publishing the cloud environment saves its prepared filesystem/configuration for
future cloud work. It does not create Git commits or push files to GitHub.
GitHub receives work only when it is committed and pushed.

The user has now requested GitHub synchronization. Continue committing and
pushing meaningful tested project checkpoints to main, including code, research,
walkthrough updates and versioned patch-only downloads. Verify the remote after
each push. Never force-push or overwrite someone else's work; reconcile new
remote commits normally. Preserve existing changes and original source files.

Source `.gba` ROMs, personal/source `.sav` files and ignored local builds remain
outside Git. After explicitly asking for a direct save download, the user has
one generated test fixture at `downloads/P002-warehouse-test.sav`. This narrow
artifact exception does not authorize uploading other saves or any game ROM.
The small patch-only deliverable is copied into `patches/P002/` so it is visible
and downloadable on GitHub. A GitHub clone does not include the user's ROM/save
inputs; reproducing builds/tests still requires those exact local files.
