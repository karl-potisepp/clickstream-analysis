import Pycluster
import numpy
def cluster(data, k=3):
    n = len(data)
    dist = numpy.zeros((n, n), numpy.float)

    for row in range(n):
        for col in range(n):
            dist[row][col] = jaccard_distance(data[row], data[col])
    
    clusterids, error, nfound = Pycluster.kmedoids(dist, nclusters=k)
    return clusterids
    
    
def print_results(labels, clusterids, stats):
    print "="*80
    clusters = {}
    for label, clusterid in zip(labels, clusterids):
        clusters.setdefault(clusterid, []).append(label)
    
    for clusterid, cluster_data in clusters.items():
        for itemset in cluster_data:
            print "[",
            for item in itemset:
                #TODO
                s = 0
                print item + "("+str(s)+"), ",
            print "]" 
        print "="*60
        
    
def jaccard_distance(first, second):
    s1 = set(first)
    s2 = set(second)
    d =  len(s1.intersection(s2)) / (len(s1.union(s2)) + 0.0)
    return 1.0 - d    

