import os.path
import numpy as np
import queries
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


# reposts, with number of followers per user.
reposts_columns = [#"feed_id", 
                   #"wbuser_id", 
                   "UNIX_TIMESTAMP(createts)", 
                   "followers_count", 
                   "reposts_count"]

feeds = [ #3417617421261823, 
          3552114468781517,
          3552406165618962,
          3553002100625578,
          3553148956059758,
          3553495522875305,
          3553707125513917,
          # 3553712896795463,
          3555028264477950,
          3556047518163949,
          3557169595179678]

#Note initial ordering is by TIME
def reposts_query(feed):
    return """SELECT %s FROM seeding_repost INNER JOIN seeding_wbuser ON seeding_repost.wbuser_id=seeding_wbuser.wbuserid WHERE feed_id=%d ORDER BY createts;""" % (", ".join(reposts_columns), feed)

data = {}

for feed in feeds:
    fname = "%d_repost_data.npy" % (feed)

    if os.path.isfile(fname):    
        data[feed] = np.load("%d_repost_data.npy" % (feed))
    else:
        data[feed] = netizenbase2numpy(reposts_query(feed),reposts_columns, save_as="%d_repost_data" % (feed))

    # clean out entries with 0 followers
    data[feed] = data[feed][data[feed].all(1)]

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
plt.show()

#plt.hist(np.log10(repost_data[:,1]),50)
#plt.title("histogram of log followers  per repost")
#plt.show()

#plt.hist(numpy.log10(repost_data[:,0]),50)
#plt.show()
fig = plt.figure()
for feed in feeds:
    plt.plot(np.sort(data[feed][:,2])[::-1])
plt.title("Repost count distribution, log/log")
plt.xlabel("users")
plt.xscale('log')
plt.ylabel("reposts")
plt.yscale('log')
plt.show()


fig = plt.figure()
for feed in feeds:
    plt.plot(data[feed][:,0],data[feed][:,1], label=str(feed))
plt.title("Number of followers of reposters over time")
plt.xlabel("time")
#plt.xscale('log')
plt.ylabel("number of reposts")
plt.yscale('log')
plt.legend()
plt.show()

fig = plt.figure()
for feed in feeds:
    plt.plot(data[feed][:,0],data[feed][:,2],'o',label=str(feed))
    
plt.title("Number of reposts over time")
plt.xlabel("time")
#plt.xscale('log')
plt.ylabel("number of reposts")
plt.yscale('log')
plt.legend()
plt.show()

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
plt.show()

#plt.hist(np.log10(flow_through),50)
#plt.title("histogram of log flow through rates per repost")
#plt.show()

fig = plt.figure()
for feed in feeds:
    plt.plot(data[feed][:,1],data[feed][:,2],'o')
plt.xlabel('num followers')
plt.xscale('log')
plt.ylabel('num reposts')
plt.yscale('log')
plt.show()



