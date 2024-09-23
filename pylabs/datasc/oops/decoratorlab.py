from datetime import time, datetime


def processresults(x: int, y: int):
    print(x, y)
    yield x+y
    print (x+y)
    yield x*y
    print(x*y)


if __name__ == '__main__':
    gen = processresults(3,6)
    print(datetime.now())
    print(next(gen))
    print(next(gen))