# Orange entry: authorization, first train trip and Valencia arrival

The controlled first-entry replay reaches Valencia Port through the game's existing quest events: Oak authorizes travel, the office stamps the ticket, the gate admits the player, the Undersea Express stops, the player helps Jin with Kyogre, and an electric Pokémon restarts the train. All 18 runtime expectations pass. No source ROM/save was changed.

This resolves the entry transport path from an explicit eligibility fixture. It does not certify an uninterrupted Johto/Kanto playthrough, every timetable/return-trip branch or real hardware. The initial fixture enables Oak's preceding-story flag `0x1701`, clears later authorization/boarding/completion flags and clears the supplied save's already-set encounter flag `0x9B`. Four initial map placements cover the negative office test, Oak, the office and the gate. All transitions after the gate use ordinary events/buttons.

The first party member has the previously documented level/stats/moves fixture for battles and Surf. Slot 6 is replaced on a disposable copy with a level-70 Ampharos, created by the ordinary `givemon` command; no enemy HP, battle result or quest completion is injected. The non-electric test selects Alakazam and is rejected; the positive test selects Ampharos through the real party menu.

| Stage | Owner / script | Result |
|---|---|---|
| Office before Oak | `2:123`, object 5, root `0x9CEE61` | No stamp without flag `0x1702` |
| Oak's Orange request | `4:88`, object 1, root `0x9D609D`; branch `0x901148` | Existing dialogue about Ivy/Orange travel; sets `0x1702` |
| Ticket stamp | Office root → `0x92E17F` | Existing animation/dialogue sets `0x1778`; repeat preserves stamp |
| Gate | `2:121`, coordinate `(4,12)`, root `0x93C15C` | First-trip branch admits stamped player and sets `0x1873`; game warp reaches `3:40` |
| Platform approach | Normal walk through outdoor warp `(64,48)` | Enters `2:124` |
| Boarding | Object at `(12,8)`, root `0x9564BA`; special `0x8E` | Enters interruption carriage `2:125`, rather than immediately arriving at Valencia |
| Help officer/Jin | Carriage officer at `(24,11)`, root `0x9318CC` | Existing dialogue and game warp open engine area `2:126` |
| Kyogre | Coordinate `(29,7)`, root `0x93E97C` | Actual level-70 legendary encounter executes; `0x9B` becomes set |
| Engine, non-electric | BG `(17,6)`, root `0x932498` | Actual party selection rejects Alakazam; trip flag `0x1779` stays clear |
| Engine, electric | Same BG and actual Ampharos selection | Existing restart/Jin sequence sets `0x1779`; game warp reaches station `1:53` |
| Valencia arrival | Station frame script `0x938D54` | `0x5301=1`; normal station exit `(20,9)` reaches Valencia Port `3:77` |

Oak's dialogue suggests a Sea Pass, but the exercised office/gate scripts use the authorization/stamp flags above. No new item or travel rule was invented to make this trip work. The first gate visit has an explicit one-time boarding branch; later visits involve RTC-derived scheduling and remain a separate test target.

The static companion exports all event/map-script owners and bounded traces for ten entry/transport maps: 93 roots, 2,111 unique instruction candidates and 166 messages. Seven roots retain frontiers. Unsupported or unresolved branches remain visible, including other S.S.Aqua/transport branches. They do not invalidate the particular runtime route exercised here or establish that every route works.

The train data also retains frame-table operands `0x7771/0x7772`, outside the inspected extended-variable range. A separate exploratory VarGet probe returned literal `0x7772`, consistent with the native range check; no source repair was made. The tested quest still completes through the actual officer, coordinate battle and engine events. These legacy conditions must not be promoted to an unavoidable progression blocker merely from their unusual IDs.

## Reproduce and retained evidence

```sh
python3 tools/entry_audit.py
python3 tools/setup_runtime.py
python3 tools/entry_runtime.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tools/verify_sources.py
```

`extracted/scripts/entry_audit.json` retains map identities, events, conditions, raw instructions, text and frontiers. `extracted/runtime/entry/entry.json` retains all 18 expectations, 136 walking requests, fixture declarations and the command transcript. Screenshots include `office_ticket_stamp.png`, `undersea_platform.png`, `electric_party_selection.png`, `valencia_station_arrival.png` and `valencia_port_from_train.png`.

Together with the laboratory and police-to-Mister-R replay, this establishes working entry and late-progression components. It does not bridge every intervening Orange route/gym in one continuous playthrough. The most supported local continuation target remains the promised warehouse puzzle/battle, for which no supported completion handler or intended team has been recovered.
