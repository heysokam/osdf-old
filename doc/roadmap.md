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
- [ ] Timer
  - [ ] Independent timer score (separate to fragfilters/score)
- [ ] First cpm/vq3 releasable version (dev)
- [ ] Gamemode "run"
- [ ] First releasable version (dev)

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
- [ ] Checkpoints
- [ ] Frags Filter
- [ ] Triggers / Targets: speed, ...
- [ ] Tricks Mode
- [ ] Scoreboard
- [ ] Entity filters: notcpm, notvq3, notsp, notmp, notdf, nottm, notfc, notdefrag
- [ ] Proxymod port
- [ ] Replays
- [ ] Ghosts
- [ ] ...

## Complete functionality (1.0.0)
- [ ] Entity compatibility for existing maps
- [ ] Server leaderboards
- [ ] Web access to leaderboards data
- [ ] HUD cvar compatibility ()   //Is this necessary, because of the hud rewrite ??
- [ ] HUD customization

## Expand (+1.0.0)
- [ ] vq1 movement (+ frictionless alternative)
- [ ] vq2 movement
- [ ] vq4 movement
- [ ] Airjump Powerup
- [ ] Physics selection Powerups (cpm and vq3 sections in the same map)
- [ ] Client sided logic (EntityPlus and SourceEngine-I/O inspired)
- [ ] Native race mode (like AG, first to finish wins. also FFA standings based on finish order)

## Wishlist
- [ ] Steam integration (requires Standalone game, since we are not modding baseq3 but gpl code)
- [ ] Portals
- [ ] Vortex weapons (implosion/pull instead of explosion/knockback)
