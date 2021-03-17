#Import necessary libraries
import numpy as np
import matplotlib.pyplot as mpl
import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord

#Read the pulsar data in csv format
#The data is in ICRS coordinate system
data_pulsar = pd.read_csv('data.csv')

#Assigning the Data to the array
pulsar_ra = data_pulsar.RA #Unit is in Degree
pulsar_dec = data_pulsar.Dec #Unit is in Degree
pulsar_distance = data_pulsar.Distance #Unit is in kiloparsec kpc

#Assigning to more convenient way
pulsar_icrs = SkyCoord(pulsar_ra[:], pulsar_dec[:], frame='icrs', unit=u.deg)

#Remember, the data is in ICRS coordinate
#The data must be converted to Galactic Coordinate System
pulsar_gal = pulsar_icrs.galactic

#Test
# print(pulsar_icrs[1])
# print(pulsar_gal[1])

#Converting to Aitoff Projection
pulsar_gal_l = pulsar_gal.l.radian
pulsar_gal_l[pulsar_gal_l > np.pi] -= 2. * np.pi
pulsar_gal_b = pulsar_gal.b.radian

'''
Plotting in Aitoff Projection
'''
#Aitoff Projection Plotting 
fig = mpl.figure(figsize=(8,5))
ax = fig.add_subplot(1,1,1, projection='aitoff')
ax.scatter(-pulsar_gal_l, pulsar_gal_b, s=0.5, color='red', alpha=1) #The reason why negative for galactic is because "mapping from inside issue
ax.grid()

#Renaming Galactic Longitude Axis to conventional format
mpl.xticks(ticks=np.radians([-150, -120, -90, -60, -30, 0, \
                             30, 60, 90, 120, 150]),
           labels=['150°', '120°', '90°', '60°', '30°', '0°', \
                   '330°', '300°', '270°', '240°', '210°'])
 
#Settings for Plotting    
titlefont = {'fontname':'Arial'}
mpl.title(label="Pulsar Distribution in Galactic Coordinate System\n(Aitoff Projection)", fontsize=15, y=1.1, **titlefont)
mpl.legend(["Pulsar"], bbox_to_anchor=(1.1, 0.9), markerscale=25)
ax.set_xlabel("Galactic Longitude, l", x=0.6)
ax.set_ylabel("Galactic Latitude, b")
fig.show()
mpl.tight_layout()
mpl.savefig('PulsarInAitoffProjection.jpg', dpi=500)

'''
Plotting in Equal
'''
fig = mpl.figure(figsize=(8,5))
ax = fig.add_subplot(1,1,1, aspect='equal')
ax.scatter(pulsar_gal.l.degree, pulsar_gal.b.degree, s=0.5, color='red', alpha=1)
ax.set_xlim(360., 0.)
ax.set_ylim(-90., 90.)
ax.grid()
titlefont = {'fontname':'Arial'}
mpl.title(label="Pulsar Distribution in Galactic Coordinate System\n(Equal Projection)", fontsize=15, **titlefont)
ax.set_xlabel("Galactic Longitude, l")
ax.set_ylabel("Galactic Latitude, b")
fig.show()
mpl.tight_layout()
mpl.savefig('PulsarInEqualProjection.jpg', dpi=500)

'''
Plotting in 3D Projection
'''
#Creating dataset
z = pulsar_gal.b.degree
x = pulsar_gal.l.degree
y = pulsar_distance

#Creating figure
fig = mpl.figure(figsize = (10, 7))
ax = mpl.axes(projection ="3d")

#To distiguish the distance, colormap is used
distance_cmap = mpl.get_cmap('CMRmap')
 
#Creating plot
plt = ax.scatter3D(x, y, z, s=2, c = y, cmap = distance_cmap)

mpl.title("Pulsar Distribution in Galactic Coordinate System\n(3D Projection)",fontsize=15)
ax.set_xlabel("Galactic Longitude, l (deg)",fontsize=15)
ax.set_ylabel("Distance, d (kpc)",fontsize=15)
ax.set_zlabel("Galactic Latitude, b (deg)",fontsize=15) 
cbar = fig.colorbar(plt, ax = ax, shrink = 0.5, aspect = 5)
cbar.ax.set_ylabel('Distance in kpc', rotation=270)

#show plot
fig.show()
mpl.tight_layout()
mpl.savefig('PulsarDistance3D.jpg', dpi=500)
