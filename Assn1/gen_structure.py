import os
import sys
import snap
from tqdm import tqdm
import time

Rnd = snap.TRnd(42)
Rnd.Randomize()
 
def compute_graph_size(G : snap.TUNGraph) :
    '''
        Function to compute number of nodes and edges in the graph.
    '''
    print("Number of nodes:", G.GetNodes())
    print("Number of edges:", G.GetEdges())


def compute_graph_degree(G : snap.TUNGraph, filepath : str) :
    '''
        Function to compute degree distribution of the graph.
    '''
    CntV = G.GetOutDegCnt()
    deg_dist = {}
    for p in CntV:  # convert CntV to a dictionary
        deg_dist[p.GetVal1()] = p.GetVal2()

    # Print number of nodes with degree 7
    try:
        print("Number of nodes with degree=7:", deg_dist[7])
    except KeyError:
        print("Number of nodes with degree=7: 0")

    # Find node id(s) with highest degree
    max_deg = max(deg_dist.keys())
    max_deg_nodes = []
    for N in G.Nodes():
        if N.GetOutDeg() == max_deg:
            max_deg_nodes.append(str(N.GetId()))
    print("Node id(s) with highest degree:", ", ".join(max_deg_nodes))

    # Plot degree distribution
    subgraph_name = filepath.split('/')[-1].split('.')[0]
    os.makedirs("plots", exist_ok=True)
    os.chdir("plots")

    G.PlotOutDegDistr("deg_dist_" + subgraph_name, "Degree Distribution")
    os.rename("outDeg.deg_dist_" + subgraph_name + ".png", "deg_dist_" + subgraph_name + ".png")
    os.remove("outDeg.deg_dist_" + subgraph_name + ".tab")
    os.remove("outDeg.deg_dist_" + subgraph_name + ".plt")
    os.chdir("..")


def compute_graph_path(G : snap.TUNGraph, num_nodes : int, filepath : str) :
    '''
        Function to compute shortest path distribution of the graph.
    '''

    fullDiam = G.GetBfsFullDiam(num_nodes, False)
    print("Approximate full diameter: %d" % fullDiam)
    effDiam = G.GetBfsEffDiam(num_nodes, False)
    print("Approximate effective diameter: %d" % effDiam)

    subgraph_name = filepath.split('/')[-1].split('.')[0]
    os.makedirs("plots", exist_ok=True)
    os.chdir("plots")
    
    G.PlotShortPathDistr("shortest_path_" + subgraph_name, "Shortest Path Distribution")
    os.rename("diam.shortest_path_" + subgraph_name + ".png", "shortest_path_" + subgraph_name + ".png")
    os.remove("diam.shortest_path_" + subgraph_name + ".tab")
    os.remove("diam.shortest_path_" + subgraph_name + ".plt")
    os.chdir("..")


def compute_graph_comp(G : snap.TUNGraph, filepath : str) :

    MxScc = G.GetMxScc()
    mxNodes = MxScc.GetNodes()
    totalNodes = G.GetNodes()
    print("Fraction of nodes in largest connected component: %.4f" % (mxNodes/totalNodes))

    edBridges = G.GetEdgeBridges()
    print("Number of edge bridges: ", len(edBridges))

    artPts = G.GetArtPoints()
    print("Number of articulation points: ", len(artPts))

    subgraph_name = filepath.split('/')[-1].split('.')[0]
    os.makedirs("plots", exist_ok=True)
    os.chdir("plots")
    
    G.PlotSccDistr("connected_comp_" + subgraph_name, "Connected Component Distribution")
    os.rename("scc.connected_comp_" + subgraph_name + ".png", "connected_comp_" + subgraph_name + ".png")
    os.remove("scc.connected_comp_" + subgraph_name + ".tab")
    os.remove("scc.connected_comp_" + subgraph_name + ".plt")
    os.chdir("..")

def compute_graph_connectivity(G : snap.TUNGraph, filepath : str) :

    AvgCF = G.GetClustCf(-1)
    print("Average clustering coefficient: %.4f" % (AvgCF))

    numTriads = G.GetTriads()
    print("Number of triads: ", numTriads)

    nId = G.GetRndNId(Rnd)
    print("Clustering coefficient of random node %d: %.4f" % (nId, G.GetNodeClustCf(nId)))

    nId = G.GetRndNId(Rnd)
    print("Number of triads random node %d participates: %d" % (nId, G.GetNodeTriads(nId)))

    subgraph_name = filepath.split('/')[-1].split('.')[0]
    os.makedirs("plots", exist_ok=True)
    os.chdir("plots")
    
    G.PlotClustCf("clustering_coeff_" + subgraph_name, "Clustering Coefficient Distribution")
    os.rename("ccf.clustering_coeff_" + subgraph_name + ".png", "clustering_coeff_" + subgraph_name + ".png")
    os.remove("ccf.clustering_coeff_" + subgraph_name + ".tab")
    os.remove("ccf.clustering_coeff_" + subgraph_name + ".plt")
    os.chdir("..")
        
def compute_graph_centrality(G : snap.TUNGraph) :
    
    deg_centr_dist = dict()
    for N in G.Nodes():
        degCentr = G.GetDegreeCentr(N.GetId())
        deg_centr_dist[N.GetId()] = degCentr
    
    sorted_deg_centr_dist = dict(sorted(deg_centr_dist.items(), key=lambda x: x[1], reverse=True))
    top5_deg_nodes = list(sorted_deg_centr_dist.keys())[:5]
    print("Top 5 nodes by degree centrality: ", " ".join([str(id) for id in top5_deg_nodes]))

    close_centr_dist = dict()
    for N in tqdm(G.Nodes()):
        closeCentr = G.GetClosenessCentr(N.GetId())
        close_centr_dist[N.GetId()] = closeCentr
    
    sorted_close_centr_dist = dict(sorted(close_centr_dist.items(), key=lambda x: x[1], reverse=True))
    top5_close_nodes = list(sorted_close_centr_dist.keys())[:5]
    print("Top 5 nodes by closeness centrality: ", " ".join([str(id) for id in top5_close_nodes]))

    Nodes, _ = G.GetBetweennessCentr(1.0)
    bet_centr_dist = dict(Nodes)
    
    sorted_bet_centr_dist = dict(sorted(bet_centr_dist.items(), key=lambda x: x[1], reverse=True))
    top5_bet_nodes = list(sorted_bet_centr_dist.keys())[:5]
    print("Top 5 nodes by betweenness centrality: ", " ".join([str(id) for id in top5_bet_nodes]))


def main(args):
    filepath = args[1]
    # start = time.time()
    G = snap.LoadEdgeList(snap.TUNGraph, filepath)
    compute_graph_size(G)
    compute_graph_degree(G, filepath)
    num_rand_nodes = 1000
    compute_graph_path(G, num_rand_nodes, filepath)
    compute_graph_comp(G, filepath)
    compute_graph_connectivity(G, filepath)
    compute_graph_centrality(G)
    # print(f"\nTime : {time.time() - start} seconds")
    
if __name__ == "__main__":
    main(sys.argv)
