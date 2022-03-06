

> Define gamemode

> Load map
>> Select map gamemode
>> Show gamemode info

> Spawn map entities
>> Spawn timer targets

> Trigger Multiple
>> Target timer
>>> Start
>>> Checkpoint
>>> Finish

struct {
	q3_trigger_t  trigger;   // Trigger that activated this target 
	qboolean 	 canReset;  // Can reset running timer
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
