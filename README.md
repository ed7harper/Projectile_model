# Projectile Motion Simulator (Euler's Method)

A Python model of a projectile launched at an angle, comparing its path **with** and **without** air resistance. The motion is stepped forward in time using **Euler's method**, and the trajectories are plotted with matplotlib.

The default object is a tennis ball launched at 30 m/s and 45°.

![trajectories](GitHub/Projectile_model_Euler/trajectory.png)
---

## Contents

- [Why a numerical model?](#why-a-numerical-model)
- [The physics](#the-physics)
- [Euler's method](#eulers-method)
- [How the code works](#how-the-code-works)
- [Results](#results)
- [Accuracy and time step](#accuracy-and-time-step)
- [Does accuracy change with launch speed?](#does-accuracy-change-with-launch-speed)
- [Assumptions and limitations](#assumptions-and-limitations)
- [Running the code](#running-the-code)
- [Possible extensions](#possible-extensions)

---

## Why a numerical model?

Without air resistance, projectile motion has an exact solution from the SUVAT equations, so it can be worked out by hand.

With air resistance, the drag force depends on the speed, and the speed depends on both the horizontal and vertical velocity. That makes the x and y motion **coupled**, and there is no simple formula for the path. The standard way around this is to split the flight into many small time steps and update the motion one step at a time. That is what this project does.

---

## The physics

### Without air resistance

The only force is gravity:

```
aₓ = 0
a_y = −g
```

The exact solution (used to check the model):

```
x = v₀·cosθ·t
y = h₀ + v₀·sinθ·t − ½gt²

Range (h₀ = 0):   R = v₀²·sin2θ / g
Maximum height:   H = (v₀·sinθ)² / 2g
```

### With air resistance (quadratic drag)

For fast-moving everyday objects such as balls, drag is proportional to speed squared:

```
F_D = ½ · ρ · C_d · A · v²
```

| Symbol | Meaning | Default value |
|---|---|---|
| ρ | Air density | 1.225 kg/m³ |
| C_d | Drag coefficient | 0.55 |
| A | Cross-sectional area, π(d/2)² | d = 0.067 m |
| m | Mass | 0.057 kg |
| g | Gravitational field strength | 9.81 m/s² |

Drag always acts directly **opposite the velocity**. Resolving it into components and dividing by mass gives:

```
k   = ½ρC_dA / m
v   = √(vₓ² + v_y²)

aₓ  = −k · v · vₓ
a_y = −g − k · v · v_y
```

Both accelerations contain the total speed `v`, which is why the x and y motion can't be solved separately.

A useful check is the **terminal velocity** when falling straight down, where drag balances weight:

```
v_t = √(g / k)
```

---

## Euler's method

Euler's method assumes that over one small time step Δt, each quantity changes at the rate it had **at the start of the step**:

```
new value = old value + (rate of change) × Δt
```

Applied to the projectile, each step is:

```
aₓ, a_y = accelerations from current vₓ, v_y

x   = x  + vₓ · Δt
y   = y  + v_y · Δt
vₓ  = vₓ + aₓ · Δt
v_y = v_y + a_y · Δt
t   = t  + Δt
```

This repeats until the projectile reaches the ground (y < 0).

### Finding the landing point

The ground is almost never hit exactly at the end of a step. On the step where y changes from positive to negative, the landing point is estimated by **linear interpolation** between the last two points:

```
x_land = x₁ + (x₂ − x₁) · y₁ / (y₁ − y₂)
```

Without this, the range would be off by up to one step's worth of horizontal distance.

---

## How the code works

<!-- Edit this section to match your actual file and function names. -->

1. **Set up constants:** g, launch speed, angle, time step, and the ball's mass, diameter, drag coefficient and air density.
2. **Calculate the drag constant** `k = ½ρC_dA / m`.
3. **Resolve the launch velocity** into `vₓ = v₀cosθ` and `v_y = v₀sinθ`.
4. **Loop with Euler's method**, storing x and y at each step, until y becomes negative.
5. **Interpolate the landing point.**
6. **Run the loop twice**, once with drag switched off (k = 0) and once with it on.
7. **Plot both trajectories** on the same axes with matplotlib and print the range and maximum height.

---

## Results

Tennis ball, v₀ = 30 m/s, θ = 45°, launched from ground level, Δt = 0.02 s:

| | Range | Max height |
|---|---|---|
| Without air resistance | 92.17 m | 23.15 m |
| With air resistance | 40.77 m | 14.00 m |
| **Change due to drag** | **−56%** | **−40%** |

Air resistance more than halves the range. For a light object at this speed, drag is clearly **not** negligible.

The trajectory with drag is also **not symmetrical**: the descent is steeper than the ascent, because the ball has lost horizontal speed by the time it comes down.

---

## Accuracy and time step

Euler's method is only an approximation. Because it uses the start-of-step values for the whole step, it builds up a small error each step.

**Without drag**, the model can be checked against the exact SUVAT answer (range 91.74 m, height 22.94 m):

| Δt (s) | Range (m) | Range error | Max height (m) |
|---|---|---|---|
| 0.1 | 93.86 | +2.3% | 24.01 |
| 0.02 | 92.17 | +0.47% | 23.15 |
| 0.002 | 91.79 | +0.05% | 22.96 |
| **Exact** | **91.74** | — | **22.94** |

**With drag** there is no exact answer, so results were compared against a run with a much smaller time step (Δt = 0.0005 s), which gives a range of about 40.72 m:

| Δt (s) | Range (m) | Max height (m) |
|---|---|---|
| 0.1 | 40.94 | 14.46 |
| 0.02 | 40.77 | 14.00 |
| 0.002 | 40.73 | 13.90 |

### What this shows

- **Euler overshoots.** On the way up the ball is slowing down, so the velocity at the start of each step is always slightly too high. The model therefore goes a little too high and too far.
- **The error is roughly proportional to Δt.** Making the time step 10× smaller makes the error about 10× smaller. This is why Euler's method is called a *first-order* method.
- **Δt = 0.002 s is accurate to well under 0.1%** for this problem, at the cost of more steps (about 2,000 for one flight).

---

## Does accuracy change with launch speed?

Euler range error at a fixed Δt = 0.02 s and θ = 45°:

| Launch speed | No drag: error | No drag: % | With drag: error | With drag: % |
|---|---|---|---|---|
| 10 m/s | +0.14 m | 1.39% | +0.11 m | 1.26% |
| 30 m/s | +0.42 m | 0.46% | +0.05 m | 0.12% |
| 60 m/s | +0.85 m | 0.23% | −0.24 m | −0.33% |
| 100 m/s | +1.41 m | 0.14% | −0.61 m | −0.66% |

- **Without drag:** the error in metres grows with speed, but the **percentage** error shrinks. Euler adds roughly one step's worth of horizontal travel (about vₓ·Δt), while the total flight gets much longer.
- **With drag:** at high speeds the error grows in both metres and percentage. Drag ∝ v², so at high speed the acceleration is large and changes quickly within each step, which breaks Euler's assumption of a constant rate over the step. The error also changes sign, because Euler starts to **overestimate** the drag and undershoots the range.

**Takeaway:** if you increase the launch speed, reduce Δt as well.

---

## Assumptions and limitations

- The ball is treated as a **point mass**.
- **C_d is constant.** In reality it varies with speed and with the state of the ball's surface. For a tennis ball it is typically around 0.5–0.6.
- **Spin is ignored**, so there is no Magnus (lift) force. Real topspin and backspin shots curve noticeably.
- **No wind**, and g and air density are constant (reasonable for heights of tens of metres).
- The ground is **flat** at y = 0.
- Euler's method introduces a **step-size error** (see above).

---

## Running the code

<!-- Replace projectile.py with your actual file name. -->

Requirements: Python 3 and matplotlib.

```bash
pip install matplotlib
python projectile.py
```

To try different scenarios, change the constants at the top of the script, such as the launch speed, angle, time step or drag coefficient.

---

## Possible extensions

- [ ] Find the **optimum launch angle** with drag. Without drag it is 45°; with drag it is lower.
- [ ] Plot **range error against Δt** on log axes to show the first-order behaviour.
- [ ] Add a **Magnus force** to model spin.
- [ ] Model a different object, such as a football, golf ball or shot put, and compare how much drag matters.
- [ ] Add **wind** as a constant horizontal air velocity.
- [ ] Plot **speed against time** and show the ball approaching terminal velocity.

---

## Author

Ed: self-taught project exploring numerical methods and mechanics, as part of preparing for engineering.








