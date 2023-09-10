import os
import snap

Rnd = snap.TRnd(42)
Rnd.Randomize()

# Facebook graph
# Fin = snap.TFIn("facebook_combined.txt")
# G = snap.TUNGraph.Load(Fin)
# for N in G.Nodes():
#     print(f"node : {N.GetId()}")

os.makedirs("subgraphs", exist_ok=True)
os.makedirs("networks", exist_ok=True)

FG = snap.LoadEdgeList(snap.TUNGraph, "facebook_combined.txt")
# print(f"Number of nodes in FB graph : {FG.GetNodes()}")
# print(f"Number of edges in FB graph : {FG.GetEdges()}")

# cnt=0
# for E in FG.Edges():
#     if E.GetSrcNId()%5==0 or E.GetDstNId()%5==0:
#         cnt+=1

# print(f"Number of edges in FB graph with nodes divisible by 5 : {cnt}")   

for N in FG.Nodes():
    if N.GetId()%5==0:
        FG.DelNode(N.GetId())

print(f"Number of nodes in FB graph after deletion : {FG.GetNodes()}")
print(f"Number of edges in FB graph after deletion : {FG.GetEdges()}")

FG.SaveEdgeList("subgraphs/facebook.elist")
FG.SaveEdgeList("networks/facebook.elist")

# Twitter graph
TG = snap.LoadEdgeList(snap.TUNGraph, "twitter_combined.txt")
# print(f"Number of nodes in Twitter graph : {TG.GetNodes()}")
# print(f"Number of edges in Twitter graph : {TG.GetEdges()}")

# cnt=0
# for E in TG.Edges():
#     if E.GetSrcNId()%3!=0 or E.GetDstNId()%3!=0:
#         cnt+=1

# print(f"Number of edges in Twitter graph with nodes not divisible by 3 : {cnt}") 

for N in TG.Nodes():
    if N.GetId()%3!=0:
        TG.DelNode(N.GetId())

# print(f"Number of nodes in Twitter graph after deletion : {TG.GetNodes()}")
# print(f"Number of edges in Twitter graph after deletion : {TG.GetEdges()}")

TG.SaveEdgeList("subgraphs/twitter.elist")
TG.SaveEdgeList("networks/twitter.elist")

# Random graph
RG = snap.GenRndGnm(snap.TUNGraph, 1000, 50000, False, Rnd)
# print(f"Number of nodes in Random graph : {RG.GetNodes()}")
# print(f"Number of edges in Random graph : {RG.GetEdges()}")

RG.SaveEdgeList("networks/random.elist")

# Small world graph
SG = snap.GenSmallWorld(1000, 50, 0.6, Rnd)
# print(f"Number of nodes in Small world graph : {SG.GetNodes()}")
# print(f"Number of edges in Small world graph : {SG.GetEdges()}")

SG.SaveEdgeList("networks/smallworld.elist")
