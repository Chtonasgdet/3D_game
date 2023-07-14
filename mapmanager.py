import pickle
class Mapmanager():
    def __init__(self):
        self.model = 'block.egg'
        self.texture = 'block.png'
        self.colors = [
            (0.5, 0.3, 0.0, 1),
            (0.2, 0.2, 0.3, 1),
            (0.5, 0.5, 0.2, 1),
            (0.0, 0.6, 0.0, 1)
        ]
        self.start_new()
        self.add_block((0,10,0))

    def start_new(self):
        self.land = render.attachNewNode('Land')

    #добавление блока
    def add_block(self, pos):
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(pos)
        self.color = self.get_color(pos[2])
        self.block.setColor(self.color)
        self.block.reparentTo(self.land)
        self.block.setTag('at', str(pos))

    #заполнение карты блоками
    def load_land(self, file_name):
        self.clear()
        with open(file_name, 'r', encoding = 'utf-8') as file:
            y = 0
            for line in file:
                x = 0
                line = line.split()
                for height in line:
                    for z in range(int(height)+1):
                        block = self.add_block((x,y,z))
                    x += 1
                y += 1
        return x,y

    def clear(self):
        self.land.removeNode()
        self.start_new()

    #распределение цветов для разных высот
    def get_color(self, height):
        if height < len(self.colors):
            return self.colors[height]
        else:
            return self.colors[len(self.colors)-1]
    
    #проверка, есть ли перед игроком блоки и сколько их
    def check_the_front(self, pos):
        return self.land.findAllMatches('=at=' + str(pos))

    def is_empty(self, pos):
        blocks = self.check_the_front(pos)
        if blocks:
            return False
        else:
            return True

    def find_highest_empty(self, pos):
        x, y, z = pos
        z = 1
        while not self.is_empty((x, y, z)):
            z += 1
        return x, y, z

    #удаление блока(в режиме наблюдателя)
    def del_block(self, pos):
        blocks = self.check_the_front(pos)
        for block in blocks:
            block.removeNode()

    #строительство блока(в режиме игрока)
    def build_block(self, pos):
        x, y, z = pos
        new_block = self.find_highest_empty(pos)
        if new_block[2] < z+1:
            self.add_block(new_block)

    #удаление блока(в режиме игрока)
    def destroy_block(self, pos):
        x, y, z = self.find_highest_empty(pos)
        pos = x, y, z-1
        self.del_block(pos)

    #сохранение и загрузка карты
    def save_map(self):
        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as file:
            pickle.dump(len(blocks), file)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, file)

    def load_map(self):
        self.clear()
        with open('my_map.dat', 'rb') as file:
            length = pickle.load(file)
            for i in range(length):
                pos = pickle.load(file)
                self.add_block(pos)