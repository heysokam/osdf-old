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
- [x] Timer (local, best per session, all maps have TimeReset)
- [x] Gamemode "run" (basic)
  - [x] Definition in code (replaced FFA, g_gametype 0)
- [x] First cpm/vq3 alpha/dev release version

## CPM and Physics selection (0.2.0)
- [x] Physics type Selection (phy_movetype NUMBER :: 0=CPM, 3=VQ3, 1:Q1-ag)
- [x] Full cpm strafing (double jumps, slick and other specific mechanics)
- [ ] Basic CPM weapons (should be full with this pass)
  - [x] Rockets 1000ups
  - [ ] Rockets increased horizontal knockback
  - [x] Instant weapon switch
  - [ ] CPMA changes: Need side-by-side comparison of csdf-cpm and osdf-cpm
    - [ ] Gauntlet knockback changed from 1 to 0.5
    - [ ] Machine Gun damage changed from 7 to 5
    - [ ] Shotgun damage decreased from 10 to 7
    - [ ] Shotgun spread increased from 700 to 900
    - [ ] Shotgun knockback increased from 1 to 1.35
    - [ ] Grenade Launcher reload reduced from 800 to 600
    - [x] Rocket Launcher speed increased from 900 to 1000
    - [ ] Rocket Launcher knockback increased from 1 to 1.2
    - [ ] Rocket Launcher splash knockback increased from 1 to 1.2
    - [ ] Lightning Gun knockback increased from 1 to 1.55
    - [ ] Railgun cooldown decreased from 1500 to 1000 for weapon switch
    - [ ] Plasma Gun damage reduced from 20 to 15
    - [ ] Plasma Gun knockback reduced from 1 to 0.5

## Strafehud and velocity pads (0.3.0)
- [ ] Proxymod strafehud
- [ ] Velocity pads  

## Proxymod port (0.4.0) 
- [ ] Complete proxymod port
  - [ ] strafehud
    - [ ] cgaz
    - [ ] snaps
  - [ ] pitch
  - [ ] compass
  - [ ] jump
  - [ ] RL
  - [ ] GL
  - [ ] bbox


## 0.5.0 and over
- [ ] Crouch doesn't remove +left/+right
- [ ] no-ob
  - [ ] Rough implementation (cvar phy_overbounce_scale = 1.000f) //TODO Code is created. cvar is currently disconnected
  - [ ] Robust fix for random overbounces only, while keeping the good ones.
- [ ] ...
  - [ ] Complete the list of TODO features



## Entities (0.6.0)
- [ ] Support for all Entities
  - [ ] target_ entities
    - [x] target_startTimer
    - [x] target_stopTimer
    - [ ] target_checkpoint
    - [ ] target_speed
    - [ ] target_fragsFilter
    - [ ] target_init
    - [ ] target_smallprint
    - [ ] target_print
    - [ ] target_multimanager
  - [ ] shooter_ entities
    - [ ] shooter_grenade_targetplayer
    - [ ] shooter_plasma_targetplayer
    - [ ] shooter_rocket_targetplayer
    - [ ] shooter_bfg
  - [ ] trigger_ entities
    - [ ] trigger_push_velocity
  - [ ] weapon_grapplinghook_types (support for all df hook types)
- [ ] Entity filters:
  - [ ] notcpm
  - [ ] notvq3
  - [ ] notsp
  - [ ] notmp
  - [ ] notdf
  - [ ] nottm
  - [ ] notfc
  - [ ] notdefrag

## Gamemodes (0.7.0)
- [ ] Run (complete)
- [ ] Tricks Mode
- [ ] FastCap
- [ ] Hooks

## Multiplayer (0.8.0)
- [ ] Multiplayer
  - [ ] Remove player interaction
  - [ ] Per client entity state (timers, weapons, etc)
  - [ ] Scoreboard

## Ghosts and Records (0.9.0)
- [ ] Records saving to disk 
- [ ] Better timer
  - [ ] Independent timer score (separate to fragfilters/score)
  - [ ] Revert hack for `trigger_multiple->wait -1` being hardcoded to `0.5`
  - [ ] Per-client activation of triggers
- [ ] Checkpoints and comparison to best times
- [ ] Automatic replay recording
- [ ] Ghosts

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

