# -*- coding: utf-8 -*-
"""
Created on Tue Feb 04 17:36:31 2014

@author: yangg_000
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from slab import SlabFile, h5File
from glob import glob
from time import time, sleep

from data_cursor_example import DataCursor, FollowDotCursor

fns = glob('..\\*.h5')
print "all h5 files found: ", fns
with h5File(fns[1], 'r') as f:
    mags_Vtrap = np.array(f['mag'][...])
with h5File(fns[0], 'r') as f:
    mags_Vres = np.array(f['mag'][...])
TwoDMapFn = "S:\\_Data\\131021 - EonHe M007v5 Trident\\010_2dhysteresis\\140123_M007v5Trident-puff_60_008\\M007v5Trident-puff_60-Small.h5"
print "getting ",TwoDMapFn
MapFn = {};
with h5File(TwoDMapFn, 'r') as f:
    MapFn['resV'] = np.array(f['resV'][...])
    MapFn['trapV'] = np.array(f['trapV'][...])
    MapFn['fits'] = np.array(f['fits'][...])
    start, end = [12433, 16451]

#plt.imshow(mags_Vtrap)
#plt.show()

fig = plt.figure()
fig.canvas.set_window_title('Trap in a Box')
ax1 = plt.subplot(121)
plt.subplots_adjust(left=0.25, bottom=0.25)
ax1.axis([0, 451, 0, 451])
ax2 = plt.subplot(122)
ax2.axis([-0.8, 1.6, -0.8, 1.6])
im = ax1.imshow(mags_Vres, interpolation='none')
resVpts = MapFn['resV'][start:end]
trapVpts = MapFn['trapV'][start:end]
trapMap = ax2.scatter(resVpts,trapVpts,c=MapFn['fits'][2][start:end],s=13,marker="s",edgecolor='none',linewidth=0,alpha=0.7)

axcolor = 'lightgoldenrodyellow'
axRes = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
axTrap  = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)

res0 = 1.5
trap0 = 0.8
rescale=False;
sRes = Slider(axRes, 'Resonator Voltage', -1.6, 5.0, valinit=res0)
sTrap = Slider(axTrap, 'Trap Voltage', -1.6, 5.0, valinit=trap0)

def update(val, resV=None, trapV=None):
    if resV == None:
        resV = sRes.val
    if trapV == None:
        trapV = sTrap.val
    image = mags_Vtrap*trapV + mags_Vres*resV
    im.set_data(image)
    if rescale:
        im.set_clim(image.min(), image.max())
    fig.canvas.draw_idle()
def updateWrapper(x, y):
    update(None, resV=x, trapV=y)

FollowDotCursor(ax2, resVpts, trapVpts, callback=updateWrapper)
sRes.on_changed(update)
sTrap.on_changed(update)

axRescale = plt.axes([0.8, 0.225, 0.1, 0.04])
btnRescale = Button(axRescale, 'Rescale', color=axcolor, hovercolor='0.975')

def rescaleToggle(event):
    update(None);
    global rescale
    if rescale == True:
        rescale = False
        btnRescale.label = 'turn on rescale'
    else:
        rescale = True
        btnRescale.label = 'turn off rescale'
btnRescale.on_clicked(rescaleToggle)


resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
def reset(event):
    sRes.reset()
    sTrap.reset()
button.on_clicked(reset)

rax = plt.axes([0.025, 0.5, 0.15, 0.15], axisbg=axcolor)
radio = RadioButtons(rax, ('on', 'off'), active=0)
def colorfunc(label):
    fig.canvas.draw_idle()
radio.on_clicked(colorfunc)

plt.show()