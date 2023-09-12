import os
import sys
import snap
import matplotlib.pyplot as plt

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

    # compute distribution of graph shortest path lengths
    pathDist = dict()
    # start = time.time()
    for N in G.Nodes():
        _, IdtoDistH = G.GetShortPathAll(N.GetId(), False)
        
        for id in IdtoDistH:
            pathLen = IdtoDistH[id]
            if pathLen not in pathDist:
                pathDist[pathLen] = 1
            else:
                pathDist[pathLen] += 1
    # t = time.time() - start

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

    # Sccs = G.GetSccs()
    # scc_size_dist = dict()

    # for scc in Sccs:
    #     if scc.Len() not in scc_size_dist:
    #         scc_size_dist[scc.Len()] = 1
    #     else:
    #         scc_size_dist[scc.Len()] += 1

    # # for size in scc_size_dist:
    # #     print(size, scc_size_dist[size])
        
    # sizes = list(scc_size_dist.keys())
    # freqs = list(scc_size_dist.values())

    # plt.plot(sizes, freqs, marker='o', linestyle='-')

    subgraph_name = filepath.split('/')[-1].split('.')[0]
    os.makedirs("plots", exist_ok=True)
    os.chdir("plots")
    
    G.PlotSccDistr("connected_comp_" + subgraph_name, "Connected Component Distribution")
    # os.rename("diam.connected_comp_" + subgraph_name + ".png", "connected_comp_" + subgraph_name + ".png")
    # os.remove("diam.connected_comp_" + subgraph_name + ".tab")
    # os.remove("diam.connected_comp_" + subgraph_name + ".plt")
    os.chdir("..")

def compute_graph_connectivity(G : snap.TUNGraph, filepath : str) :

    '''
        TODO: Giving OOM error for twitter graph !
    '''
    AvgCF = G.GetClustCf(-1)
    print("Average clustering coefficient: ", AvgCF)

    numTriads = G.GetTriads()
    print("Number of triads: ", numTriads)

    nId = G.GetRndNId(Rnd)
    print(f"Clustering coefficient of random node {nId}: {G.GetNodeClustCf(nId)}")

    nId = G.GetRndNId(Rnd)
    print(f"Number of triads random node {nId} participates: {G.GetNodeTriads(nId)}")

    # '''
    #     TODO: Giving OOM error for twitter graph !
    # '''

    # nIdCCfH = G.GetNodeClustCfAll()
    # ccf_dist = dict()

    # for id in nIdCCfH:
    #     rnd_ccf = round(nIdCCfH[id], 1)     # divide ccf values into buckets of width 0.1
    #     if rnd_ccf not in ccf_dist:
    #         ccf_dist[rnd_ccf] = 1
    #     else:
    #         ccf_dist[rnd_ccf] += 1

    # sorted_ccf_dist = dict(sorted(ccf_dist.items()))    # sort the ccf distribution dictionary by key

    # # for ccf in sorted_ccf_dist:
    # #     print(ccf, sorted_ccf_dist[ccf])

    # ccfs = list(sorted_ccf_dist.keys())
    # freqs = list(sorted_ccf_dist.values())

    # plt.plot(ccfs, freqs, marker='o', linestyle='-')

    subgraph_name = filepath.split('/')[-1].split('.')[0]
    os.makedirs("plots", exist_ok=True)
    os.chdir("plots")
    
    G.PlotSccDistr("clustering_coeff_" + subgraph_name, "Clustering Coefficient Distribution")
    # os.rename("diam.clustering_coeff_" + subgraph_name + ".png", "clustering_coeff_" + subgraph_name + ".png")
    # os.remove("diam.clustering_coeff_" + subgraph_name + ".tab")
    # os.remove("diam.clustering_coeff_" + subgraph_name + ".plt")
    os.chdir("..")
        
def compute_graph_centrality(G : snap.TUNGraph) :
    
    '''
        TAKING TOO MUCH TIME !
    '''
    deg_centr_dist = dict()
    for N in G.Nodes():
        degCentr = G.GetDegreeCentr(N.GetId())
        deg_centr_dist[N.GetId()] = degCentr
    
    top5_deg_nodes = list(deg_centr_dist.keys())[:5]
    print("Top 5 nodes by degree centrality: ", " ".join([str(id) for id in top5_deg_nodes]))

    close_centr_dist = dict()
    for N in G.Nodes():
        closeCentr = G.GetClosenessCentr(N.GetId())
        close_centr_dist[N.GetId()] = closeCentr
    
    top5_close_nodes = list(close_centr_dist.keys())[:5]
    print("Top 5 nodes by closeness centrality: ", " ".join([str(id) for id in top5_close_nodes]))

    bet_centr_dist = dict()
    for N in G.Nodes():
        betCentr = G.GetBetweennessCentr(N.GetId())
        bet_centr_dist[N.GetId()] = betCentr
    
    top5_bet_nodes = list(bet_centr_dist.keys())[:5]
    print("Top 5 nodes by betweenness centrality: ", " ".join([str(id) for id in top5_bet_nodes]))



def main(args):
    filepath = args[1]
    G = snap.LoadEdgeList(snap.TUNGraph, filepath)
    # compute_graph_size(G)
    # compute_graph_degree(G, filepath)
    num_rand_nodes = 1000
    compute_graph_path(G, num_rand_nodes, filepath)
    # compute_graph_comp(G, filepath)
    # compute_graph_connectivity(G, filepath)
    # compute_graph_centrality(G)
    
    
if __name__ == "__main__":
    main(sys.argv)