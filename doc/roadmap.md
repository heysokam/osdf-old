# Roadmap:
## Works in default q3a
- [x] Surface flags (uses shader properties)
- [x] Vq3 movement (needs `pmove_fixed 1`)
- [x] Vq3 Teleports
- [x] vq3 Hurt Trigger
- [x] target score

## Minimal working product (0.0.1)
- [x] Initial setup & compilation (manual)
- [x] Map loading
- [] Prove that changes to the code actually affect gameplay through `.qvm` files
- [] First releaseable dev version of the mod, with no functionality added to baseq3.

## Automated setup on linux (0.0.2)
- [] Automated compilation from python, custom makefile or scons
- [] Automated packing

## Minimal viable product (0.1.0)
- [x] Basic vq3 movement
- [x] Weapons  
- [] Timer

## CPM and Overbounce (0.2.0 and over)
- [] Basic cpm movement
- [] no-ob

## Strafehud and velocity pads (0.3.0)
- [] Proxymod compatibility (?maybe postponed to later patch?)
- [] Velocity pads  

## (0.4.0 and over)
- [] Checkpoints
- [] Triggers / Targets
- [] Frags Filter
- [] Replays
- [] Ghosts
- [] HUD cleanup
- [] HUD customization
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