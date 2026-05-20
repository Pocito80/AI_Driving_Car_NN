extends VehicleBody3D

var track_path: Path3D
var spawn_point: Node3D

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
var laps_completed: int = 0
var total_track_checkpoints: int = 12

var distance_along_track = 0.0
var total_track_length = 0.0
var spawn_track_offset = 0.0

var rays = []

var current_throttle: float = 0.0
var current_steer: float = 0.0

func _ready():
	total_track_length = track_path.curve.get_baked_length()
	

func setup(rays_number):
	rays = [$RaycastLeftFront, $RaycastFront, $RaycastRightFront, $RaycastRight, $RaycastLeft, $RaycastLeftBack, $RaycastRightBack, $RaycastBack]
	rays = rays.slice(0, rays_number)
	var local_spawn_position = track_path.to_local(spawn_point.global_position)
	spawn_track_offset = track_path.curve.get_closest_offset(local_spawn_position)


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

	if  time > 40 and alive:
		end_live()

func hit_checkpoint(index: int):
	if index == target_checkpoint:
		checkpoints_collected += 1
		target_checkpoint += 1
	if target_checkpoint >= total_track_checkpoints:
		laps_completed += 1
		target_checkpoint = 0

func get_state() -> Dictionary:
	var distances = []
	for ray in rays:
		distances.append(ray.get_collision_point().distance_to(ray.global_position) if ray.is_colliding() else 20.0)
	return {
		"id": self.name,
		"sensors": distances,
		"fitness": fitness,
		"traveled": distance_along_track,
		"velocity": round(linear_velocity.length()),
	}
	
func apply_ai_command(throttle: float, steer: float):
	if alive:
		current_throttle = throttle
		current_steer = steer
		track_distance()

func _on_body_entered(body):
	if body.is_in_group("walls") and alive:
		end_live()


func track_distance():
	var car_local_pos = track_path.to_local(global_position)
	var current_offset = track_path.curve.get_closest_offset(car_local_pos)
	
	var offset_difference = current_offset - spawn_track_offset
	if offset_difference < 0:
		offset_difference += total_track_length

	distance_along_track = offset_difference + laps_completed * total_track_length

func end_live():
	alive = false
	current_throttle = 0
	current_steer = 0
	track_distance()
	

	fitness += checkpoints_collected * 100 + distance_along_track

