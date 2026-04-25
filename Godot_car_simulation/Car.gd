extends VehicleBody3D

var max_RPM = 2000
var max_torque = 1600
var max_brake_force = 15.0
var turn_speed = 10
var turn_amount = 0.3

var time = 0
var alive = true
var fitness = 0

var checkpoints_collected: int = 0
var target_checkpoint: int = 0
var total_track_checkpoints: int = 12


# @onready var rays = [$RaycastLeft, $RaycastFront, $RaycastRight]
@onready var rays = [$RaycastLeft, $RaycastFront, $RaycastRight, $RaycastLeft2, $RaycastRight2]

var current_throttle: float = 0.0
var current_steer: float = 0.0

func _physics_process(delta):

	var RPM_left = abs($wheel_back_left.get_rpm())
	var RPM_right = abs($wheel_back_right.get_rpm())
	var RPM = (RPM_left + RPM_right) / 2.0

	if current_throttle > 0.0:
		var torque = current_throttle * max_torque * pow(1.0 - (RPM / max_RPM), 0.5)
		engine_force = torque
		brake = 0.0
	elif current_throttle < 0.0:
		engine_force = 0.0
		brake = abs(current_throttle) * max_brake_force 
	else:
		engine_force = 0.0
		brake = 2.0 
	
	var steer_target = current_steer * -turn_amount

	var return_speed = turn_speed
	if current_steer == 0.0:
		return_speed = turn_speed * 5.0 

	steering = lerp(steering, steer_target, return_speed * delta)
		
		
	if alive:
		time += delta
		fitness += (linear_velocity.length() * 3.6)/1000

	if  time > 40 and alive:
		# fitness = -10 * time + 400
		# print("Car", self.name, "finished with fitness:", fitness, "and time:", time,"collected:")
		end_live()

func hit_checkpoint(index: int):
	print("Car", self.name, "hit checkpoint", index, "target was", target_checkpoint)
	if index == target_checkpoint:
		checkpoints_collected += 1
		target_checkpoint += 1
	if target_checkpoint >= total_track_checkpoints:
		target_checkpoint = 0

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
	fitness += checkpoints_collected * 100
	# print("Car", self.name, "ended live with fitness:", fitness, "and time:", time,"collected:", checkpoints_collected)


