import Tkinter as tk
import time
import forest, view, agents

def init_forest():
    agent_types = [agents.Tree, agents.LumberJack, agents.Bear]
    f = forest.Forest(20, agent_types)
    f.populate_all()
    return f


def tk_main():
    f = init_forest()
    app = view.GuiView(f, 12)

    app.mainloop()


def console_main():
    f = init_forest()
    fview = view.ForestView(f)

    counter = 0
    while True:
        if counter % 2 == 0:
            print fview.grid_view()
            print fview.world_status

        if counter % 6 == 0:
            fview.set_status()

        f.iter_sim()
        counter += 1    



if __name__ == '__main__':
    # console_main()
    tk_main()