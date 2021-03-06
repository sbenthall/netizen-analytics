import os.path
import numpy as np
from NButils import *
from numpy import array, zeros, asarray
import MySQLdb
import matplotlib.pyplot as plt
from pylab import axes,axis

'''

Feeds data:

+------------------+---------------+
| wbfeedid         | reposts_count |
+------------------+---------------+
| 3417617421261823 |          3256 |
| 3552114468781517 |          2339 |
| 3552406165618962 |           144 |
| 3553002100625578 |         10509 |
| 3553148956059758 |          3832 |
| 3553495522875305 |           677 |
| 3553707125513917 |           831 |
| 3553712896795463 |          NULL |
| 3555028264477950 |           842 |
| 3556047518163949 |          2000 |
| 3557169595179678 |          1184 |
+------------------+---------------+
'''


data = load_repost_data(feeds)

#plt.hist(numpy.log10(repost_data[:,1]),50)
#plt.show()

#plt.hist(numpy.log10(repost_data[:,0]),50)
#plt.show()
fig = plt.figure()
for feed in feeds:
    plt.plot(np.sort(data[feed][:,1])[::-1])
plt.title("Reposting users follower distribution, log/log")
plt.xlabel("users")
plt.xscale('log')
plt.ylabel("followers")
plt.yscale('log')
#plt.show()

#plt.hist(np.log10(repost_data[:,1]),50)
#plt.title("histogram of log followers  per repost")
#plt.show()

#plt.hist(numpy.log10(repost_data[:,0]),50)
#plt.show()
fig = plt.figure()
for feed in feeds:
    plt.plot(np.sort(data[feed][:,2])[::-1],'o')
plt.title("Repost count distribution, log/log")
plt.xlim(xmax=5000)
plt.xlabel("users")
plt.xscale('log')
#plt.ylim(ymax=1000)
plt.ylabel("reposts")
plt.yscale('log')
#plt.show()


fig = plt.figure()
for feed in feeds:
    plt.plot(data[feed][:,0], data[feed][:,1], label=str(feed))
plt.title("Number of followers of reposters over time")
plt.xlabel("time")
#plt.xscale('log')
plt.ylabel("followers")
plt.yscale('log')
plt.legend()
#plt.show()

fig = plt.figure()
for feed in feeds:
    plt.plot(data[feed][:,0],data[feed][:,2],'o',label=str(feed))
    
plt.title("Number of reposts over time")
plt.xlabel("time")
#plt.xscale('log')
plt.ylabel("number of reposts")
plt.yscale('log')
plt.legend()
#plt.show()

#plt.hist(np.log10(repost_data[:,2]),50)
#plt.title("histogram of log reposts through rates per repost")
#plt.show()

flow = {}
for feed in feeds:
    flow[feed] = data[feed][:,1] / data[feed][:,0]

fig = plt.figure()
for feed in feeds:
    plt.plot(data[feed][:,0],flow[feed],label=str(feed))
plt.title("flow through plot over time")
plt.yscale('log')
plt.legend()
#plt.show()

fig = plt.figure()
for feed in feeds:
    plt.hist(np.log10(flow[feed]),50) #, histtype='bar')
plt.title("histogram of log flow through rates per repost")
plt.xlabel("log flow rate")
plt.ylabel("number of reposts")
plt.show()

fig = plt.figure()
for feed in feeds:
    plt.plot(data[feed][:,1],data[feed][:,2],'o')
plt.xlabel('num followers')
plt.xscale('log')
plt.ylabel('num reposts')
plt.yscale('log')

plt.show()



