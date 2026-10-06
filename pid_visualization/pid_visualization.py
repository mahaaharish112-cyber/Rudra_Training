import matplotlib.pyplot as plt


# ============================================================
# PID CONTROLLER - ANGLE CONTROL SIMULATION
# ============================================================

print("=" * 80)
print("                 PID ANGLE CONTROL SIMULATION")
print("=" * 80)

# ------------------------------------------------------------
# USER INPUT
# ------------------------------------------------------------

target_angle = float(input("Enter target angle (degrees): "))
initial_angle = float(input("Enter initial angle (degrees): "))

Kp = float(input("Enter Kp value: "))
Ki = float(input("Enter Ki value: "))
Kd = float(input("Enter Kd value: "))

simulation_time = float(input("Enter simulation time (seconds): "))
dt = float(input("Enter time step (seconds): "))

# Control force limit
max_control_force = float(
    input("Enter maximum control force: ")
)

print("\nStarting PID simulation...\n")


# ============================================================
# PID VARIABLES
# ============================================================

angle = initial_angle

integral = 0.0
previous_error = 0.0

time = 0.0


# ============================================================
# DATA STORAGE
# ============================================================

time_data = []

target_data = []
angle_data = []

error_data = []
correction_data = []
control_force_data = []

p_data = []
i_data = []
d_data = []


# ============================================================
# TERMINAL TABLE HEADER
# ============================================================

print(
    f"{'Time':>8} "
    f"{'Angle':>12} "
    f"{'Error':>12} "
    f"{'Correction':>15} "
    f"{'Control Force':>16}"
)

print("-" * 80)


# ============================================================
# PID SIMULATION
# ============================================================

while time <= simulation_time:

    # --------------------------------------------------------
    # Calculate error
    # --------------------------------------------------------

    error = target_angle - angle


    # --------------------------------------------------------
    # Integral term
    # --------------------------------------------------------

    integral += error * dt


    # --------------------------------------------------------
    # Derivative term
    # --------------------------------------------------------

    if dt > 0:
        derivative = (error - previous_error) / dt
    else:
        derivative = 0.0


    # --------------------------------------------------------
    # PID components
    # --------------------------------------------------------

    P = Kp * error
    I = Ki * integral
    D = Kd * derivative


    # --------------------------------------------------------
    # PID correction
    # --------------------------------------------------------

    correction = P + I + D


    # --------------------------------------------------------
    # Limit control force
    # --------------------------------------------------------

    control_force = max(
        -max_control_force,
        min(correction, max_control_force)
    )


    # --------------------------------------------------------
    # Simulated system
    # --------------------------------------------------------
    #
    # Control force changes the angle.
    #
    # This is a simplified mathematical model.
    #

    angle_change = control_force * dt

    angle += angle_change


    # --------------------------------------------------------
    # Store data
    # --------------------------------------------------------

    time_data.append(time)

    target_data.append(target_angle)
    angle_data.append(angle)

    error_data.append(error)
    correction_data.append(correction)
    control_force_data.append(control_force)

    p_data.append(P)
    i_data.append(I)
    d_data.append(D)


    # --------------------------------------------------------
    # Print terminal output
    # --------------------------------------------------------

    print(
        f"{time:8.2f} "
        f"{angle:12.2f} "
        f"{error:12.2f} "
        f"{correction:15.2f} "
        f"{control_force:16.2f}"
    )


    # --------------------------------------------------------
    # Update previous error
    # --------------------------------------------------------

    previous_error = error

    time += dt


# ============================================================
# FINAL RESULTS
# ============================================================

final_error = target_angle - angle


print("\n")
print("=" * 80)
print("                    SIMULATION RESULTS")
print("=" * 80)

print(f"Target Angle           : {target_angle:.2f} degrees")
print(f"Initial Angle          : {initial_angle:.2f} degrees")
print(f"Final Angle            : {angle:.2f} degrees")

print(f"Final Error            : {final_error:.2f} degrees")

print(f"Final P Contribution   : {p_data[-1]:.2f}")
print(f"Final I Contribution   : {i_data[-1]:.2f}")
print(f"Final D Contribution   : {d_data[-1]:.2f}")

print(f"Final Correction       : {correction_data[-1]:.2f}")
print(f"Final Control Force    : {control_force_data[-1]:.2f}")

print("=" * 80)


# ============================================================
# GRAPH 1
# TARGET ANGLE VS ACTUAL ANGLE
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    time_data,
    target_data,
    label="Target Angle"
)

plt.plot(
    time_data,
    angle_data,
    label="Actual Angle"
)

plt.xlabel("Time (seconds)")
plt.ylabel("Angle (degrees)")

plt.title("Target Angle vs Actual Angle")

plt.legend()
plt.grid(True)

plt.tight_layout()


# ============================================================
# GRAPH 2
# ERROR
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    time_data,
    error_data,
    label="Error"
)

plt.axhline(
    0,
    linestyle="--",
    label="Zero Error"
)

plt.xlabel("Time (seconds)")
plt.ylabel("Error (degrees)")

plt.title("PID Error")

plt.legend()
plt.grid(True)

plt.tight_layout()


# ============================================================
# GRAPH 3
# PID COMPONENTS
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    time_data,
    p_data,
    label="P"
)

plt.plot(
    time_data,
    i_data,
    label="I"
)

plt.plot(
    time_data,
    d_data,
    label="D"
)

plt.xlabel("Time (seconds)")
plt.ylabel("Contribution")

plt.title("PID Components")

plt.legend()
plt.grid(True)

plt.tight_layout()


# ============================================================
# GRAPH 4
# CORRECTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    time_data,
    correction_data,
    label="PID Correction"
)

plt.axhline(
    0,
    linestyle="--",
    label="Zero Correction"
)

plt.xlabel("Time (seconds)")
plt.ylabel("Correction")

plt.title("PID Correction")

plt.legend()
plt.grid(True)

plt.tight_layout()


# ============================================================
# GRAPH 5
# CONTROL FORCE
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    time_data,
    control_force_data,
    label="Control Force"
)

plt.axhline(
    0,
    linestyle="--",
    label="Zero Force"
)

plt.xlabel("Time (seconds)")
plt.ylabel("Control Force")

plt.title("Control Force")

plt.legend()
plt.grid(True)

plt.tight_layout()


# ============================================================
# DISPLAY GRAPHS
# ============================================================

plt.show()
