"""Birdroom OOP course project: birds, cages and room placement."""
from datetime import datetime, date
from calendar import monthrange
from random import randint

SPECIES = {"Z": "Zebra Finch", "G": "Gouldian Finch", "B": "Budgerigar", "L": "Lovebird"}

def valid_id(value):
    if not isinstance(value, str) or not value or not value.isascii() or not value.isalnum() or value != value.upper():
        raise ValueError("ID must contain uppercase ASCII letters and digits only.")

def age_parts(birth):
    born = datetime.strptime(birth, "%d:%m:%Y").date()
    now = date.today()
    if born > now:
        raise ValueError("Birth date cannot be in the future.")
    years, months, days = now.year-born.year, now.month-born.month, now.day-born.day
    if days < 0:
        months -= 1
        previous_month = now.month-1 or 12
        previous_year = now.year if now.month > 1 else now.year-1
        days += monthrange(previous_year, previous_month)[1]
    if months < 0:
        years -= 1
        months += 12
    return years, months, days

class Bird:
    def __init__(self, ID: str, btype: str, birth: str, colors: list, foodtype: str, volume: int):
        self.valid_check(ID, btype, birth, colors, foodtype, volume)
        self.id, self.btype, self.birth = ID, btype, birth
        self.colors, self.foodtype, self.volume = list(colors), foodtype.capitalize(), volume

    @staticmethod
    def valid_check(ID, btype, birth, colors, foodtype, volume):
        valid_id(ID)
        if btype not in SPECIES:
            raise ValueError("Unknown bird species.")
        if not isinstance(birth, str):
            raise ValueError("Birth date must be a string.")
        age_parts(birth)
        if not isinstance(colors, list) or not colors or not all(isinstance(c,str) and c.strip() for c in colors):
            raise ValueError("Colors must be a nonempty list of strings.")
        if not isinstance(foodtype,str) or foodtype.lower() not in ("seeds","corn"):
            raise ValueError("Food must be seeds or corn.")
        if type(volume) is not int or volume <= 0:
            raise ValueError("Required volume must be positive.")

    def get_age(self):
        y,m,d = age_parts(self.birth)
        return f"{y}Y,{m}M,{d}D"
    def get_age_in_years(self):
        return age_parts(self.birth)[0]
    def get_type(self):
        return self.btype
    def get_colors(self):
        return list(self.colors)
    def get_food_type(self):
        return self.foodtype
    def get_volume(self):
        return self.volume
    def __eq__(self, other):
        return self.btype == other.btype if isinstance(other, Bird) else NotImplemented
    def __lt__(self, other):
        return len(self.colors) < len(other.colors) if isinstance(other, Bird) else NotImplemented
    def __gt__(self, other):
        return len(self.colors) > len(other.colors) if isinstance(other, Bird) else NotImplemented
    def __str__(self):
        return (f"Bird ID: {self.id}\nBird type: {SPECIES[self.btype]}\n"
                f"Age: {self.get_age()}\nColors: {self.colors}\nFood type: {self.foodtype}")

class Finch(Bird):
    def __init__(self, ID, btype, birth, colors, volume):
        if btype not in ("Z","G"):
            raise ValueError("Finch must be Z or G.")
        super().__init__(ID,btype,birth,colors,"Seeds",volume)
    def nest_building(self):
        return ["|"] + ["_"] * self.get_age_in_years() + ["|"]

class Parrot(Bird):
    def __init__(self, ID, btype, birth, colors, volume):
        if btype not in ("B","L"):
            raise ValueError("Parrot must be B or L.")
        super().__init__(ID,btype,birth,colors,"Corn",volume)
    def find_nestbox(self):
        n = max(2,self.get_age_in_years())
        return [["*"]*n] + [["*"]+[" "]*(n-2)+["*"] for _ in range(n-2)] + [["*"]*n]

class Zebrafinch(Finch):
    def __init__(self, ID, birth, colors):
        super().__init__(ID,"Z",birth,colors,27000)
    def jump(self):
        return "I like to jump"

class Gouldianfinch(Finch):
    def __init__(self, ID, birth, colors):
        super().__init__(ID,"G",birth,colors,96000)
        self.vocal_power = randint(1,10)
    def sing(self):
        return f"I like to sing - {self.vocal_power}"
    def __str__(self):
        return super().__str__()+f"\nSinging strength: {self.vocal_power}"

class Budgerigar(Parrot):
    def __init__(self, ID, birth, colors):
        super().__init__(ID,"B",birth,colors,96000)
        self.vocal_power = randint(1,10)
    def tweet(self):
        return f"I like to tweet - {self.vocal_power}"
    def __str__(self):
        return super().__str__()+f"\nTweeting strength: {self.vocal_power}"

class Lovebird(Parrot):
    def __init__(self, ID, birth, colors):
        super().__init__(ID,"L",birth,colors,120000)
    def kiss(self):
        return "I like to kiss"

class Cage:
    permitted_colors = ("Silver","Black","White")
    def __init__(self, ID: str, length: int, depth: int, height: int, color: str):
        self.valid_check(ID,length,depth,height,color)
        self.id,self.length,self.depth,self.height,self.color = ID,length,depth,height,color
        self.capable_size = length*depth*height
        self.current_size = 0
        self.birds = []
    @staticmethod
    def valid_check(ID,length,depth,height,color):
        valid_id(ID)
        if color not in Cage.permitted_colors:
            raise ValueError("Unsupported cage color.")
        dims = (length,depth,height)
        if any(type(d) is not int or d%10 for d in dims):
            raise ValueError("Dimensions must be integer multiples of 10 cm.")
        if not (30<=length<=180 and 30<=depth<=60 and 40<=height<=180):
            raise ValueError("Cage dimensions out of range.")
    def add_bird(self,bird):
        if not isinstance(bird,Bird) or any(b is bird for b in self.birds):
            return False
        if self.birds and self.birds[0].get_type()!=bird.get_type():
            return False
        if self.current_size+bird.get_volume()>self.capable_size:
            return False
        self.birds.append(bird)
        self.current_size+=bird.get_volume()
        return True
    def get_birds(self):
        return list(self.birds)
    def get_num_of_birds(self):
        return len(self.birds)
    def get_cage(self):
        char=self.birds[0].get_type() if self.birds else "#"
        return [char*(self.length//10) for _ in range(self.height//10)]
    def __str__(self):
        kind=SPECIES[self.birds[0].btype] if self.birds else "Empty"
        return (f"Cage ID: {self.id}\nSize: {(self.length,self.depth,self.height)}\n"
                f"Color: {self.color}\nNum of birds: {len(self.birds)}\nBirds type: {kind}")

class Birdroom:
    def __init__(self,length: float,width: float,height: float):
        self.valid_check(length,width,height)
        self.length,self.width,self.height=length,width,height
        self.cages=[]
        self.cage_positions={}
        self.capable_size=length*width*height
        self.current_size=0
    @staticmethod
    def valid_check(length,width,height):
        dims=(length,width,height)
        if any(type(d) not in (int,float) for d in dims):
            raise ValueError("Room dimensions must be numeric.")
        if not (2<=length<=10 and 2<=width<=6 and 2<=height<=3):
            raise ValueError("Room dimensions out of range.")
        if any(abs(d*10-round(d*10))>1e-8 for d in dims):
            raise ValueError("Room dimensions must use 0.1 m increments.")
    def get_cages(self):
        return list(self.cages)
    def get_birds(self):
        return [b for cage in self.cages for b in cage.get_birds()]
    def get_strength(self):
        return sum(b.vocal_power for b in self.get_birds() if isinstance(b,(Gouldianfinch,Budgerigar)))
    def add_cage(self,cage,x: float,y: float):
        if not isinstance(cage,Cage) or not cage.get_num_of_birds() or cage in self.cages:
            return False
        if any(type(v) not in (int,float) or abs(v*10-round(v*10))>1e-8 for v in (x,y)):
            return False
        if x<0 or y<0:
            return False
        w,h=cage.length/100,cage.height/100
        if x+w>self.length+1e-8 or y+h>self.height+1e-8:
            return False
        for other in self.cages:
            ox,oy=self.cage_positions[other]
            ow,oh=other.length/100,other.height/100
            if not (x+w<=ox+1e-8 or ox+ow<=x+1e-8 or y+h<=oy+1e-8 or oy+oh<=y+1e-8):
                return False
        volume=cage.capable_size/1_000_000
        if self.current_size+volume>self.capable_size+1e-8:
            return False
        self.cages.append(cage)
        self.cage_positions[cage]=(x,y)
        self.current_size+=volume
        return True
    def get_birdroom(self):
        rows,cols=round(self.height*10),round(self.length*10)
        wall=[[" "]*cols for _ in range(rows)]
        for cage in self.cages:
            x,y=self.cage_positions[cage]
            left,bottom=round(x*10),round(y*10)
            w,h=cage.length//10,cage.height//10
            char=cage.get_birds()[0].get_type()
            for row in range(bottom,bottom+h):
                for col in range(left,left+w):
                    wall[row][col]=char
        return ["".join(row) for row in wall]
    def get_most_colorful(self):
        birds=self.get_birds()
        return max(birds,key=lambda b:len(b.colors)) if birds else None
    def __str__(self):
        return (f"Size: {(self.length,self.width,self.height)}\n"
                f"Num of cages: {len(self.cages)}\nNum of birds: {len(self.get_birds())}")
