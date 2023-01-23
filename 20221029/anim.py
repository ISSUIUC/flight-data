"""
Matplotlib Animation Example

author: Jake Vanderplas
email: vanderplas@astro.washington.edu
website: http://jakevdp.github.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import pandas as pd

df = pd.read_csv("flight_computer.csv")[300:]
t = df["timestamp_ms"]
mx = df["mx"]
my = df["my"]
mz = df["mz"]
voltage = df["battery_voltage"]
mx_min = min(mz)
mx_max = max(my)

fsm_timer = df["rocket_state0"]
fsm_50 = df["rocket_state1"]
fsm_gnc = df["rocket_state3"]
fsm_6 = df["rocket_state2"]

FRAMES = 18989
FPS = 100

# styling stuff
plt.rcParams["font.family"] = "monospace"
plt.style.use("dark_background")

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, len(t)/100), ylim=(-1, 15))
ax.set_xlabel("Time (s)")
ax.set_ylabel("Stage in Flight")

line, = ax.plot([], [], lw=2, label="Mostly Timer-Based")
# line2, = ax.plot([],[], lw=2, label="my")
line3, = ax.plot([], [], lw=2, label="Kalman Filter Data-Based")



# initialization function: plot the background of each frame
def init():
    line3.set_data([], [])
    return line3,

# animation function.  This is called sequentially

# fig_voltmag, ax1 = plt.subplots()
# ax2 = ax1.twinx()
# ax1.set_ylim(6, 9)
# ax2.set_ylim(-1, 1)
def animate_voltmag(i):
    ax1.cla()
    ax2.cla()
    v = voltage[1:i]
    m = mz[1:i]
    x = np.linspace(1, len(v), len(v))/100

    volt_line, = ax1.plot(x, v, label="Voltage", color="#4b4efa")
    mag_line, = ax2.plot(x, m, label="mz", color="#f092fc")
    ax1.set_xlim(0, len(v)/100)
    ax2.set_xlim(0, len(v)/100)

    plt.legend()
    return volt_line, mag_line,


def animate_fsm_gnc(i):
    print(int((i/18989) * 20) * "-")
    # y = fsm_timer[1:i]
    # x = np.linspace(1, len(y), len(y))/100
    # line.set_data(x, y)
    # ax.set_xlim(0, len(y)/100)
    # line.set_color("#f584b1")
    #
    # y2 = my[1:i]
    # x2 = np.linspace(1, len(y), len(y))/100
    # line2.set_data(x2, y2)
    # ax.set_xlim(0, len(y)/100)
    # line2.set_color("#f5ee90")
    ax.set_title("Kalman Filter Data-Based")
    y3 = fsm_gnc[1:i]
    x3 = np.linspace(1, len(y3), len(y3))/100
    line3.set_data(x3, y3)
    ax.set_xlim(0, len(y3)/100)
    line3.set_color("#78caeb")
    # plt.legend()
    return  line3,

def animate_fsm_timer(i):
    print(int((i/18989) * 20) * "-")
    ax.set_title("Mostly Timer Based")
    y3 = fsm_timer[1:i]
    x3 = np.linspace(1, len(y3), len(y3))/100
    line3.set_data(x3, y3)
    ax.set_xlim(0, len(y3)/100)
    line3.set_color("#eb7a34")
    # plt.legend()
    return  line3,

def animate_fsm_6(i):
    print(int((i/18989) * 20) * "-")
    ax.set_title("Sensor Based, System Remembers Last 6 Datapoints")
    y3 = fsm_6[1:i]
    x3 = np.linspace(1, len(y3), len(y3))/100
    line3.set_data(x3, y3)
    ax.set_xlim(0, len(y3)/100)
    line3.set_color("#b3094d")
    # plt.legend()
    return  line3,

def animate_fsm_50(i):
    print(int((i/18989) * 20) * "-")
    ax.set_title("Sensor Based, System Remembers Last 50 Datapoints")
    y3 = fsm_50[1:i]
    x3 = np.linspace(1, len(y3), len(y3))/100
    line3.set_data(x3, y3)
    ax.set_xlim(0, len(y3)/100)
    line3.set_color("#7ead3d")
    # plt.legend()
    return  line3,




# call the animator.  blit=True means only re-draw the parts that have changed.
print("\nStarting GNC animation...\n")
anim1 = animation.FuncAnimation(fig, animate_fsm_gnc, init_func=init,
                               frames=FRAMES, interval=10, blit=True)
print("\nStarting Buffer 6 animation...\n")
anim2 = animation.FuncAnimation(fig, animate_fsm_6, init_func=init,
                               frames=FRAMES, interval=10, blit=True)
print("\nStarting Buffer 50 animation...\n")
anim3 = animation.FuncAnimation(fig, animate_fsm_50, init_func=init,
                               frames=FRAMES, interval=10, blit=True)
print("\nStarting Timer animation...\n")
anim4 = animation.FuncAnimation(fig, animate_fsm_timer, init_func=init,
                               frames=FRAMES, interval=10, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
anim1.save('vid_fsm_gnc.mp4', fps=FPS, extra_args=['-vcodec', 'libx264'])
anim2.save('vid_fsm_6.mp4', fps=FPS, extra_args=['-vcodec', 'libx264'])
anim3.save('vid_fsm_50.mp4', fps=FPS, extra_args=['-vcodec', 'libx264'])
anim4.save('vid_fsm_timer.mp4', fps=FPS, extra_args=['-vcodec', 'libx264'])
