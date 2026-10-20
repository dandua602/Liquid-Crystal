# Where to find the project on GitHub

Repository: https://github.com/dandua602/Liquid-Crystal

- **Start here:** the repository's [README](README.md).
- **Play instructions:** [WALKTHROUGH.md](WALKTHROUGH.md), including screenshots,
  the Route59 map, puzzle, battle, Office entry/return and saving.
- **Download the current patch:** [P002-prototype.zip](patches/P002/P002-prototype.zip).
  Open that file and choose **Download raw file**, or use its download button.
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

Source `.gba` ROMs, `.sav` files and ignored local builds remain outside Git.
The small patch-only deliverable is copied into `patches/P002/` so it is visible
and downloadable on GitHub. A GitHub clone does not include the user's ROM/save
inputs; reproducing builds/tests still requires those exact local files.
