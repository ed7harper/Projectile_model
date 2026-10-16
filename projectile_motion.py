import math
import matplotlib.pyplot as plt

u = float(input('Initial velocity (m/s): '))
angle = float(input('Launch angle (degrees): '))
Cd = float(input('Drag coefficient: '))
A = float(input('Cross-sectional area (m^2): '))
m = float(input('Mass (kg): '))

g = 9.81
rho = 1.2
dt = 0.001
theta = math.radians(angle)

def simulate(c):
    v_x = u * math.cos(theta)
    v_y = u * math.sin(theta)
    x, y, t = 0.0, 0.0, 0.0
    max_height = 0.0
    xs, ys = [0.0], [0.0]

    while y >= 0:
        v = math.sqrt(v_x**2 + v_y**2)
        a_x = -(c/m) * v * v_x
        a_y = -g - (c/m) * v * v_y
        v_x += a_x * dt
        v_y += a_y * dt
        x += v_x * dt
        y += v_y * dt
        t += dt
        max_height = max(max_height, y)
        xs.append(x)
        ys.append(y)

    return xs, ys, x, max_height, t

c = 0.5 * rho * Cd * A
xs, ys, R, H, T = simulate(c)       
xs0, ys0, R0, H0, T0 = simulate(0)  

print(f'With drag:  range {R:.2f} m, max height {H:.2f} m, time {T:.2f} s')
print(f'No drag:    range {R0:.2f} m, max height {H0:.2f} m, time {T0:.2f} s')

plt.plot(xs, ys, label='With drag')
plt.plot(xs0, ys0, '--', label='No drag')
plt.xlabel('Horizontal distance (m)')
plt.ylabel('Height (m)')
plt.title('Projectile motion: drag vs no drag')
plt.ylim(bottom=0)
plt.legend()
plt.grid(True)
plt.savefig('images:trajectory.png./trajectory.png', dpi=150, bbox_inches='tight')
plt.show()