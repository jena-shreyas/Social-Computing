import os
import snap

Rnd = snap.TRnd(42)
Rnd.Randomize()

os.makedirs("subgraphs", exist_ok=True)
os.makedirs("networks", exist_ok=True)

# Facebook graph
FG = snap.LoadEdgeList(snap.TUNGraph, "facebook_combined.txt") 

for N in FG.Nodes():
    if N.GetId()%5==0:
        FG.DelNode(N.GetId())

FG.SaveEdgeList("subgraphs/facebook.elist")
FG.SaveEdgeList("networks/facebook.elist")

# Twitter graph
TG = snap.LoadEdgeList(snap.TUNGraph, "twitter_combined.txt")

for N in TG.Nodes():
    if N.GetId()%3!=0:
        TG.DelNode(N.GetId())

TG.SaveEdgeList("subgraphs/twitter.elist")
TG.SaveEdgeList("networks/twitter.elist")

# Random graph
RG = snap.GenRndGnm(snap.TUNGraph, 1000, 50000, False, Rnd)
RG.SaveEdgeList("networks/random.elist")

# Small world graph
SG = snap.GenSmallWorld(1000, 50, 0.6, Rnd)
SG.SaveEdgeList("networks/smallworld.elist")
