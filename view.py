import Tkinter as tk

str_to_color = {'T': '#003300',
                't': '#194719',
                '+': '#335C33',
                '@': '#1F0F00',
                '#': '#8D1919'}

class ForestView(object):

    def __init__(self, world):
        self.world = world
        self.world_status = ""

    def grid_view(self):
        views = []
        for y in xrange(self.world.length):
            views.append(self.row_view(y))
        return '\n' + '\n'.join(row for row in views) + '\n'

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
        count = self.world.type_data[kind.__name__]['count']
        count = count // kind.graph_units
        return kind.__name__ + ': ' + ''.join([kind.marker for _ in xrange(count)])

    def set_status(self):
        date_str = "year: " + str(self.world.steps // 12) + " month: " + str(self.world.steps % 12)
        type_str = '\n'.join([self.graph_type(kind) for kind in self.world.agent_types])
        self.world_status = date_str + '\n' + type_str


class GuiView(object):

    def __init__(self, world, scale):
        self.scale = scale
        self.world = world

        self.root = tk.Tk()
        self.canv = tk.Canvas(self.root, height=world.length*scale + 5, width=world.width*scale + 5)
        self.canv.pack()
        self.draw_grid()

        self.simming = False

        self.root.bind('<Button-1>', self.on_click)


    def draw_row(self, row):
        for col in xrange(self.world.width):
            cell = sorted(self.world.cells[col,row], key = lambda a: type(a).ratio)
            x = col*self.scale + 5
            y = row*self.scale + 5
            self.canv.create_rectangle(y, x, y+self.scale, x+self.scale, fill=self.cell_color(cell))

    def draw_grid(self):
        self.canv.delete('all')
        for row in xrange(self.world.length):
            self.draw_row(row)

    def cell_color(self, cell):
        if len(cell) == 0:
            return '#AD855C'
        else:
            return str_to_color[str(cell[0])]

    def iter_once(self):
        self.world.iter_sim()
        self.draw_grid()

    def iter_loop(self):
        if self.simming:
            self.world.iter_sim()
            self.draw_grid()
            self.root.after(1, self.iter_loop)

    def on_click(self, event):
        if not self.simming:
            self.simming = True
            self.iter_loop()
        else:
            self.simming = False


    def mainloop(self):
        self.root.mainloop()









        