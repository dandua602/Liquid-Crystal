# First map ownership inventory — Nexus controllers

Source SHA-256: `c69446ff635eeb69c4285c6b76e99c291fee1dc2e54342040bce37b5cdc7e7cf`.

Ten Nexus controller roots only. Pointer prefixes are physical scan candidates, not native bounds. Layout/event validation applies to selected owners; dummy/bad slots elsewhere are not discarded from the banks. No gameplay reachability or full connectivity claim.

CONFIRMED_IN_ROM: byte/pointer/coordinate values. Structural roles use pinned FireRed field definitions and native lookup evidence. Section labels are not unique room names.

Native lookup signature at 0x55238; group-table literal at 0x5524C → table 0x3526A8.

| Group:map (decimal) | Section label | Header | Layout size | Objects/warps/coords/BG |
|---|---|---|---|---|
| 3:99 | ROUTE 53 | 0xB1E89C | 42×48 | 14/1/0/6 |
| 3:100 | SANDWAY TOWN | 0xB29130 | 100×36 | 17/7/10/8 |
| 3:101 | ROUTE 54 | 0xB30B88 | 68×42 | 9/2/0/4 |
| 3:102 | ROUTE 55 | 0xB4A100 | 42×68 | 12/1/0/4 |
| 3:104 | ROUTE 56 | 0xC0C90C | 68×42 | 12/2/0/4 |
| 3:107 | ROUTE 54 | 0xC24978 | 68×42 | 9/2/0/4 |
| 3:111 | SCIENCE COMPLEX | 0xC313D0 | 42×48 | 14/1/0/6 |
| 5:86 | WEST VALE PORT | 0xB278B8 | 155×20 | 20/40/5/2 |
| 5:102 | NEXUS LABORATORY | 0xC00A6C | 20×15 | 3/1/0/12 |
| 6:23 | MANDARIN CITY | 0xC18AE4 | 20×15 | 3/1/0/12 |

## Background-event owners

| Script | Group:map | BG index | Coordinates | Pointer site |
|---|---|---|---|---|
| 0xAD344E | 5:102 | 11 | 11,1 | 0xC01900 |
| 0xAD344E | 6:23 | 11 | 16,4 | 0xC18E58 |
| 0xAD354B | 3:102 | 2 | 5,49 | 0xC04308 |
| 0xAD3D6E | 3:102 | 3 | 8,54 | 0xC04314 |
| 0xAD3D94 | 3:101 | 3 | 55,9 | 0xC02AAC |
| 0xAD3D94 | 3:104 | 3 | 13,17 | 0xC04600 |
| 0xAD3D94 | 3:107 | 3 | 55,9 | 0xC2611C |
| 0xAD3DBA | 3:101 | 2 | 24,14 | 0xC02AA0 |
| 0xAD3DBA | 3:107 | 2 | 24,14 | 0xC26110 |
| 0xAD3DE0 | 3:100 | 5 | 12,6 | 0xC04B30 |
| 0xAD3E06 | 3:100 | 6 | 38,28 | 0xC04B3C |
| 0xAD3E2C | 3:99 | 4 | 26,17 | 0xC02974 |
| 0xAD3E2C | 3:111 | 4 | 26,17 | 0xC32560 |
| 0xAD3E52 | 3:99 | 5 | 18,24 | 0xC02980 |
| 0xAD3E52 | 3:111 | 5 | 18,24 | 0xC3256C |
| 0xAD3E78 | 5:86 | 0 | 116,14 | 0xC01474 |
| 0xAD3E78 | 5:86 | 1 | 117,14 | 0xC01480 |

## Bounds and remaining work

Group-table and bank starts come from native lookup pointers, not the beginning of a maximal pointer-looking run. Selected bank prefixes stop at non-ROM words. Do not trim banks at a bad intermediate layout or infer counts from numerically adjacent bank pointers. The native lookup itself has no certified bounds check.

All 17 owner records retain script reuse; identical scripts or coordinates do not certify duplicate maps. This first pass exports raw warp and connection records. Run tools/warp_graph.py for separate destination, return-record and default indexed-layout checks; see research/orange_connectivity.md. Gates and runtime reachability remain untested.

The bounded connectivity audit expands the scope to 32 distinct map slots. Continue by cataloging their event and map-entry scripts, retaining candidate aliases and legacy content.
