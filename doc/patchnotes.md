**Legend**
> new : New features  
> chg : Change in existing functionality  
> dep : Soon-to-be removed feature  
> rmv : Removed feature  
> fix : Bug fixes.  
> sec : Security, in case of vulnerabilities.  
> ... : Part of the feature listed above it

# Unreleased
... :  

# History
## 0.2.0
2022.07.10  
new : (cfg) VM configuration disables QVM loading (vm_cgame 0, vm_game 0, vm_ui 0)  
new : (cfg) Server Pure is deactivated, to allow Library Loading (sv_pure 0)  
new : Buildsystem ported to SCons. No longer uses make  
... : Buildsystem handles Cross-Compiling for both win/lnx  
... : Libraries are not packed in a .pk3 (they don't work from inside one)  
... : Buildscript creates and zips both platform binaries  
chg : CPM Rocket Launcher: Self knockback increased to 1.2  
rmv : Removed bash shell script for launching the mod (was system dependent)  
new : Custom fork of oDFe. Loads osdf mod directly
fix : /cpm and /vq3 commands now work with osdf

2022.05.10  
rmv : Removed bash shell script used for automating the build process. Temporarily stored in `+` subfolder, but will be deleted.  
new : Linux automated build script has been fully rewritten in nimscript (bash becomes {cr}ypt!$C real fast)  
chg : The build system no longer compiles into QVM by default. It creates Dynamic Libraries instead.  
dep : This mod will no longer support the QVM architecture moving forward. Incoming features will make the mod fully incompatible with QVM compilation  

## 0.0.2
new : Local Timer. Best per session. All maps have TimeReset (temporary hack until better Timer support)  
new : target_startTimer entity support  
new : target_stopTimer entity support  

new : Full cpm strafing (double jumps, slick haste, telejumps, stairjumps, rampjumps, etc)  
new : CPM weapon behavior  
... : Instant weapon switch on CPM  
... : Rocket Launcher speed increased from 900 to 1000  

chg : Q1-qw deactivated. Q1 physics default to AG-style  
new : Q1 AD movement, balanced similarly to QW (77fps/32as/100aa)  
new : Q1 AD movement, balanced similarly to AG (125fps/35as/100aa)  
new : Physics type Selection (phy_movetype NUMBER :: 0=CPM, 3=VQ3, 1:Q1-ag)  

new : Initial Main Menu UI layout, background and theme

## 0.0.1
new : Basic cpm strafing (Correct accel, aircontrol and A/D strafing)  
new : Instant respawn.   
... : player_die() has no delay.   
... : g_forcerespawn now means miliseconds, instead of seconds  
... : g_forcerespawn default value changed to 1. Previous behavior is now `g_forcerespawn 20000`  
new : Gamemode "run" (basic). Replaces FFA, `g_gametype 0`  
... : Powerups no longer drop on dead
new : Basic Linux automatic qvm compiling setup. Script at: src/qvm.sh  
... : Automated compilation from makefile  
... : Automated packing  

chg : Changed default pmove_fixed value to 1. It doesn't need to be changed by cfg to work correctly.  
new : Created default .cfg files. Solves pmove_fixed not being used automatically, and some other configuration basics.  

## 0.0.0 (Mod Compiling Basics)  
new : Initial setup & compilation (manual)  
... : Changes to the code actually affect gameplay through `.qvm` files  
:: Worked by default  
: Surface flags (uses shader properties)  
: Vq3 movement (`pmove_fixed 1`)  
: Vq3 Weapons  
: Vq3 Teleports  
: vq3 Hurt Trigger  
: target_score  
: Map loading  

# TODO
#::::::::::::::
_Urgent    : Cause us to react. We stop what we're currently doing and work on the urgent task instead._
_Important : Lead us towards our mission/goals. Require planning, organization and initiative._
#::::::::::::::
# 1 : IMP.URG : Critical
#::::::::::::::
fix : q1 physics working correctly with native binaries  
fix : W movement working properly in q1 physics  

#:::::::::::::::
# 2 : IMP.notU : Planned Goals
#:::::::::::::::
new : Proxymod support  
new : Velocity pads  
new : OBfix  
new : Map loader UI  
new : New hud for Player state configuration (health, ammo, powerups, etc)  
new : Launcher / Updater / Downloader

#:::::::::::::::
# 3 : notI.URG : Non-critical Fixes
#:::::::::::::::
fix : sound bug on some systems (potentially SDL non-static linking or version)  
rmv : Custom qvm-only acos function removed from the code  
chg : CPM w-turn acos function should use stdlib instead  

#::::::::::::::::
# 4 : notI.notU : Implement when possible
#::::::::::::::::
new : /varcommand

