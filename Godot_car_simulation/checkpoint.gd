extends Area3D

# This number tells the manager which checkpoint this is (0, 1, 2, etc.)
@export var checkpoint_index: int = 0

func _on_body_entered(body):
	# Check if the object that entered is actually the player
	if body.is_in_group("player"):
		# Tell the main world script that this specific checkpoint was hit
		if body.has_method("hit_checkpoint"):
			body.hit_checkpoint(checkpoint_index)
		#get_parent().get_parent().process_checkpoint(checkpoint_index)
		# Optional: disable the checkpoint so it can't be hit twice
		#monitoring = false
