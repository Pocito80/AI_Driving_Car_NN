# AI Driving Module

This repository contains an AI car simulation split between a simulation in Godot and a neural network writen in Python. Python side trains and serves neural networks over UDP to the Godot simulation.

## Overview

- **Godot simulation**: the scene and vehicle logic are in `Godot_car_simulation/` and run in Godot (open the folder as a Godot project).
- **Python backend**: training, model management, plotting and UDP communication are in `Python_NN/`.

The architecture uses a UDP channel between Godot and Python. Godot sends sensor states for a fleet of cars. Python runs the neural networks, returns actuator commands, and performs evolution.

## Features

- Evolutionary training of neural networks (selection, crossover, mutation).
- Save/load model parameters and generation statistics to `Python_NN/Saved_models/`.
- Simple CLI menus for configuring training and loading models.
- Plotting utilities for generation metrics.

## Requirements

- Python 3.13
- Godot 4.6.1 
- Python packages: `numpy`, `matplotlib`, `questionary` (install by running `pip install numpy matplotlib questionary`).


## Quick start — Godot simulation

1. Open `Godot_car_simulation/` in Godot.
2. Run the main scene `Main_Scene.tscn`. The Godot project should wait for the Python UDP server and exchange JSON messages with Python backend.


## Quick start — Python backend

1. Configure training or loading via the interactive menu. From the `Python_NN` folder run:

```bash
python Python_NN/main.py
```

2. The menu allows:
- Starting new training (choose number of agents, mutation rate, raycast count, hidden layer width/depth, activation and mutation functions).
- Continuing training from an existing folder in `Saved_models/`.
- Loading a model for inference (load a saved generation or the `best_model_paramiters.npy`).

3. When running, the Python backend opens a UDP server and waits for a Godot client to connect. Ensure the Godot project is started before the Python backend tries to connect (on default UDP server uses `127.0.0.1` ports `4242` and `4243` make sure that you have this ports free).


## Saved models and outputs

Directory: `Python_NN/Saved_models/`

- `model_<N>` — one folder per run (contains `paramiters.json`, saved `model_paramiters_gen_<g>_car_<i>.npy`, plot data `.npy`, and `best_model_paramiters.npy` when a new best is found).
- `paramiters.json` — JSON dump of `Model_Paramiters` used for that run (number_of_agents, mutation_rate, raycast_number, hidden_layer_width, hidden_layer_depth, activation_function, mutation_function, best_fittness).
- Plot data files: `best_plot_data_fitness.npy`, `average_plot_data_fitness.npy`, etc.

Use the CLI menus to select folders and generations for continuing training or for running inference from a saved model.

## File map

- [Python_NN/main.py]: Main loop and state machine that coordinates initialization, UDP handshake, running, saving and evolution.
- [Python_NN/neural_network.py]: Neural network classes, mutation and crossover implementations, save/load helpers.
- [Python_NN/udp.py]: UDP server wrapper used by the Python backend.
- [Python_NN/menu.py]: Interactive menu using `questionary` to set training parameters and select saved models.
- [Python_NN/plot.py]: Plot helper utilities for showing generation metrics.
- [Godot_car_simulation/ai_manager.gd]: Godot script that manages the fleet of cars, and applies neural network outputs to the cars.
- [Godot_car_simulation/Car.gd]: Godot script for the car logic, including sensors, movement, fitness calculation, and checkpoint handling.
- [Godot_car_simulation/udp.gd]: UDP client wrapper used by the Godot simulation to communicate with the Python backend.
- [Godot_car_simulation/Main_Scene.tscn]: Godot scene containing the track, spawn point, and AI manager.


## Contact

For questions, contact leckimaciek2000@gmail.com.

