extends VehicleBody3D

var max_RPM = 2000
var max_torque = 1600
var max_brake_force = 15.0 # Added: Adjust this for how hard the AI can brake
var turn_speed = 10
var turn_amount = 0.3

var time = 0
var alive = true
var fitness = 0

var checkpoints_collected: int = 0
var target_checkpoint: int = 0
var total_track_checkpoints: int = 12

# This path MUST match the name of your Label node in the scene tree
#@onready var speed_label = $UI/SpeedLabel 
# @onready var rays = [$RaycastLeft, $RaycastFront, $RaycastRight]
@onready var rays = [$RaycastLeft, $RaycastFront, $RaycastRight, $RaycastLeft2, $RaycastRight2]

# --- AI STATE VARIABLES ---
# These store the commands from Python until the next frame
var current_throttle: float = 0.0
var current_steer: float = 0.0

func _physics_process(delta):
	# RPM Calculation for torque curve
	var RPM_left = abs($wheel_back_left.get_rpm())
	var RPM_right = abs($wheel_back_right.get_rpm())
	var RPM = (RPM_left + RPM_right) / 2.0
	
	# --- AI MOTOR & BRAKING LOGIC ---
	if current_throttle > 0.0:
		# Acceleration (Throttle 0.1 to 1.0)
		var torque = current_throttle * max_torque * pow(1.0 - (RPM / max_RPM), 0.5)
		engine_force = torque
		brake = 0.0
	elif current_throttle < 0.0:
		# Braking (Throttle -0.1 to -1.0)
		engine_force = 0.0
		# abs() turns the negative throttle into a positive braking force
		brake = abs(current_throttle) * max_brake_force 
	else:
		# Coasting (Throttle exactly 0.0)
		engine_force = 0.0
		brake = 2.0 
	
	# --- AI STEERING LOGIC ---
	# In Godot, positive steering turns LEFT, negative turns RIGHT.
	var steer_target = current_steer * -turn_amount

	# If the AI is not trying to steer, return wheels to center 5x faster
	var return_speed = turn_speed
	if current_steer == 0.0:
		return_speed = turn_speed * 5.0 

	steering = lerp(steering, steer_target, return_speed * delta)
		
	# --- SPEEDOMETER LOGIC ---
	#var speed_ms = linear_velocity.length()
	#var speed_kmh = speed_ms * 3.6
	#if speed_label:
		#speed_label.text = str(round(speed_kmh)) + " KM/H"
		
	if alive:
		time += delta
		# fitness += (linear_velocity.length() * 3.6)/1000

	if (checkpoints_collected == total_track_checkpoints or time > 40) and alive:
		fitness = -10 * time + 400
		# print("Car", self.name, "finished with fitness:", fitness, "and time:", time,"collected:")
		end_live()

func hit_checkpoint(index: int):
	# Only award a point if it's the checkpoint the car is SUPPOSED to hit next
	if index == target_checkpoint:
		checkpoints_collected += 1
		target_checkpoint += 1

func get_state() -> Dictionary:
	var distances = []
	for ray in rays:
		distances.append(ray.get_collision_point().distance_to(ray.global_position) if ray.is_colliding() else 20.0)
	
	return {
		"id": self.name,
		"sensors": distances,
		"fitness": fitness,
		"velocity": round(linear_velocity.length()),
	}
	
func apply_ai_command(throttle: float, steer: float):
	# Update the state variables with data from Python.
	# clamp() ensures a buggy Python script can't send a throttle of 5000 and break physics.
	if alive:
		current_throttle = throttle
		current_steer = steer
		#print(current_steer, current_throttle)
		#print(target_checkpoint)

func _on_body_entered(body):
	if body.is_in_group("walls") and alive:
		# print("BOOM!")
		end_live()
		#print(time)
		#print(fitness)
		#get_tree().call_deferred("reload_current_scene")

func end_live():
	alive = false
	current_throttle = 0
	current_steer = 0
	# fitness += checkpoints_collected * 100
	# print("Car", self.name, "ended live with fitness:", fitness, "and time:", time,"collected:", checkpoints_collected)


