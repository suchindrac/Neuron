import tkinter as tk
import pickle
import random

tt_hide = True
ttp_win = None
label = None

def display_tooltip(event):
    global ttp_win
    global label
    global tt_hide
    
    if tt_hide:
        if label != None:
            label.pack_forget()
        tt_hide = False
        return
    
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    o = canvas.find_closest(x, y)[0]
    uuid = canvas.gettags(o)[0]
    node = node_map.get_node_by_uuid(uuid)
    ttd = ""
    ktd = ["text", "value", "next_is", "is_verb", "is_noun", "conn_nouns", "conn_verbs"]
    for k in ktd:
        if k == "conn_nouns":
            ttd += f"{k} -> {[x.value[0] for x in node.__dict__[k]]}\n"
        elif k == "conn_verbs":
            ttd += f"{k} -> {[x.value[0] for x in node.__dict__[k]]}\n"
        else:
            ttd += f"{k} -> {node.__dict__[k]}\n"

    ttp_win = tk.Toplevel(root)
    ttp_win.wm_overrideredirect(True)
    ttp_win.wm_geometry("+%d+%d" % (x, y))
    label = tk.Label(ttp_win, text=ttd, justify="left", wraplength=300,
                     background="#ffffff")

    label.pack(expand=True)

    tt_hide = True
        
if __name__ == "__main__":
    root = tk.Tk()
    canvas = tk.Canvas(root, width=800, height=800, bg="yellow")
    canvas.pack()

    root.bind("<Button-1>", display_tooltip)
    
    node_map = None
    with open("node_map.pkl", "rb") as fd:
        node_map = pickle.load(fd)

    disp_nodes = node_map.verb_nodes
    # disp_nodes.extend(node_map.noun_nodes)

    for node in disp_nodes:
        x, y = random.randint(10, 800), random.randint(10, 800)
        r = 10
        tag = f"{node.uuid}"
        canvas.create_oval(x-r, y-r, x+r, y+r, fill="blue", outline="#DDD", width=4, tag=tag)
    
    root.mainloop()
