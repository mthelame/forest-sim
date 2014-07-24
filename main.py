#!/usr/bin/env python

import Tkinter as tk
import time, sys
import forest, view, agents


def tk_main(forest):
    app = view.GuiView(forest)
    app.mainloop()


def console_main(forest):
    fview = view.ForestView(forest)
    counter = 0
    while True:
        print fview.grid_view()
        print fview.world_status
        if counter % 12 == 0:
            fview.set_status()

        forest.iter_sim()
        counter += 1


if __name__ == '__main__':
    agent_types = [agents.Tree, agents.LonerLJ, agents.LumberJack, agents.Bear]
    f = forest.Forest(60, agent_types)
    f.populate_all()

    if len(sys.argv) > 1:
        if sys.argv[1] == 'text':
            console_main(f)
        else:
            print "unknown command"
    else:
        tk_main(f)
