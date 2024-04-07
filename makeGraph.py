from graphviz import Digraph
import pandas as pd

df = pd.read_csv('data.csv')

dot = Digraph()


maxGen = df['Generation'].max()

for i in range(maxGen):
    for people in df[df['Generation'] == i]:
        print("AD")