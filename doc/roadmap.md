# Roadmap:
## Works in default q3a
- [x] Surface flags (uses shader properties)
- [x] Vq3 movement (`pmove_fixed 1`)
- [x] Vq3 Teleports
- [x] vq3 Hurt Trigger
- [x] target score

## Minimal working product (0.0.1)
- [x] Initial setup & compilation (manual)
- [x] Map loading
- [x] Changes to the code actually affect gameplay through `.qvm` files

## Automated compilation on bash shell (0.0.2)
- [x] Automated compilation from makefile
- [x] Automated packing

## Minimal viable product (0.1.0)
- [x] Full vq3 movement
- [x] Basic vq3 Weapons (should be full by default)  
- [x] Basic cpm strafing (Correct accel, aircontrol and A/D strafing)
- [x] Instant respawn (g_combat.c/player_die()/line608  & some other spots to switch timer to ms and make 1 mean immediate )
- [x] Gamemode "run"
- [x] Timer (local, best per session)
- [x] Gamemode "run" (basic)
  - [x] Definition in code (replaced FFA, g_gametype 0)
  - [ ] Entity reset on player_die()
- [ ] First cpm/vq3 alpha/dev release version

## CPM and Physics selection (0.2.0)
- [x] Full cpm strafing (double jumps, slick and other specific mechanics)
- [ ] Basic CPM weapons (should be full with this pass)
  - [x] Rockets 1000ups
  - [ ] ... other
- [x] Physics type Selection (phy_movetype NUMBER :: 0=CPM, 3=VQ3, 1:Q1-ag)

## Strafehud and velocity pads (0.3.0)
- [ ] Proxymod strafehud
- [ ] Velocity pads  

## (0.4.0 and over)
- [ ] Crouch doesn't remove +left/+right
- [ ] no-ob
  - [ ] Rough implementation (cvar phy_overbounce_scale = 1.000f) //TODO Code is created. cvar is currently disconnected
  - [ ] Robust fix for random overbounces only, while keeping the good ones.
- [ ] Independent timer score (separate to fragfilters/score)
- [ ] Frags Filter
- [ ] Triggers / Targets: speed, ...
- [ ] Entity filters: notcpm, notvq3, notsp, notmp, notdf, nottm, notfc, notdefrag
- [ ] Proxymod port
- [ ] Scoreboard
- [ ] All gamemodes
  - [ ] Run (complete)
  - [ ] Tricks Mode
  - [ ] FastCap
  - [ ] Hooks
- [ ] Multiplayer
  - [ ] Remove player interaction
- [ ] ...

## Ghosts and Records (0.9.0)
- [ ] Ghosts
- [ ] Records saving to disk 
- [ ] Better timer
- [ ] Checkpoints and comparison to best times
- [ ] Automatic replay recording

## Complete functionality (1.0.0)
- [ ] Entity compatibility for existing maps
- [ ] HUD customization
- [ ] HUD cvar compatibility   //Is this necessary, because of the hud rewrite ??
- [ ] Server leaderboards
- [ ] Web access to leaderboards data

## Expand (+1.0.0)
_[this section is not a todo, but more like a wishlist of sorts]_
- [ ] Airjump Powerup
- [ ] Physics selection Powerups (cpm and vq3 sections in the same map)
- [ ] Client sided logic (EntityPlus and SourceEngine-I/O inspired)
- [ ] Native race mode (like AG, first to finish wins. also FFA race, standings based on finish order)
- [ ] New data and stats:
  - [ ] Persistent stats per map.
  - [ ] Checkpoints: player vs wr, p vs pb (spec or own), p vs own pb
  - [ ] Getting data from leaderboards server to compare
- [ ] Ghosts expand:
  - [ ] Multiple ghosts (example: own & spec'ed player)
- [ ] Conditional binds (bind X if cvar cvarvalue actionTrue actionFalse)

### New physics
- [x] vq1 movement (qw/ag)
  - [x] AD movement
    - [x] QW balanced
    - [x] AG balanced
  - [ ] SBJ
  - [ ] Duckroll
  - [ ] Q1 rocket launcher
  - [ ] Gaus (needs new name)
  - [ ] ...
- [ ] vq2 movement
- [ ] vq4 movement
- [ ] New mechanics
  - [ ] Walljumps (urt insp) (optional wsw-like powerup, to boost its power)
  - [ ] ...

## Wishlist
- [ ] Vortex weapons (implosion/pull instead of explosion/knockback)
- [ ] Portals
- [ ] Steam integration (requires Standalone game, since we are not modding baseq3 but gpl code)

## Fixes
- [ ] Make target_speaker loop globally (currently can either loop or global, but not both)

