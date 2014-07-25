#!/usr/bin/env python

import Tkinter as tk
import time, sys
import forest, controller, agents


def tk_main(forest):
    app = controller.Controller(f)
    app.run()


if __name__ == '__main__':
    agent_types = [agents.Tree, agents.LonerLJ, agents.LumberJack, agents.Bear, agents.Deer]
    f = forest.Forest(30, agent_types)
    f.populate_all()
    tk_main(f)
