
//
// g_target.c
//
void target_timer_use( int ev, gentity_t *act ) {
  // Skip cases
  if (!act->client){return;} // Activator is not a client
  if (act->client->ps.pm_type != PM_NORMAL){return;} // Activator is not in normal movement mode
  if (act->client->ps.stats[STAT_HEALTH] <= 0){return;} // Activator is not alive

  switch (ev){
  case EV_TIMER_START:
    // Hitting start trigger
    // Set start to servertime
    act->client->ps.stats[STAT_TIME_START] = cmd.servertime; ///TODO ????
    // Notify: New time as servertime
  case EV_TIMER_CP:
    // Hitting checkpoint trigger, and timer is active
    // Exit if timer is not active (start = NULL)
    if (act->client->ps.stats[STAT_TIME_START] = NULL) {return;}
    //
    // Notify: Add client checkpoint as current servertime - start
    // ??
  case EV_TIMER_CANCEL:
    // Cancel timer. When player respawns, and timer is active
    // Exit if timer is not active (start = NULL)
    if (act->client->ps.stats[STAT_TIME_START] = NULL) {return;}
    // 
    // Notify: Timer has been canceled at servertime - start
    // Set timer to inactive (start = NULL)
    act->client->ps.stats[STAT_TIME_START] = NULL;
  case EV_TIMER_END:
    // Hitting stop trigger with an active timer
    // Exit if timer is not active (start = NULL)
    if (act->client->ps.stats[STAT_TIME_START] = NULL) {return;}
    //
    // Store end time
    // Notify: Final run time is servertime - start
    // Set timer to inactive (start = NULL)
    act->client->ps.stats[STAT_TIME_START] = NULL;
  }
}








//..//  I don't think we need all of this
//        All that we need is probably just the start servertime
//        Instead of adding time every frame...
//          we calculate the time on the client or server when needed
//          and consider NULL as the timer being inactive
typedef struct {
  qboolean active;  // inactive:  time = NULL
  int time;         // calculated, not stored
  int start;        // stored in ps.stats
} timerData_t;









> Define gamemode
  - 0 = run = ffa-default

> Load map
>> Select map gamemode [x]
>> Show gamemode info  [x]

> Spawn map entities
>> Spawn timer targets [ ]
    SP_target_timer    [ ]
      Populate timer entity properties

> Trigger Multiple
>> Target timer
>>> Start
	Entity activated:       target_startTimer
	Function called:        timer_start(timer)
    Event sent to client:   ET_TIMER_START
    Client function:        cg_timer_update(timer)

>>> Checkpoint
	Entity activated:       target_checkpoint
	Function called:        timer_checkpoint(timer)
    Event sent to client:   ET_TIMER_CHECKPOINT
>>> Finish
	Entity activated:       target_stopTimer
	Function called:        timer_checkpoint(timer)
    Event sent to client:   ET_TIMER_STOP
>>>  ??    Can I use just one event type for all of them ??   
>>>> ET_TIMER
>>>> entity->classname == "target_startTimer" :: do start function

struct {
	q3_trigger_t  trigger;   // Trigger that activated this target 
	qboolean 	 canReset;   // Can reset running timer
  
} timerData_t;

timerData_t timer;
timer_reset(timer){return;}
timer_start(timer){ // When the trigger is activated
	qboolean canReset;
	
	// Reset behavior
	canReset = (timer.trigger.wait == -1 || timer.canReset)
	if (canReset) { timer_reset; return; }

	// Start behavior
	// Create event
	// Initialize to 0
	return;
}

timer_frame(timer){ // Each frame, when there is a timer event running
	
}

timer_checkpoint(){
	return;
}

timer_stop(){
	return;
}


// Post 1.0.0 only
// Extra functionality. 
> Mapper selected timer name
> Multiple timers 

> Kinda related to timers, being able to force checkpoints and their order without frag filters would be nice as frag filters are just an unnecessary step if nothing uses frags outside of CPs and finish but I don't think that goes well for csdf unless cgg copies the code over, as with any new changes :S
>> sOkam!: Checkpoint entities could have a new key in them, that selects the order in which they can be activated. Kindof like a score system (aka fragfilters), but living only in timer entities.
That way the mapper will dictate the order of them, and will only need to add fragfilters to support csdf IF they want to
Trigger stop could then have a new key in it, that stores the number of checkpoints required to activate

The new entities on csdf will just ignore those keys, because there is not code for doing anything about them. So, in this way, the new system can coexist with the current csdf one, without making the entities incompatible with each other. 


One way triggers: (Is this possible?)
Make one way triggers (trigger patches) function the same as one-way clips. Currently going thru a trigger patch functions the same as a normal trigger brush
