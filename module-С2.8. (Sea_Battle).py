# Добавляем Рандом для компьютера
from random import randint

# Точки выстрелов
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

# Общий класс исключений
class BoardException(Exception):
    pass

# Ошибка, выстрел за доску
class BoardOutException(BoardException):
    def __str__(self):
        return "Вы выстрелили за доску, попробуйте еще раз и в этот раз будьте точнее!"

# Ошибка, повторный выстрел
class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку, попробуйте еще раз!"

# Исключение для размещения кораблей
class BoardWrongShipException(BoardException):
    pass

# Корабли
class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

# Точки корабля
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x 
            cur_y = self.bow.y
            
            if self.o == 0:
                cur_x += i
            
            elif self.o == 1:
                cur_y += i
            
            ship_dots.append(Dot(cur_x, cur_y))
        
        return ship_dots

# Проверка на попадание
    def shooten(self, shot):
        return shot in self.dots





# Игровое поле
class Board:
    def __init__(self, hid = False, size = 6):
        self.size = size
        self.hid = hid
        
        self.count = 0
        
        self.field = [ ["O"]*size for _ in range(size) ]
        
        self.busy = []
        self.ships = []
    
    def add_ship(self, ship):
        
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
        
        self.ships.append(ship)
        self.contour(ship)
            
    def contour(self, ship, verb = False):
        near = [
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "Т"
                    self.busy.append(cur)
    
    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i+1} | " + " | ".join(row) + " |"
        
        if self.hid:
            res = res.replace("■", "O")
        return res
    
    def out(self, d):
        return not((0<= d.x < self.size) and (0<= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        
        if d in self.busy:
            raise BoardUsedException()
        
        self.busy.append(d)
        
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print("Попадание! Корабль уничтожен!")
                    return False
                else:
                    print("Попадание! Корабль ранен!")
                    return True
        
        self.field[d.x][d.y] = "Т"
        print("Мимо, повезет в следующий раз!")
        return False
    
    def begin(self):
        self.busy = []

# Пользователь
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy
    
    def ask(self):
        raise NotImplementedError()
    
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

# Компьютер
class AI(Player):
    def ask(self):
        d = Dot(randint(0,5), randint(0, 5))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        return d

# Пользователь
class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            
            if len(cords) != 2:
                print(" Введите координаты X и Y! ")
                continue
            
            x, y = cords
            
            if not(x.isdigit()) or not(y.isdigit()):
                print(" Введите числа! ")
                continue
            
            x, y = int(x), int(y)
            
            return Dot(x-1, y-1)

# Процесс игры
class Game:
    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        
        self.ai = AI(co, pl)
        self.us = User(pl, co)
    
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board
    
    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

# Приветствие
    def greet(self):
        print("*******************************************************")
        print("*                    Здравствуй!                      *")
        print("*         Я хочу сыграть с тобой в одну игру!         *")
        print("*                     МОРСКОЙ БОЙ                     *")
        print("*******************************************************")
        print("*               Для игры Вам понадобится              *")
        print("*        вводить следующие данные через пробел        *")
        print("*                   Номер строки: Х                   *")
        print("*                   Номер столбца: Y                  *")
        print("*******************************************************")

# Доски для игоков
    def loop(self):
        num = 0
        while True:
            print("-"*30)
            print("Ваша доска:")
            print(self.us.board)
            print("-"*30)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-"*30)
                print("Вы Ходите!")
                repeat = self.us.move()
            else:
                print("-"*30)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            
            if self.ai.board.count == 7:
                print("-"*30)
                print("Вы выиграли, УРА!!!")
                break
            
            if self.us.board.count == 7:
                print("-"*30)
                print("Вы проиграли ... компьютер выиграл!")
                print("Попробуйте еще раз!")
                break
            num += 1

# Игра
    def start(self):
        self.greet()
        self.loop()

# Запуск игры
g = Game()
g.start()