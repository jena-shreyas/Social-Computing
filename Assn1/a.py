import torch.nn as nn
import torch

embed = nn.Embedding(539, 64)
input = torch.ones(651, 651, dtype=torch.long)
output = embed(input)
print(output.shape)