from model import Model


def main():
    model = Model(duration=365, servers=0)
    model.run()
    model.plot('example_simulation.png')


if __name__ == '__main__':
    main()
