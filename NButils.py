import MySQLdb
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

