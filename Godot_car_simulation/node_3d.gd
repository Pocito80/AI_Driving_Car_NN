extends Node3D



#var next_checkpoint_required = 0
#var total_checkpoints = 0


#func _ready():
	#for i in range(20):
		#var car = car_scene.instantiate()
		#car.name = "Car_" + str(i)
		#add_child(car)
		#car.add_to_group("player")
		## Bitwise logic: 
		## Layer 2 only (1 << 1)
		#car.collision_layer = 2 
		## Mask Layer 1 only (1 << 0)
		#car.collision_mask = 1
		##car.global_transform = spawn_point.global_transform
#
#var time_elapsed = 0.0
#var game_running = true
	#

#
#func _process(delta):
	#if game_running:
		#time_elapsed += delta
		#$CanvasLayer/TimerLabel.text = "Time: %.2f" % time_elapsed

#func process_checkpoint(index):
	#if index == next_checkpoint_required:
		#print("Checkpoint number " + str(total_checkpoints))
		#print("Checkpoint " + str(index) + " cleared!")
		#next_checkpoint_required += 1
		#print("next requuired" + str(next_checkpoint_required))
		#
		## Check if this was the final checkpoint (The Finish Line)
		#if next_checkpoint_required == total_checkpoints:
			#win_game()
			#
	#else:
		#print("Wrong checkpoint! You missed one.")
#
#func win_game():
	#game_running = false
	#print("Lap Complete!")
