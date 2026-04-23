extends Camera3D

@export var move_speed: float = 12.0
@export var fast_multiplier: float = 4.0
@export var mouse_sensitivity: float = 0.0025

var yaw: float = 0.0
var pitch: float = 0.0
var mouse_captured: bool = true


func _ready():
	current = true
	yaw = rotation.y
	pitch = rotation.x
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)


func _unhandled_input(event):
	if event is InputEventMouseMotion and mouse_captured:
		yaw -= event.relative.x * mouse_sensitivity
		pitch = clamp(pitch - event.relative.y * mouse_sensitivity, deg_to_rad(-89.9), deg_to_rad(89.9))
		rotation = Vector3(pitch, yaw, 0.0)
	elif event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_ESCAPE:
		mouse_captured = not mouse_captured
		Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED if mouse_captured else Input.MOUSE_MODE_VISIBLE)


func _process(delta):
	var movement := Vector3.ZERO

	if Input.is_key_pressed(KEY_W):
		movement -= global_transform.basis.z
	if Input.is_key_pressed(KEY_S):
		movement += global_transform.basis.z
	if Input.is_key_pressed(KEY_A):
		movement -= global_transform.basis.x
	if Input.is_key_pressed(KEY_D):
		movement += global_transform.basis.x
	if Input.is_key_pressed(KEY_Q):
		movement -= Vector3.UP
	if Input.is_key_pressed(KEY_E):
		movement += Vector3.UP

	if movement != Vector3.ZERO:
		movement = movement.normalized()

	var speed := move_speed
	if Input.is_key_pressed(KEY_SHIFT):
		speed *= fast_multiplier

	global_position += movement * speed * delta


