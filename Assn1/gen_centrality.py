from tqdm import tqdm
import os
import sys

import snap
Rnd = snap.TRnd(42)
Rnd.Randomize()

def compute_closeness_centrality(G : snap.TUNGraph, save_path: str) :
    '''
        Function to compute closeness centrality of each node in the graph.

        Variables:
        - cc_dict : stoes id and closeness centrality of each node
        - shortestPaths : returns length of shortest paths from source node to all other nodes

    '''
    cc_dict = dict()
    for N in tqdm(G.Nodes()):
        id = N.GetId()
        _, shortestPaths = G.GetShortPathAll(id)    # compute shortest path lengths from given node to all other nodes
        sum_paths = sum([shortestPaths[i] for i in shortestPaths if i!=id])  
        cc = (G.GetNodes() - 1) / sum_paths    # compute closeness centrality for given node
        if cc > 1:  # if graph is not connected, cc may be greater than 1
            cc = 0

        cc_dict[id] = cc
        
    cc_sorted = sorted(cc_dict.items(), key=lambda x: x[1], reverse=True)

    filename = "closeness.txt"
    filepath = os.path.join(save_path, filename)

    with open(filepath, 'w') as f:
        for id, cc in cc_sorted:
            f.write("%d %.6f\n" % (id, cc))

    top_100_cc = [id for id, _ in cc_sorted[:100]]   # top 100 nodes based on closeness centrality
    return top_100_cc


def compute_betweenness_centrality(G : snap.TUNGraph, save_path: str) :
    '''
        Function to compute betweenness centrality for each node using Brandes algorithm. 

        Steps : 

            Forward phase :
                - For each node s in the unweighted graph, use BFS traversal to compute sigma, storing no. of shortest paths from s to each node
                - Also, store a list of predecessors of each node to compute dependency later

            Backward phase :
                - For each intermediate node v that lies on one of the shortest paths from s to some other node, increment 
        Variables:

        - stack: stack of nodes in order of distance from s
        - prev: list of predecessors of each node
        - sigma: number of shortest paths from s to each node
        - dist: shortest path length from s to each node
        - delta: one-sided dependency of each node on s
    '''
    betweenness = {N.GetId(): 0 for N in G.Nodes()}  # initialize betweenness centrality to 0 for each node

    for s in tqdm(G.Nodes()):
        # initialize variables
        stack = []
        prev = dict()
        sigma = dict()

        # initialize predecessors and sigma
        for v in G.Nodes():
            id = v.GetId()
            prev[id] = []
            if id == s.GetId():
                sigma[id] = 1
            else:
                sigma[id] = 0

        # initialize distance from source node
        dist = dict()
        dist[s.GetId()] = 0

        # initialize BFS queue
        queue = []
        queue.append(s.GetId())

        # Forward phase : BFS traversal
        while len(queue) > 0:
            v = queue.pop(0)
            stack.append(v)
            for w in G.GetNI(v).GetOutEdges():
                if w not in dist:
                    queue.append(w)
                    dist[w] = dist[v] + 1
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    prev[w].append(v)

        # initialize dependency vector delta
        delta = dict()
        for v in G.Nodes():
            delta[v.GetId()] = 0    

        # Backward phase : compute dependency
        while len(stack) > 0:
            w = stack.pop()
            for v in prev[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])  # compute dependency of v on w
            if w != s.GetId():
                betweenness[w] += delta[w]

    # normalize betweenness by multiplying by 2/(n-1)(n-2)
    N = G.GetNodes()
    factor = 2 / ((N - 1) * (N - 2))
    betweenness = {id: factor * bw for id, bw in betweenness.items()}

    betweenness_sorted = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)

    filename = "betweenness.txt"
    filepath = os.path.join(save_path, filename)

    with open(filepath, 'w') as f:
        for id, bw in betweenness_sorted:
            f.write("%d %.6f\n" % (id, bw))

    top_100_bw = [id for id, _ in betweenness_sorted[:100]]  # top 100 nodes based on betweenness centrality
    return top_100_bw


def compute_biased_pagerank(G : snap.TUNGraph, alpha: float, save_path: str) :
    '''
        Function to compute biased pagerank for each node in the graph.
    '''
    # function to check convergence of pagerank
    def check_convergence(PR, prev_PR):
        max = -1
        for id, pr in PR.items():
            if max < abs(pr - prev_PR[id]):
                max = abs(pr - prev_PR[id])
        
        if max > 1e-10:  # check if difference between pagerank vectors is less than threshold
            return False
        return True
    priority_nodes = [node.GetId() for node in G.Nodes() if node.GetId()%4==0]
    N = G.GetNodes()
    S = len(priority_nodes)
    d = {}

    # initialize biased preference vector
    for node in G.Nodes():
        id = node.GetId()
        if S!=0:    # if there are priority nodes
            if id%4==0:
                d[id] = 1/S
            else:
                d[id] = 0
        else:
            d[id] = 1/N

    # initialize pagerank vector
    PR = {id: pr for id, pr in d.items()}
    prev_PR = PR.copy()

    # iterate until convergence
    while(1):
        for N in G.Nodes():
            t = 0
            for v in N.GetOutEdges():
                t += PR[v]/G.GetNI(v).GetOutDeg()
            PR[N.GetId()] = alpha*t + (1-alpha)*d[N.GetId()]

        #normalize PR values
        sum_pr = sum(PR.values())
        PR = {id: pr/sum_pr for id, pr in PR.items()}

        # check for convergence
        if check_convergence(PR, prev_PR):
            break

        prev_PR = PR.copy() # update previous pagerank vector

    PR_sorted = sorted(PR.items(), key=lambda x: x[1], reverse=True)

    filename = "pagerank.txt"
    filepath = os.path.join(save_path, filename)

    with open(filepath, 'w') as f:
        for id, pr in PR_sorted:
            f.write("%d %.6f\n" % (id, pr))

    top_100_pr = [id for id, _ in PR_sorted[:100]]  # top 100 nodes based on pagerank
    return top_100_pr

def main(args):
    filepath = args[1]
    save_path = "centralities"
    os.makedirs(save_path, exist_ok=True)
    G = snap.LoadEdgeList(snap.TUNGraph, filepath)    
    alpha = 0.8

    top_100_closeness = compute_closeness_centrality(G, save_path)
    top_100_betweenness = compute_betweenness_centrality(G, save_path)
    top_100_pagerank = compute_biased_pagerank(G, alpha, save_path)

    # find intersection of top 100 nodes by closeness, betweenness and pagerank
    inf_nodes = list(set(top_100_closeness) & set(top_100_betweenness) & set(top_100_pagerank))
    print("Number of influencer nodes: ",len(inf_nodes))
    
if __name__ == "__main__":
    main(sys.argv)