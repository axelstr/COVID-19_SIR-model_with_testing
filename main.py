from model import Model


def main():
    model = Model(servers=0, pSymptomatic=0)
    model.run()
    model.plot()


if __name__ == '__main__':
    main()
