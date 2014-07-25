import view
import Tkinter as tk

class Controller(object):

    def __init__(self, world):
        self.world = world
        self.simming = False # whether the sim is running

        self.win_width = 650
        self.win_height = 700
        self.view_objects = []

        self.root = tk.Tk()
        self.root.geometry("%dx%d" % (self.win_width, self.win_height))
        self.root.resizable(0,0)

        grid = view.TkGraphView(self, world) # create graph view
        self.view_objects.append(grid) 

        self.params = tk.Frame(self.root)
        self.params.pack(side='right', fill='y', expand=1)

        strt_stp = tk.Button(self.params, text="Start/Stop", command=self.start_stop)
        strt_stp.pack(side='top', fill='x') # start stop button

        reset = tk.Button(self.params, text="Reseed", command=self.reset_world)
        reset.pack(side='top', fill='x') # reset button

        graph = view.TkGridView(self, world) # create grid view
        self.view_objects.append(graph) 

        # self.root.bind("<Button-1>", self.start_stop)

    def iter_loop(self):
        if self.simming:
            self.world.iter_sim()
            self.update_views()
            self.root.after(100, self.iter_loop)

    def update_views(self):
        for v in self.view_objects:
            v.draw()

    def start_stop(self, event=None):
        if not self.simming:
            self.simming = True
            self.iter_loop()

        else:
            self.simming = False

    def reset_world(self):
        self.simming = False
        self.world.reset()
        self.update_views()

    def run(self):
        self.root.mainloop()