class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.mode = True
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.first_person_viev()
        self.accept_events()

    #вид от первого лица
    def first_person_viev(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0,0,1.5)
        self.camera_on = True

    #вид от третьего лица
    def third_person_viev(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.camera_on = False

    #смена вида
    def changed_view(self):
        if self.camera_on == True:
            self.third_person_viev()
        else:
            self.first_person_viev()

    #повороты камерой
    def turn_left(self):
        self.hero.setH((self.hero.getH()+5)%360)

    def turn_right(self):
        self.hero.setH((self.hero.getH()-5)%360)

    def turn_up(self):
        self.hero.setP((self.hero.getP()+5)%360)

    def turn_down(self):
        self.hero.setP((self.hero.getP()-5)%360)

    #играбельный режим
    def player_mode(self, angle):
        pos = self.look_at(angle)
        if self.land.is_empty(pos):
            pos = self.land.find_highest_empty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.is_empty(pos):
                self.hero.setPos(pos)

    #режим наблюдателя(можно передвигаться как угодно, даже сквозь стены)
    def observer_mode(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    #смена игрового режима
    def View(self, angle):
        if self.mode == True:
            self.observer_mode(angle)
        else:
            self.player_mode(angle)

    #проверка направления движения
    def look_at(self, angle):
        from_x = round(self.hero.getX())
        from_y = round(self.hero.getY())
        from_z = round(self.hero.getZ())
        dx, dy = self.check_dir(angle)
        return from_x + dx, from_y + dy, from_z

    def check_dir(self, angle):
        if angle >= 0 and angle <= 22.5:
            return 0, -1
        elif angle <= 67.5:
            return 1, -1
        elif angle <= 112.5:
            return 1, 0
        elif angle <= 157.5:
            return 1, 1
        elif angle <= 202.5:
            return 0, 1
        elif angle <= 247.5:
            return -1, 1
        elif angle <= 292.5:
            return -1, 0
        elif angle <= 337.5:
            return -1, -1
        else:
            return 0, -1

    #передвижение персонажа
    def move_forward(self):
        angle = (self.hero.getH())%360
        self.View(angle)

    def move_left(self):
        angle = (self.hero.getH() + 90)%360
        self.View(angle)

    def move_back(self):
        angle = (self.hero.getH() + 180)%360
        self.View(angle)

    def move_right(self):
        angle = (self.hero.getH() + 270)%360
        self.View(angle)

    def move_up(self):
        self.hero.setZ(self.hero.getZ() + 1)

    def move_down(self):
        self.hero.setZ(self.hero.getZ() - 1)

    def changed_mode(self):
        if self.mode == True:
            self.mode = False
        else:
            self.mode = True

    #строительство и разрушение блоков
    def build(self):
        angle = self.hero.getH()%360
        pos = self.look_at(angle)
        if self.mode:
            self.land.add_block(pos)
        else:
            self.land.build_block(pos)
    
    def destroy(self):
        angle = self.hero.getH()%360
        pos = self.look_at(angle)
        if self.mode:
            self.land.del_block(pos)
        else:
            self.land.destroy_block(pos)

    #обработка событий
    def accept_events(self):
        #смена вида
        base.accept('c', self.changed_view)

        #поворот влево/вправо, вверх/вниз
        base.accept('n', self.turn_left)
        base.accept('n' + '-repeat', self.turn_left)

        base.accept('m', self.turn_right)
        base.accept('m' + '-repeat', self.turn_right)

        base.accept('v', self.turn_up)
        base.accept('v' + '-repeat', self.turn_up)

        base.accept('b', self.turn_down)
        base.accept('b' + '-repeat', self.turn_down)

        #движение игрока влево/вправо, вверх/вниз
        base.accept('w', self.move_forward)
        base.accept('w' + '-repeat', self.move_forward)

        base.accept('a', self.move_left)
        base.accept('a' + '-repeat', self.move_left)

        base.accept('s', self.move_back)
        base.accept('s' + '-repeat', self.move_back)
        
        base.accept('d', self.move_right)
        base.accept('d' + '-repeat', self.move_right)

        base.accept('q', self.move_up)
        base.accept('q' + '-repeat', self.move_up)

        base.accept('e', self.move_down)
        base.accept('e' + '-repeat', self.move_down)

        #смена игрового режима
        base.accept('z', self.changed_mode)

        #добавление/удаление блока
        base.accept('f', self.build)
        base.accept('g', self.destroy)

        #сохранение и загрузка карты
        base.accept('k', self.land.save_map)
        base.accept('l', self.land.load_map)