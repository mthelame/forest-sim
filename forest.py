import random

class Forest(object):

    def __init__(self, dim, agent_types):
        self.length = dim
        self.width = dim

        self.cells = dict()
        for y in xrange(dim):
            for x in xrange(dim):
                self.cells[(x,y)] = set()

        self.agent_types = agent_types
        self.agents = {kind.__name__: set() for kind in self.agent_types}
        self.type_data = {kind.__name__: kind.create_data_dict() for kind in self.agent_types}

        self.steps = 1

    def count_type(self, kind):
        return len(self.agents[kind.__name__])

    def add_agent(self, agent):
        kind = type(agent).__name__
        self.agents[kind].add(agent)
        self.cells[(agent.x,agent.y)].add(agent)

    def rem_agent(self, agent):
        kind = type(agent).__name__
        self.agents[kind].remove(agent)
        self.cells[(agent.x,agent.y)].remove(agent)

    def random_agent(self, kind):
        return random.choice(tuple(self.agents[kind.__name__]))

    def update_pos(self, agent, old_pos, new_pos):
        self.cells[old_pos].remove(agent)
        self.cells[new_pos].add(agent)

    def neighbor_coords(self, x, y):
        neighbors = [(x - 1, y - 1),
                     (x - 1, y),
                     (x - 1, y + 1),
                     (x, y - 1),
                     (x, y + 1),
                     (x + 1, y - 1),
                     (x + 1, y),
                     (x + 1, y + 1)]
        if x != 0 and x != self.width - 1 and y != 0 and y != self.length - 1:
            return neighbors # majority of cells will not need to check borders

        valids = []
        for c in neighbors:
            if c[0] >= 0 and c[0] < self.width and c[1] >= 0 and c[1] < self.length:
                valids.append(c)
        return valids        

    def populate_type(self, agent_type):
        for pos,cell in self.cells.iteritems():
            if random.random() < agent_type.ratio:
                agent = agent_type(self, pos[0], pos[1])
                self.add_agent(agent)

    def populate_all(self):
        for kind in self.agent_types:
            self.populate_type(kind)

    def spawn_new(self, agent_type):
        valids = []
        for coords,cell in self.cells.iteritems():
            if not any(type(agent) == agent_type for agent in cell):
                valids.append(coords)
        x, y = random.choice(valids)
        return agent_type(self, x, y)

    def agent_type_actions(self, agent_type):
        for agent in list(self.agents[agent_type.__name__]):
            agent.action()

    def iter_sim(self):
        for agent_type in self.agent_types:
            self.agent_type_actions(agent_type)
        if self.steps % 12 == 0:
            self.super_iter()
        self.steps += 1

    def super_iter(self):
        for agent_type in self.agent_types:
            agent_type.super_action(self, self.type_data[agent_type.__name__])


class ToroidalForest(Forest):

    def neighbor_coords(self, x, y):
        x_min = (x - 1) % self.width
        x_max = (x + 1) % self.width
        y_min = (y - 1) % self.length
        y_max = (y + 1) % self.length

        neighbors = [(x_min, y_min),
                     (x_min, y),
                     (x_min, y_max),
                     (x, y_min),
                     (x, y_max),
                     (x_max, y_min),
                     (x_max, y),
                     (x_max, y_max)]
        return neighbors

