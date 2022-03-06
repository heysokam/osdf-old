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
- [] Timer
- [] First releasable version (dev)

## CPM and Overbounce (0.2.0 and over)
- [] Full cpm strafing (double jumps and other specific mechanics)
- [] no-ob

## Strafehud and velocity pads (0.3.0)
- [] Proxymod compatibility (?maybe postponed to later patch?)
- [] Velocity pads  

## (0.4.0 and over)
- [] Gamemode "run"
- [] Checkpoints
- [] Triggers / Targets
- [] Frags Filter
- [] Replays
- [] Ghosts
- [] HUD cvar compatibility ()
- [] HUD customization
- [] Instant respawn
- [] Scoreboard
- [] ...

## Complete functionality (1.0.0)
- [] Entity compatibility for existing maps
- [] Server leaderboards
- [] Web access to leaderboards data

## Expand (+1.0.0)
- [] vq1 movement (+ frictionless alternative)
- [] vq2 movement
- [] vq4 movement
- [] Client sided logic (EntityPlus and SourceEngine-I/O inspired)

## Wishlist
- [] Steam integration (requires Standalone game, since we are not modding baseq3 but gpl code)
- [] Portals
- [] Darkplaces Renderer