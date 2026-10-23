"""Run with python demo.py."""
from birdroom import Birdroom, Cage, Gouldianfinch, Zebrafinch

def main():
    room = Birdroom(2.5, 2.0, 2.2)
    first = Cage("CAGE1", 60, 50, 60, "Silver")
    second = Cage("CAGE2", 60, 50, 60, "Black")
    first.add_bird(Zebrafinch("Z001", "15:03:2022", ["Gray", "White"]))
    second.add_bird(Gouldianfinch("G001", "12:06:2021", ["Red", "Green", "Yellow"]))
    print("First cage placed:", room.add_cage(first, 0.0, 0.0))
    print("Second cage placed:", room.add_cage(second, 0.7, 0.0))
    print(room)
    print("Total vocal strength:", room.get_strength())
    print("Most colorful bird:", room.get_most_colorful().id)
    print("Room front view:")
    for row in reversed(room.get_birdroom()):
        print(row)

if __name__ == "__main__":
    main()
