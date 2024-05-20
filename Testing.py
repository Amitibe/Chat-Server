def main():
    with open("Game.py", "r") as file:
        return file.read()
def play(x):

    exec(x)
if __name__ == '__main__':
    x = main()
    play(x)
