import os

import matplotlib.pyplot
import numpy

backLegSensorValues = numpy.load("data/backLegSensorValues.npy")
frontLegSensorValues = numpy.load("data/frontLegSensorValues.npy")

sensor_fig, (back_sensor_axis, front_sensor_axis) = matplotlib.pyplot.subplots(
    2, 1, figsize=(10, 6), num="Touch Sensors", sharex=True
)
back_sensor_axis.plot(
    backLegSensorValues,
    label="BackLeg",
    linewidth=3.0,
    color="#1f77b4",
    alpha=0.95,
)
back_sensor_axis.set_ylim(-0.05, 1.05)
back_sensor_axis.set_ylabel("Touch")
back_sensor_axis.set_title("BackLeg Touch")
back_sensor_axis.grid(True, alpha=0.25)
back_sensor_axis.legend()

front_sensor_axis.plot(
    frontLegSensorValues,
    label="FrontLeg",
    linewidth=3.0,
    color="#d62728",
    alpha=0.95,
)
front_sensor_axis.set_ylim(-0.05, 1.05)
front_sensor_axis.set_xlabel("Time Step")
front_sensor_axis.set_ylabel("Touch")
front_sensor_axis.set_title("FrontLeg Touch")
front_sensor_axis.grid(True, alpha=0.25)
front_sensor_axis.legend()
sensor_fig.tight_layout()

motor_back_path = os.path.join("data", "backLegMotorValues.npy")
motor_front_path = os.path.join("data", "frontLegMotorValues.npy")
if os.path.exists(motor_back_path) and os.path.exists(motor_front_path):
    backLegMotorValues = numpy.load(motor_back_path)
    frontLegMotorValues = numpy.load(motor_front_path)
    matplotlib.pyplot.figure("Motor Commands", figsize=(10, 4))
    matplotlib.pyplot.plot(
        backLegMotorValues,
        label="BackLeg motor",
        linewidth=4.0,
        color="#2ca02c",
        alpha=0.95,
        zorder=3,
    )
    matplotlib.pyplot.plot(
        frontLegMotorValues,
        label="FrontLeg motor",
        linewidth=1.2,
        linestyle="--",
        marker="o",
        markersize=2.5,
        markevery=max(1, len(frontLegMotorValues) // 40),
        color="#ff7f0e",
        alpha=0.95,
        zorder=4,
    )
    matplotlib.pyplot.xlabel("Time Step")
    matplotlib.pyplot.ylabel("Target Angle (rad)")
    matplotlib.pyplot.grid(True, alpha=0.25)
    matplotlib.pyplot.legend()
    matplotlib.pyplot.tight_layout()

matplotlib.pyplot.show()
