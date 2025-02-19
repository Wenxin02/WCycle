import networkx as nx
from tqdm import tqdm
import pandas as pd
import csv

def weighted_cycle(G, output_path):
    list_cycle_basis = nx.cycle_basis(G)
    total_cycle_basis = len(list_cycle_basis)
    cycleNum_dict = {}

    for i in tqdm(G.nodes(), desc="Calculating weighted cycle counts", unit="node"):
        weight_i = 0
        for cycle in list_cycle_basis:
            if i in cycle:
                edges_in_cycle = [(cycle[j], cycle[(j + 1) % len(cycle)]) for j in range(len(cycle))]
                weight_i += sum(G[edge[0]][edge[1]].get('weight', 1) for edge in edges_in_cycle)

        cycleNum_dict[i] = weight_i/total_cycle_basis

    with open(output_path+'WCycle.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        csv_writer.writerow(['ID', 'WCycle'])

        for node, count in cycleNum_dict.items():
            csv_writer.writerow([node, count])

    print(f"WCycle saved")
    return cycleNum_dict

input_path=""
output_path=""
data_path=input_path
df=pd.read_csv(data_path,sep=",",header=None)
df.columns = ['userA','userB', 'weight']
G=nx.from_pandas_edgelist(df,source='userA',target='userB',edge_attr='weight',create_using=nx.Graph())
weighted_cycle(G,output_path)