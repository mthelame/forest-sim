import Tkinter as tk

str_to_color = {'T': '#003300',
                't': '#194719',
                '+': '#335C33',
                '@': '#1F0F00',
                '#': '#8D1919',
                'L': '#FF6600',
                ' ': '#AD855C'}

class ForestView(object):

    def __init__(self, world):
        self.world = world
        self.world_status = ""

    def grid_view(self):
        views = []
        for y in xrange(self.world.length):
            views.append(self.row_view(y))
        return ('\n' * 10) + '\n'.join(row for row in views) + '\n'

    def row_view(self, row):
        view = []
        for col in xrange(self.world.width):
            cell = sorted(self.world.cells[col,row], key = lambda a: type(a).ratio)
            if len(cell) > 0:
                view.append(str(cell[0]))
            else:
                view.append('.')
        return ' '.join(c for c in view)

    def graph_type(self, kind):
        count = self.world.count_type(kind)
        count = count // kind.graph_units
        return kind.__name__ + ': ' + ''.join([kind.marker for _ in xrange(count)])

    def set_status(self):
        date_str = "year: " + str(self.world.steps // 12) + " month: " + str(self.world.steps % 12)
        type_str = '\n'.join([self.graph_type(kind) for kind in self.world.agent_types])
        self.world_status = date_str + '\n' + type_str


class GuiView(object):

    def __init__(self, world):
        self.scale = 520 // world.length
        self.world = world
        self.simming = False # whether the sim is running

        self.root = tk.Tk()
        self.root.resizable(0,0)
        self.canv = tk.Canvas(self.root, height=world.length*self.scale + 5, 
                                         width=world.width*self.scale + 5)
        self.canv.pack(anchor="nw")

        self.graph_canv = tk.Canvas(self.root, height=100, width=world.width*self.scale + 55)
        self.graph_canv.pack(anchor="s")


        self.canv.bind('<Button-1>', self.on_click)

        self.draw_grid()


    def draw_row(self, row):
        for col in xrange(self.world.width):
            cell = sorted(self.world.cells[col,row], key = lambda a: type(a).ratio)
            x = col*self.scale + 5
            y = row*self.scale + 5
            self.canv.create_rectangle(x, y, x+self.scale, y+self.scale, fill=self.cell_color(cell))

    def draw_grid(self):
        self.canv.delete('all')
        for row in xrange(self.world.length):
            self.draw_row(row)

    def graph_type(self, kind, time):
        count = self.world.count_type(kind) // kind.graph_units
        graph_height = self.graph_canv.winfo_height()
        count_max = (self.world.length * self.world.width) // 20

        g_count = graph_height - ((count * graph_height) // count_max) - 5

        color = str_to_color[kind.marker]
        self.graph_canv.create_rectangle(time + 2, g_count, 
                                         time + 4, g_count + 2, 
                                         fill=color, outline=color)

    def draw_graph(self):
        month = self.world.steps
        for kind in self.world.agent_types:
            self.graph_type(kind, month)

    def cell_color(self, cell):
        if len(cell) == 0:
            agent_str = ' '
        else:
            agent_str = str(cell[0]) 
        return str_to_color[agent_str]

    def iter_once(self):
        self.world.iter_sim()
        self.draw_grid()

    def iter_loop(self):
        if self.simming:
            self.world.iter_sim()
            self.draw_grid()
            self.draw_graph()
            self.canv.after(30, self.iter_loop)

    def on_click(self, event):
        if not self.simming:
            self.simming = True
            self.iter_loop()
        else:
            self.simming = False

    def mainloop(self):
        self.root.mainloop()
