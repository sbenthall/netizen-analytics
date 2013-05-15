from NButils import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

data = load_repost_data(feeds)

foo = np.ones((1,1))

#For N reposts, returns an N x N matrix
#estimating for each repost the likelihood
#that any other entry was its parent

def reconstruct_lineage_forward(reposts):
    n = reposts.shape[0] # number of reposts
    recorded_reposts = np.sum(reposts[:,2]);

    lineage = zeros((n, n))

    #number of followers of user reposting
    followers = reposts[:,1]
    
    #variables to increment
    #number of reposts unaccounted for by reposts_count
    #don't count the first one
    unrecorded = n - recorded_reposts - 1

    #recorded subsequent repost weight for each post
    weights = np.copy(reposts[:,2])

    for repost_i in range(1,n):

        print(np.sum(weights[0:repost_i]), unrecorded)
        #probability of being a recorded repost
        p_recorded = np.sum(weights[0:repost_i]) / (np.sum(weights[0:repost_i]) + unrecorded)

        #if recorded, likelihood of having a particular parent
        if p_recorded > 0:
            parent_likelihood_recorded = weights[0:repost_i] / np.sum(weights[0:repost_i])
        else:
            # don't divide by zero if there are no recorded reposts yet
            parent_likelihood_recorded = zeros((1,repost_i))
        
        #if unrecorded, likelihood of having a particular parent
        parent_likelihood_unrecorded = followers[0:repost_i] / np.sum(followers[0:repost_i])

        # add padding
        plr_padded = np.hstack((np.atleast_2d(parent_likelihood_recorded), zeros((1, n - repost_i))))
        plu_padded = np.hstack((np.atleast_2d(parent_likelihood_unrecorded), zeros((1, n - repost_i))))

        lineage[repost_i,:] = p_recorded * plr_padded + (1 - p_recorded) * plu_padded
        if not (np.sum(lineage[repost_i,:]) > .99999 and np.sum(lineage[repost_i,:]) < 1.00001):
            print(np.sum(lineage[repost_i,:]))
            import pdb; pdb.set_trace()

        weights -= np.squeeze(p_recorded * plr_padded)
        unrecorded -= (1 - p_recorded)

    return lineage

# Whereas the above algorithm attempts to allocate
# probability moving forward through the posts in time,
# this algorithm starts from the latest post,
# reallocating probability when it encounters
# recorded reposts.
#
def reconstruct_lineage_backward(reposts):
    n = reposts.shape[0] # number of reposts
    recorded_reposts = np.sum(reposts[:,2]);

    lineage = zeros((n, n))

    #number of followers of user reposting
    followers = reposts[:,1]
    
    #variables to increment
    #number of reposts unaccounted for by reposts_count
    #don't count the first one
    unrecorded = n - recorded_reposts - 1

    #recorded subsequent repost weight for each post
    weights = np.copy(reposts[:,2])

    for post_i in range(n-1,1,-1):

        #if unrecorded, likelihood of having a particular parent
        parent_likelihood_unrecorded = followers[0:post_i] / np.sum(followers[0:post_i])
        plu_padded = np.hstack((np.atleast_2d(parent_likelihood_unrecorded), zeros((1, n - post_i))))
        lineage[post_i,:] = plu_padded

        if weights[post_i] > 0:
            p_reposted_from_this = weights[post_i] / (n - post_i)
            lineage[post_i+1:n,post_i+1:n] = lineage[post_i+1:n,post_i+1:n] * (1 - p_reposted_from_this)
            lineage[post_i+1:n,post_i] = np.ones((n-post_i-1,1)).squeeze() * p_reposted_from_this

        if not (np.sum(lineage[post_i,:]) > .99999 and np.sum(lineage[post_i,:]) < 1.00001):
            print(np.sum(lineage[post_i,:]))
            import pdb; pdb.set_trace()

    return lineage


def lineage_depths(lineage):
    n = lineage.shape[0]
    
    depths = zeros((n,1))

    for i in range(1,n):
        depths[i] = 1 + np.dot(lineage[i,:], depths)

    return depths

def lineage_descendents(lineage):
    n = lineage.shape[0]

    descendents = zeros((n,1))

    for k in range(n-1,0,-1):
        desc = np.dot(lineage[:,k], 1 + descendents)

        descendents[k] = desc

    return descendents

lineages = list()

for k,d in data.items():
    lineage = reconstruct_lineage_backward(d)
    lineages.append(lineage)
    #print(lineage)
    print(k)

    fig = plt.figure()
    plt.imshow(lineage, cmap=cm.spectral)
    plt.title("Probabilistic lineage of reposts for feed %d" % (k))
    plt.xlabel("Parent post")
    plt.ylabel("Posts in chronological order")
    #plt.show()

    depths = lineage_depths(lineage)
    descendents = lineage_descendents(lineage)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(depths,'bo')
    ax1.set_xlabel('Chronologically ordered posts')
    ax1.set_ylabel('Expected depths',color='b')
    for tl in ax1.get_yticklabels():
        tl.set_color('b')

    ax2 = ax1.twinx()
    ax2.plot(descendents,'r.')
    ax2.plot(d[:,2],'g.')
    ax2.set_ylabel('Expected total descendents',color='r')
    ax2.set_yscale('log')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')

    plt.show()


