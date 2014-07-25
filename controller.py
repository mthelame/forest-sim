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

        self.view_objects.append(view.TkGraphView(self, world)) # create graph view

        self.params = tk.Frame(self.root) # create options
        self.params.pack(side='right', fill='y', expand=1)
        strt_stp = tk.Button(self.params, text="Start/Stop", command=self.start_stop)
        strt_stp.pack(side='top')

        self.view_objects.append(view.TkGridView(self, world)) # create grid view

        self.root.bind('<Button-1>', self.start_stop)

    def iter_loop(self):
        if self.simming:
            self.world.iter_sim()
            for v in self.view_objects:
                v.draw()

            self.root.after(30, self.iter_loop)


    def start_stop(self, event=None):
        if not self.simming:
            self.simming = True
            self.iter_loop()
        else:
            self.simming = False

    def run(self):
        self.root.mainloop()