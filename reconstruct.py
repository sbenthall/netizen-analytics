from NButils import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

data = load_repost_data(feeds)

foo = np.ones((1,1))

#For N reposts, returns an N x (N + 1) matrix
#estimating for each repost the likelihood
#that any other entry was its parent
#
# The first column of this matrix captures residual probability
# due to uncounted reposts.  It's a hack.
def reconstruct_flow(reposts):
    n = reposts.shape[0]
    lineage = zeros((n, n +1))

    #
    weights = np.hstack((np.array([1]),np.copy(reposts[:,2])))

    for repost_i in range(2,n):
        #print(weights)
        expected_parents = weights[0:repost_i] / np.sum(weights[0:repost_i])

        ep_padded = np.hstack((np.atleast_2d(expected_parents), zeros((1, n + 1 - repost_i))))

        lineage[repost_i,:] = ep_padded
        weights -= np.squeeze(ep_padded)
        weights[0] = 1

    return lineage


lineage = reconstruct_flow(data[feeds[2]])

print(lineage)
plt.imshow(lineage, cmap=cm.hot)
plt.show()
