

> Define gamemode

> Load map
>> Select map gamemode
>> Show gamemode info

> Spawn map entities
>> Spawn timer targets

> Trigger Multiple
>> Target timer
>>> Start
	Entity activated:       target_startTimer
	Function called:        timer_start(timer)
    Event sent to client:   ET_TIMER_START
    Client function:        cg_timer_update(timer)

>>> Checkpoint
	Entity activated:       target_checkpoint
    Event sent to client:   ET_TIMER_CHECKPOINT
	Function called:        timer_checkpoint(timer)
>>> Finish
	Entity activated:       target_stopTimer
    Event sent to client:   ET_TIMER_STOP
	Function called:        timer_checkpoint(timer)
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
