import Tkinter as tk

str_to_color = {'T': '#003300',
                't': '#194719',
                '+': '#335C33',
                '@': '#1F0F00',
                '#': '#8D1919',
                'L': '#FF6600',
                ' ': '#B89470',
                'D': '#A37519'}

class TkGridView(object):

    def __init__(self, controller, world):
        self.controller = controller
        self.root = controller.root
        self.world = world
        self.scale = (controller.win_height - 150) // world.length

        self.canv = tk.Canvas(self.root, height=world.length*self.scale + 5, 
                                         width=world.width*self.scale + 5, bg= '#B89470')
        self.canv.pack(side="left", anchor='nw')

        self.draw()

    def draw_row(self, row):
        for col in xrange(self.world.width):
            cell = sorted(self.world.cells[col,row], key = lambda a: type(a).ratio)
            x = col*self.scale + 5
            y = row*self.scale + 5
            if len(cell) == 0:
                continue
            self.canv.create_oval(x, y, x+self.scale, y+self.scale, 
                                       fill=self.cell_color(cell), 
                                       outline=self.cell_color(cell))

    def draw(self):
        self.canv.delete('all')
        for row in xrange(self.world.length):
            self.draw_row(row)

    def cell_color(self, cell):
        agent_str = str(cell[0]) 
        return str_to_color[agent_str]


class TkGraphView(object):

    def __init__(self, controller, world):
        self.controller = controller
        self.root = controller.root
        self.world = world

        self.canv = tk.Canvas(self.root, height=144)
        self.canv.pack(side='bottom', anchor='sw', fill='x', expand=1)

    def graph_type(self, kind, time):
        pass # need to implement this

    def draw(self):
        interval = 2 # every other month
        month = self.world.steps
        if month % interval == 0:
            for kind in self.world.agent_types:
                self.graph_type(kind, month // 2)
