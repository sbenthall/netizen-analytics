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
    n = reposts.shape[0] # number of reposts
    recorded_reposts = np.sum(reposts[:,2]);
    print((n,recorded_reposts))

    lineage = zeros((n, n))

    #number of followers of user reposting
    followers = reposts[:,1]
    
    #variables to increment
    #number of reposts unaccounted for by reposts_count
    #don't count the first one
    unrecorded = n - recorded_reposts - 1
    print("Unrecorded reposts: %d" % (unrecorded))

    #recorded subsequent repost weight for each post
    weights = np.copy(reposts[:,2])

    for repost_i in range(1,n):
        #import pdb; pdb.set_trace()
        #probability of being a recorded repost
        print(np.sum(weights[0:repost_i]), unrecorded)

        p_recorded = np.sum(weights[0:repost_i]) / (np.sum(weights[0:repost_i]) + unrecorded)
        #print("Probability recorded: %s"% (str(p_recorded)))

        #if recorded, likelihood of having a particular parent
        if p_recorded > 0:
            parent_likelihood_recorded = weights[0:repost_i] / np.sum(weights[0:repost_i])
        else:
            parent_likelihood_recorded = zeros((1,repost_i))
        
        #if unrecorded, likelihood of having a particular parent
        parent_likelihood_unrecorded = followers[0:repost_i] / np.sum(followers[0:repost_i])

        #print("PLR: %s" % (str(parent_likelihood_recorded)))
        #print("PLU: %s" % (str(parent_likelihood_unrecorded)))

        # add padding
        plr_padded = np.hstack((np.atleast_2d(parent_likelihood_recorded), zeros((1, n - repost_i))))
        plu_padded = np.hstack((np.atleast_2d(parent_likelihood_unrecorded), zeros((1, n - repost_i))))

        lineage[repost_i,:] = p_recorded * plr_padded + (1 - p_recorded) * plu_padded
        if not (np.sum(lineage[repost_i,:]) > .99999 and np.sum(lineage[repost_i,:]) < 1.00001):
            print(np.sum(lineage[repost_i,:]))
            import pdb; pdb.set_trace()
        #print(lineage[repost_i,0:repost_i+1])
        weights -= np.squeeze(p_recorded * plr_padded)
        unrecorded -= (1 - p_recorded)

    return lineage

for k,d in data.items():
    lineage = reconstruct_flow(d)
    #print(lineage)
    print(k)
    plt.imshow(lineage, cmap=cm.spectral)
    plt.title("Probabilistic lineage of reposts for feed %d" % (k))
    plt.xlabel("Parent post")
    plt.ylabel("Posts in chronological order")
    plt.legend()
    plt.show()
