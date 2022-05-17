import matplotlib.pyplot as plt
import matplotlib as mpl
import csv
from numpy import *

from mpl_toolkits.mplot3d.art3d import Poly3DCollection

header = []
x = []
y = []
z = []

file = open('1Timeout.csv', 'r')
data = csv.reader(file, delimiter = ',')
header = next(data)

for line in data:
    x.append(float(line[0]))
    y.append(float(line[1]))
    z.append(float(line[2]))

# initialize figure
fig = plt.figure()

# make 3D plot
ax = fig.add_subplot(111, projection='3d')

# plot data
#scat = ax.scatter(x, y, z, c=z, s=2, cmap='viridis', marker=',')
#ax.plot3D(x,y,z)
# polygons below function instead of fill between
#ax.fill_between(x, y, 0, color='white', alpha=.2)

lines = ax.plot(x,y,z,label="line plot")
for x in range(len(lines)):
    print(lines[x].get_data_3d())
# label plot
ax.set_title("Waterfall Plot")
#ax.set_xlabel("time (s)")
#ax.set_ylabel("freq (mHz)")
#ax.set_zlabel("dBm (RX power)")

# color bar
""" condense to line below
cmap = mpl.cm.get_cmap('viridis')
norm = mpl.colors.Normalize(vmin= min(z), vmax= max(z))
fig.colorbar(mpl.cm.ScalarMappable(cmap=cmap, norm=norm), ax=ax)
"""
#fig.colorbar(scat)

# show plot
plt.show()

#DIDN'T WORK
"""
fig, ax = plt.subplots()
colorbar = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                      #   norm=norm,
                                        # orientation='horizontal')
#plt.colorbar()
#ax.colorbar(pos, ax=ax1)
plt.show()
                                        
"""
""" working graph 
ax = plt.axes(projection="3d", location='left')
ax.plot(x, y, z)
ax.set_title("Waterfall Plot")
"""

#OLD CODE
"""
ax = plt.axes(projection="3d")
# print single points
# ax.scatter(100,100,100) # print single points

# Scatter Plots

x_data = np.random.randint(0, 100, 500) # 500 random points between 0-100
y_data = np.random.randint(0, 100, 500)
z_data = np.random.randint(0, 100, 500)
ax.scatter(x_data, y_data, z_data, marker="v", alpha=0.1)
"""

# Plot Function
"""
x_data = np.arange(0, 50, 0.1) #(start, end, step size)
y_data = np.arange(0, 50, 0.1)
z_data = x_data * y_data # function we want to make

ax.plot(x_data, y_data, z_data)
ax.set_title("Test")
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
ax.set_zlabel("Z axis")

# Surface Plot
x_data = np.arange(0,50,0.1)
y_data = np.arange(0,50,0.1)

X, Y = np.meshgrid(x_data, y_data)
Z = np.sin(X) * np.cos(Y)
ax.plot_surface(X,Y,Z, cmap="plasma")
plt.show()

"""