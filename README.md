# Physics-Simulator-Python v1.0
-->A high-performance 2D Physics Engine built in Python using NumPy and Pygame. Unlike standard velocity-based simulators, this engine uses Verlet Integration to achieve superior stability for rigid bodies and constraints.

# Verlet Physics Engine

A 2D rigid-body physics simulator built with Python, NumPy, and Pygame. This project implements non-linear constraint resolution and Verlet integration to create a stable, interactive environment for rigid and soft bodies.

## Technical Overview

### 1. Numerical Integration
Most basic simulators use Euler Integration ($Pos_{new} = Pos_{now} + V \cdot \Delta t$). However, velocity-based systems are prone to floating-point drift, causing objects to "explode" during high-speed collisions.

This engine utilizes **Verlet Integration**, which derives motion from the difference between the current and previous positions:

$$x_{new} = x_{now} + (x_{now} - x_{old}) + a \cdot \Delta t^2$$

### Key Benefits of Verlet:
* **Implicit Velocity:** The term $(x_{now} - x_{old})$ acts as a self-correcting velocity.
* **Geometric Stability:** If a particle is manually moved (e.g., snapped back inside a wall), the velocity automatically recalculates based on the new displacement.
* **Constraint Handling:** It allows for rigid distance constraints without complex impulse-based math.

### 2. Constraint Resolution
The engine uses an iterative solver (10 iterations per frame) to resolve two types of constraints:
* **Boundary Constraints:** Particles are snapped to the viewport edges (Floor/Walls). The resulting change in position creates a natural bounce effect.
* **Distance Constraints (Links):** Links maintain a "Resting Length" between two particles. If the distance deviates, the solver pushes or pulls the particles to maintain structural integrity.

### 3. Rigid Body Architecture
To prevent shapes from shearing or collapsing, a **Star Topology** is used:
* **Squares:** 4 corner particles + 1 central hub linked to every corner via internal braces.
* **Triangles:** 3 corner particles + 1 incenter particle linked to the vertices.
This "Skeleton" approach provides high torsional rigidity while remaining lightweight.

## Features
* **Parent ID System:** Every particle and link is tagged with a unique object ID. This allows for atomic deletion; removing a single part of a square wipes all associated entities to prevent "ghost physics."
* **Real-time Interaction:** Left-click to grab and throw objects; right-click to delete objects by ID.
* **Dynamic Physics:** Real-time gravity adjustment and variable bounce coefficients.
* **Vectorized Math:** Utilizes NumPy for high-speed coordinate calculations and distance norms.

## Controls
| Input | Action |
| :--- | :--- |
| 1 | Spawn Simple Particle |
| 2 | Spawn Rigid Square |
| 3 | Spawn Rigid Triangle |
| Left Click | Grab and Move |
| Right Click | Delete Object (Atomic ID wipe) |
| UP / DOWN | Adjust Gravity |
| O/P | Adjust Bounce Factor|
| Z | Zero Gravity Toggle |

## Requirements
* Python 3.x
* NumPy
* Pygame

## Usage
1. Clone the repository.
2. Run `pip install numpy pygame`.
3. Execute `python main.py`.
