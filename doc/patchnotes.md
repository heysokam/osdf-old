**Legend**
> new : New features
> chg : Change in existing functionality
> dep : Soon-to-be removed feature
> rmv : Removed feature
> fix : Bug fixes.
> sec : Security, in case of vulnerabilities.

# Unreleased
... : 

# History

## 0.0.2
new : Local Timer. Best per session. All maps have TimeReset (temporary hack until better Timer support)
new : target_startTimer entity support
new : target_stopTimer entity support

new : Full cpm strafing (double jumps, slick haste, telejumps, stairjumps, rampjumps, etc)
new : CPM weapon behavior
    : Instant weapon switch on CPM
    : Rocket Launcher speed increased from 900 to 1000

chg : Q1-qw deactivated. Q1 physics default to AG-style
new : Q1 AD movement, balanced similarly to QW (77fps/32as/100aa)
new : Q1 AD movement, balanced similarly to AG (125fps/35as/100aa)
new : Physics type Selection (phy_movetype NUMBER :: 0=CPM, 3=VQ3, 1:Q1-ag)

## 0.0.1
new : Basic cpm strafing (Correct accel, aircontrol and A/D strafing)
new : Instant respawn. 
    : player_die() has no delay. 
    : g_forcerespawn now means miliseconds, instead of seconds
    : g_forcerespawn default value changed to 1. Previous behavior is now `g_forcerespawn 20000`
new : Gamemode "run" (basic). Replaces FFA, `g_gametype 0`
new : Basic Linux automatic qvm compiling setup. Script at: src/qvm.sh
    : Automated compilation from makefile
    : Automated packing

chg : Changed default pmove_fixed value to 1. It doesn't need to be changed by cfg to work correctly.
new : Created default .cfg files. Solves pmove_fixed not being used automatically, and some other configuration basics.

## 0.0.0 (Mod Compiling Basics)
new : Initial setup & compilation (manual)
    : Changes to the code actually affect gameplay through `.qvm` files
:: Worked by default
: Surface flags (uses shader properties)
: Vq3 movement (`pmove_fixed 1`)
: Vq3 Weapons
: Vq3 Teleports
: vq3 Hurt Trigger
: target_score
: Map loading

