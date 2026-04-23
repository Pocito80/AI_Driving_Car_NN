extends Area3D

@export var checkpoint_index: int = 0

func _on_body_entered(body):
	if body.is_in_group("player"):
		if body.has_method("hit_checkpoint"):
			body.hit_checkpoint(checkpoint_index)