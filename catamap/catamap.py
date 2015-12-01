"""
[ intro ]

Right after watching @reversemode's talk "21 days" I felt a bit nostalgic,
in the talk he mentions one of first video games we used to play back 
when we were kids, oh boy.. we spent a ridiculous amount of time drawing maps 
of a catacomb maze and it was great fun!.. that feeling you get when you 
manage to unravel those sort of riddles is probably not far off from what 
you experience reversing/breaking software :)

I thought it could be good fun to have look at the same riddle from a 
software reversing perspective, these days is obviously way easier
than it coulda been back then since the awesome guys from ScummVM 
have reimplemented the scumm game engine and made it available for 
everyone to enjoy.

This crappy script aims to generate a map of the catacomb rooms for the
graphic adventure game "Indiana Jones and the Last Crusade"

[ usage ] 

In order to run the script you first need to extract the contents from the 
game's LFL files using scummpacker then run this script at the same 
directory where the extracted files lie. 

The script looks for rooms with objects labeled "tunnel", identifies rooms and 
traverses them, in order to do this we make use of the "descumm" tool to decompile
the game's scripts and look for constructions using the loadRoomWithEgo() 
opcode.

[ notes ] 

In the game Indy enters the catacombs through room 50, I have also 
taken screenshots of each one of the rooms (see screens.sh) and uploaded 
them to this repo.

Room 86 is a false positive, it contains an element named "tunnel"
and it mistakenly gets added to the map, that's why it shows up as
an orphan node in the graph.

[references]

game@wikipedia      : https://en.wikipedia.org/wiki/Indiana_Jones_and_the_Last_Crusade:_The_Graphic_Adventure
scummvm             : http://scummvm.org/
scummpacker         : http://www.jestarjokin.net/sw/doc/scummpacker_manual.html
descumm             : https://github.com/scummvm/scummvm-tools
@reversemode's talk : https://www.youtube.com/watch?v=218Qk2x0rhE

[ greets ] 

@reversemode : for bringing these memories back! :)
@ScummVM     : you guys rock
"""
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
