import MySQLdb
import os.path

import numpy as np
from numpy import array, zeros, asarray

# Connect to database, query data, convert to numpy array
# return or optionally save if save_as filename is included
def netizenbase2numpy(query,columns, host="localhost", user="root", password="root", db_name="netizenbase", save_as=None):
    db = MySQLdb.connect(host, user, password, db_name)

    cursor = db.cursor()
    num_rows = cursor.execute(query)

    data = zeros((num_rows,len(columns)))

    i = 0
    for row in cursor:
        row_array = asarray(row).T
        data[i,:] = row_array 
        i += 1
    
    db.close()

    if save_as is not None:
        np.save(save_as,data)

    return data



## SETUP FOR REPOST STUDIES


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
          #3553002100625578,
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


def load_repost_data(feeds):
    data = {}
    for feed in feeds:
        fname = "%d_repost_data.npy" % (feed)

        if os.path.isfile(fname):
            data[feed] = np.load("%d_repost_data.npy" % (feed))
        else:
            data[feed] = netizenbase2numpy(reposts_query(feed),reposts_columns, save_as="%d_repost_data" % (feed))

            # clean out entries with 0 followers
            data[feed] = data[feed][data[feed].all(1)]

    return data
