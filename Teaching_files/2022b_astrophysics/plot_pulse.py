#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rcParams.update({'font.size':18})

q = 1.0
b = 1.0
beta  = 0.9
gamma = 1.0/np.sqrt(1.0-beta**2)

vt_min = -2.1
vt_max =  2.1
nvt    = 201

vt = np.arange(nvt)/(nvt-1.0)*(vt_max - vt_min) + vt_min

f  = (gamma**2 * vt**2/b**2 + 1.0)**(1.5)
Ex = -q/b**2 * gamma*(vt/b)/f
Ey =  q/b**2 * gamma/f

scale   = 1.0
fig, ax = plt.subplots(1,1, figsize=(10.0,10.0))
Q       = ax.quiver(0.0, b, 0.0, 0.0, scale=scale, angles='xy', scale_units='xy')
point,  = ax.plot(-1000.0, 0.0, linestyle='None', marker='o')
line,   = ax.plot([None,0.0], [0.0,None], linestyle=':', color='r')
plot2,  = ax.plot(Ex,Ey+b,linestyle=':', color='g')

ax.plot([vt_min, vt_max], [0.0, 0.0],linestyle=':', color='r')
ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-0.5, 3.5)
ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$y$')
ax.set_title(r'Electric Field Vector')

def init():
    U = Ex[0]
    V = Ey[0]
    Q.set_UVC(U, V)
    point.set_data([vt[0]], [0.0])
    #line.set_data([vt[0],0.0], [0.0,b])
    line.set_data([None,0.0], [0.0,None])
    return Q, point, line

def update_quiver(iframe, Q, Ex, Ey, point, line):
    U = Ex[iframe]
    V = Ey[iframe]
    Q.set_UVC(U, V)
    point.set_data([vt[iframe]], [0.0])
    line.set_data([vt[iframe],0.0], [0.0,b])
    return Q, point, line

ani = animation.FuncAnimation(fig, update_quiver, init_func=init,fargs=(Q, Ex, Ey, point, line),
                              frames=nvt, interval=200, blit=True, repeat_delay=1000)

#plt.show()

#-- make mp4 file.
#-- (to do this, you need to install "ffmpeg". "sudo port install ffmpeg" in macos, "sudo apt install ffmpeg" in Linux.
fname0   = 'ani_pulse'
Writer   = animation.writers['ffmpeg']
metadata = dict(title=r'%s' % fname0, artist='K.-I. Seon')
duration = 10.0   # in sec
fps      = nvt/duration
writer   = Writer(metadata=metadata, fps=fps)
#ani.save(fname0+'_ani.mp4', dpi=dpi,writer=writer)
ani.save(fname0+'.mp4', writer=writer)
