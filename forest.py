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

        self.steps = 0

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

    def neighbor_coords(self, in_x, in_y):
        neighbors = []
        for x in xrange(in_x - 1, in_x + 2):
            for y in xrange(in_y - 1, in_y + 2):
                x = x % self.width
                y = y % self.length
                if (x,y) != (in_x, in_y):
                    neighbors.append((x,y))
        return neighbors

    def populate_type(self, agent_type):
        for pos,cell in self.cells.iteritems():
            if random.random() < agent_type.ratio:
                agent = agent_type(self, pos[0], pos[1])
                self.add_agent(agent)
        self.type_data[agent_type.__name__]['count'] = self.count_type(agent_type)

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
            self.type_data[agent_type.__name__]['count'] = self.count_type(agent_type)
        if self.steps % 12 == 0:
            self.super_iter()
        self.steps += 1

    def super_iter(self):
        for agent_type in self.agent_types:
            agent_type.super_action(self, self.type_data[agent_type.__name__])
