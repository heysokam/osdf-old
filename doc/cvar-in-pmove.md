

1.  Want to add a cvar that will act as a conditional check inside bg_pmove.c
So far I got the cvar hooked, its g_ based, and its also showing inside the game console correctly
Is there a way to connect the cvar without including all of g_local.h?
The goal is that the cvar will be flagged as cheats, will be server-based, and it will decide what type of movement to apply (aka. fork away to modded functions vs just continue default code)

2. I'm adding some files in a subfolder, such as game/mymod that will contain things like game/mymod/header.h, etc
I have created header.h and code.c inside that subfolder, and those files contain the declaration+definition
I have also added an #include "mymod/myheader.h" line at the top of bg_pmove.c
I'm using the ioq3 makefile for compiling, building only qvm+tools (if that's relevant)
But when I try to call the functions, the compiler is saying that the symbols don't exist
Am I missing something obvious?

t: declare it in your header file then include the file in g main and add it to the cvar table?
afaik you'll still need to declare it on top of bg_pmove

e: You can't really have cvars in bg_pmove, @sOkam!
sOkam!: why so? I wanted to expose things like pm_airaccelerate and such, locked behind cheats ofc

e: it's shared between game and cgame, so the cvar only exists on game when you created it in g_main. 
And also, both game and cgame need to know the same value, because of prediction
sOkam!: i thought bg_ was for that type of thing. maybe im not properly understanding the architecture atm
e: For what type of thing? It is shared but you don't have access to the cvar
t: i dont know how or what's the aim here but afaik, you can communicate the cvar/condition to cgame and tie it up in predictplayerstate so there are no prediction errors
e: On both sides without adding it to both sides

sOkam!: change physics inside console, just like you can normally do with default behavior with g_gravity, g_speed, etc
e: Of course you can, but it's not easy. You'll notice g_gravity isn't referenced anywhere in bg_pmove
It's set as a value in each clients player state which is accessed that way
t: indeed that's the clean and correct way to do it
sOkam!: that's what I want to do, precisely. but how, is the Q 

e: Alternatively do what is done with pmove_msec/pmove_fixed
t: or you can steal an existing ps variable that is bunk (there should be at least one) and use it for your purposes. that's what i do xD
e: By putting the variables in pmove_t you don't need to steal any ps variables
t: true. but i like to live dangerously
e: You haven't lived dangerously until you've remapped large parts of the ps and es 
t: ouch. yeah that sounds awful

sOkam!: is that cheatable in some way by the client?. the goal is that the player cannot change it, unless using sv_cheats
e: I mean with the source available anything is possible cheat wise. But you don't have to make it so they can change the cvar locally
sOkam!: not if the server runs the show, and its safely handled
e: Regardless, the client must still obtain the values from the server
Pmove is executed on client as well. But changing it will only mess up their prediction

sOkam!: the point is for it to be a server-side value
e: Doesn't matter, client still needs to obtain it from server. Whether that be system info, or some other command
sOkam!: so, if its set inside pmove_t, its obtained from the server by the client and also is cvar accessible?
e: No you need to develop that system. That's just how you'd access the data inside of bg_pmove
sOkam!: i see. so the values would need to be hardcoded to make them work differently at the moment, right? (without the tech to hook it to a cvar)
e: No cvar access directly in pmove
https://github.com/etfdevs/ETF/blob/master/code/game/g_active.c#L1265
https://github.com/etfdevs/ETF/blob/master/code/game/g_main.c#L283
https://github.com/etfdevs/ETF/blob/master/code/game/bg_public.h#L280
https://github.com/etfdevs/ETF/blob/master/code/cgame/cg_predict.c#L734
https://github.com/etfdevs/ETF/blob/master/code/cgame/cg_servercmds.c#L213
thats basically the gist of it
you just need to parse out the systeminfo and its best to do it this way because of cvar protection in newer engines
https://github.com/etfdevs/ETF/blob/master/code/cgame/cg_servercmds.c#L439
https://github.com/etfdevs/ETF/blob/master/code/cgame/cg_q3f_init.c#L1259
The latter of which is equivalent to CG_Init(). Find where serverinfo is parsed and put the function call by it

t: f so much suffering till i learned how this process worked
sOkam!: looks complex idd
t: it's not really complex tbh. the simplest of things are most often the hardest. or maybe im just not that bright, anyway xD

t:
you can add stuff to pmove, 
you use it in bg_pmove to manipulate movement, 
then tie it to a server cvar inside clientthink_real, 
then communicate that cvar to the cgame module 
and at the end you tie your pmove variable to the communicated cvar inside predictplayerstate so there be no prediction mess ups
