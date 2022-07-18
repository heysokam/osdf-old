**Legend**
> new : New features  
> chg : Change in existing functionality  
> dep : Soon-to-be removed feature  
> rmv : Removed feature  
> fix : Bug fixes.  
> sec : Security, in case of vulnerabilities.  
> ... : Part of the feature listed above it

# Unreleased
_v0.3.0-r0_
2022.07.18
new : Initial accel hud code has been added to the buildsystem. Currently inactive (WIP)

2022.07.15
new : (VJK) New Mechanic: Jump Holdboost
   ::  While holding jump, and moving at +375ups, you get extra jumpvel on each jump (375 is 1.5x of 250basespeed)
   ::  It will reach the same heigh than vq3 in 8jumps, but will keep growing
   ::  Starts at 225 base jumpvel, and increases by 5u each jump
   ::  5u is 12% of 45. Which is the difference between vq3 and vjk jumpvel (270-225)
new : (VJK) HoldBoost hud element

2022.07.14
new : Sound event control system in cg_event.c  Can be used to stop any type of sound spam (autojump, rampslides, etc)
new : (CQ3) New physics: VQ3 aircontrol, with CPM tech (dj/ramps/slick/etc)

2022.07.13
new : pm_time hud element   (mainly related to skimming, but general purpose)
new : New mechanic: Rampslides from Q2  (currently active for VQ4 physics)
chg : (VQ1) Added Q3 Overbounces
fix : (VQ1) Fixed visual glitch on physics change without `/map` command
new : (VQ1) Crouching mid-air raises your feet by 14u (sbj). Allows jump to reach higher and further.
new : (VQ4) Crouching mid-air raises your feet by 12u (sbj). Allows jump to reach higher and further.

2022.07.12
fix : (VQ3) Fixed upramps giving the wrong amount of velocity on jump
chg : (VJK) Reverted jumpvel back to 225 (in preparation for a new jump height mechanic)
new : (VQ4) New physics : Quake 4 Inspired.  Activate with `/exec phy_vq4`
   ::       Will have crouchsliding, rampslides (from q2/q4) and vq3 aircontrol
new : (VQ4) Set groundaccel to 15 (same as original Q4 and cpm)
new : (VQ4) New mechanic: Crouchslide
   ::       Earns 2x frames of crouchslide per 1x frame spent in the air, capped at 2000ms 
   ::       Has 0 friction, and a separate accel value of 20  (could change after testing)
... :  

# History
## 0.2.0
2022.06.21
_v0.2.0-r0_  
new : OBfix. Applied on SURF_NOOB surfaces (cvar to be done)
chg : bg_pmove restructure. Moved all custom code to phy/ subfolder

2022.06.20
new : Initial work on Strafehud porting. Not connected, but doesn't break compiling
chg : (VJK) Changed jumpvel from 225 to default vq3 (270), to allow easier clearing of defrag maps
fix : (Q1) "Stepdown" bug is fixed (wasn't stepdown, it was q1 downramp behavior happening on incorrect dotproduct)
fix : (Q1) W/S movement working properly in q1 physics  
fix : (Q1) Crouch works again in q1 physics  
fix : (Q1) Surf ramps no longer stick you to the ramp on exit
... : (code) VectorReflectOS. Sets backoff = 0 when facing away from the surface
new : (Q1) Variable Jump Heights. Activated with +speed. 
... :      Flatground = x0.5 jumpvel
... :      Downramps behave like q1 (additive, based on your current Zvel)

2022.06.18  
chg : CPM Item Pickup: Above size increased from 36u (32u doesn't trigger) to 66 (62u doesn't trigger)  
new : VJK physics. VQ3 with 4airaccel, 12groundspeed, 250speed and 225jumpvel. `/exec phy_vjk`  
chg : Moved all custom bg_pmove.c code into subfolder sgame/phy/  (not connected to the buildsystem yet)   
new : Added basic buildsystem instructions (sketch)  
... : Added Native windows build instructions for the `chocolatey/mingw` method  
... : Added disclaimer for WSL cross-compilation  
new : Initial edits to the buildsystem for native windows compilation  
... : Fixed native win32 SCons environment resolution  
... : Changed file path resolution, so that it remains system-agnostic (uses SCons Nodes wherever possible)  

2022.06.11
fix : CPM Rocket Launcher: Vertical self knockback scaling reduced to 1  

2022.06.10  
_v0.2.0-r0_  
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
fix : double-ramp-boost bug on `r7-climbworld` (found on VQ1, check on other physics)
fix : Wall-stop bug

#:::::::::::::::
# 2 : IMP.notU : Planned Goals
#:::::::::::::::
new : Velocity pads  
new : Proxymod support  
new : Hud element: Current map & Internal version  
new : Map loader UI  
new : Launcher / Updater / Downloader
new : New hud for Player state configuration (health, ammo, powerups, etc)  

fix : Mappers/visual cfg gets wiped out by the build script
??? : wsw hud system . how does it work?

port github.com/Jelvan1/cgame_proxymod#examples

port Warp entities

#SP
new : Font support
new : UI q3ui
new : UI revamp
new : W based physics (WW)
... : W turning affected by phy_ground_accel and phy_speed (aka also by haste)
... : W accelerate (how to balance)
... : AirJump by default
... : Dash by default (ground and air)
... : Blink by default (MC-EoE style?)
... : Wallkick by default


#:::::::::::::::
# 3 : notI.URG : Non-critical Fixes
#:::::::::::::::
fix : sound bug on some systems (potentially SDL non-static linking or version)  
new : Pre-run balance for q1. Pure vs Pro runs from AG (maybe also cpm?)
fix : map_restart doesn't reset timer

#::::::::::::::::
# 4 : notI.notU : Implement when possible
#::::::::::::::::
new : Q1 barrel entity
new : USE buttons
new : Unlock 1000 maxfps. Possible?
new : /varcommand
chg : (CPM) Correct deceleration values

