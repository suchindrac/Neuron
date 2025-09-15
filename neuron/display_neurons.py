import tkinter as tk
import pickle
import random

root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=300, bg="yellow")

canvas.pack()

node_map = None
with open("node_map.pkl", "rb") as fd:
    node_map = pickle.load(fd)

for node in node_map.verb_nodes:
    x, y = random.randint(0, 100), random.randint(0, 100)
    r = 5
    canvas.create_oval(x-r, y-r, x+r, y+r, fill="blue", outline="#DDD", width=4, tag=node.text)
    
root.mainloop()
