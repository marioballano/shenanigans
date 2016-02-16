#!/usr/bin/env python
import os
import re
from subprocess import check_output
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

def connected_room(sf):
  r = None
  deco = check_output(['descumm','-3',sf])
  m = re.search("loadRoomWithEgo\((-?[0-9]+),(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)\)",deco)
  if m: r = m.group(2)
  return r

def walkobjects(room):
  for root, dirs, files in os.walk(room):
    for name in files:
      if name == "OC.dmp":
        dst_room = connected_room(os.path.join(root,name))
        if dst_room:
          inspect_room(dst_room)
          G.add_edge(room,dst_room)
 
def inspect_room(room):
  if room not in G.nodes():
    G.add_node(room)
    walkobjects(room)

def walkrooms():
  for root, dirs, files in os.walk('.'):
    for name in dirs:
      if (name.endswith('_tunnel')):
        room = root.split(os.path.sep)[1]
        inspect_room(room)

def draw():
  nx.draw(G,with_labels=True)
  plt.savefig("catamap.png")
  plt.show()

if __name__ == '__main__':
  walkrooms()
  draw()
  print ' '.join(G.nodes())
