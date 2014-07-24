import random

class Agent(object):
    next_id = 1
    ratio = 0
    speed = 0
    marker = 'A'
    graph_units = 1

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.age = 0
        self.active = True

        self.id = Agent.next_id
        Agent.next_id += 1

    def __repr__(self):
        return str(self.id) + ' ' + type(self).__name__

    def __str__(self):
        return type(self).marker

    def get_data_dict(self):
        return self.world.type_data[type(self).__name__]

    def get_pos(self):
        return (self.x,self.y)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def action(self):
        self.age += 1

    def valid_moves(self):
        valids = []
        for coord in self.world.neighbor_coords(self.x, self.y):
            occupants = self.world.cells[coord]
            if not any(type(agent) == type(self) for agent in occupants):
                valids.append(coord)
        return valids

    def is_move_valid(self, coords):
        occupants = self.world.cells[coords]
        if not any(type(agent) == type(self) for agent in occupants):
            return True
        else:
            return False

    def move(self):
        possible_moves = self.world.neighbor_coords(self.x, self.y)
        
        move = random.choice(possible_moves)
        while not self.is_move_valid(move):
            possible_moves.remove(move)
            try:
                move = random.choice(possible_moves)
            except IndexError:
                return # no valid moves

        new_x, new_y = move
        self.world.update_pos(self, (self.x, self.y), (new_x, new_y))
        self.x = new_x
        self.y = new_y

    def preys_on(self, agent):
        return False

    def get_prey(self):
        for cellmate in self.world.cells[(self.x, self.y)]:
            if self.preys_on(cellmate):
                return cellmate
        return None

    @classmethod
    def create_data_dict(cls):
        return {}

    @classmethod
    def super_action(cls, world, data):
        pass


class Tree(Agent):
    ratio = .6
    base_fertility = 0.015
    age_up_one = 24
    age_up_two = 120
    marker = 'T'
    graph_units = 10

    def __init__(self, world, x, y):
        super(Tree, self).__init__(world, x, y)
        self.stage = random.randint(0,2)

        if self.stage == 0:
            self.age = random.randint(0, type(self).age_up_one - 1)
        elif self.stage == 1:
            self.age = random.randint(type(self).age_up_one, type(self).age_up_two - 1)
        else:
            self.age = random.randint(type(self).age_up_two, 200)

    def __str__(self):
        return ['+','t','T'][self.stage]

    def action(self):
        self.age += 1
        if self.age == type(self).age_up_one or self.age == type(self).age_up_two:
            self.stage += 1

        if self.stage == 0:
            return

        offspring = self.try_reproduce()
        if offspring:
            self.world.add_agent(offspring)

    def move(self):
        pass # trees don't move, silly

    def try_reproduce(self):
        valid_coords = []
        for coord in self.world.neighbor_coords(self.x, self.y):
            if not any(isinstance(a, Tree) for a in self.world.cells[coord]):
                valid_coords.append(coord)
        if len(valid_coords) == 0 or random.random() > (Tree.base_fertility * self.stage):
            return None
        else:
            coord = random.choice(valid_coords)
            return type(self).breed_new(self.world, coord[0], coord[1])

    @classmethod
    def breed_new(cls, world, x, y):
        agent = cls(world, x, y)
        agent.stage = 0
        agent.age = 0
        return agent


class LumberJack(Agent):
    ratio = 0.005
    speed = 2
    marker = '#'

    def __init__(self, world, x, y):
        super(LumberJack, self).__init__(world, x, y)

    def preys_on(self, agent):
        return isinstance(agent, Tree) and agent.stage > 0 and agent.active

    def prey_value(self, prey):
        return int(prey.stage ** 1.6)

    def action(self):
        self.age += 1
        moves_left = type(self).speed
        prey = None
        while moves_left > 0:
            prey = self.get_prey()
            if prey:
                prey.active = False
                break

            self.move()
            moves_left -= 1
        if prey:
            self.world.rem_agent(prey)
            d = self.get_data_dict()
            d['total_lumber'] += self.prey_value(prey)

    @classmethod
    def create_data_dict(cls):
        return {'total_lumber': 0}

    @classmethod
    def super_action(cls, world, data):
        lumber = data['total_lumber']
        count = world.count_type(cls)
        if count == 0:
            world.add_agent(world.spawn_new(cls))
            return
        diff = ((lumber // 8) - count)
        if diff > 0:
            for _ in xrange(2):
                world.add_agent(world.spawn_new(cls))
        if diff < 0:
            try:
                world.rem_agent(world.random_agent(cls))
            except IndexError:
                print world.agents[cls.__name__]
                print len(world.agents[cls.__name__])
                raise

        data['total_lumber'] = 0


class LonerLJ(LumberJack):
    marker = 'L'

    def __init__(self, world, x, y):
        super(LumberJack, self).__init__(world, x, y)
        self.lumber_collected = 0

    def action(self):
        self.age += 1
        moves_left = type(self).speed
        prey = None
        while moves_left > 0:
            prey = self.get_prey()
            if prey:
                prey.active = False
                break

            self.move()
            moves_left -= 1
        if prey:
            self.world.rem_agent(prey)
            self.lumber_collected += self.prey_value(prey)

    @classmethod
    def create_data_dict(cls):
        return {}

    @classmethod
    def super_action(cls, world, data):
        new_loners = 0
        all_loners = list(world.agents[cls.__name__])
        if len(all_loners) == 0:
            new_loners += 1 # always one fool willing to try his luck

        for loner in all_loners:
            if loner.lumber_collected < 4: 
                world.rem_agent(loner)
            if loner.lumber_collected > 16: # huge profits inspire copycats
                new_loners += 1
            loner.lumber_collected = 0

        for _ in xrange(new_loners):
            world.add_agent(world.spawn_new(cls))



class Bear(Agent):
    ratio = 0.003
    speed = 4
    marker = '@'

    def __init__(self, world, x, y):
        super(Bear, self).__init__(world, x, y)

    def preys_on(self, agent):
        return isinstance(agent, LumberJack) and agent.active

    def action(self):
        self.age += 1
        moves_left = type(self).speed
        prey = None
        while moves_left > 0:
            prey = self.get_prey()
            if prey:
                prey.active = False
                break

            self.move()
            moves_left -= 1
        if prey:
            self.world.rem_agent(prey)
            d = self.get_data_dict()
            d['mauls'] += 1

    @classmethod
    def create_data_dict(cls):
        return {'mauls': 0}

    @classmethod
    def super_action(cls, world, data):
        mauls = data['mauls']
        if mauls == 0:
            world.add_agent(world.spawn_new(cls))
        else:
            world.rem_agent(world.random_agent(cls))
        data['mauls'] = 0
