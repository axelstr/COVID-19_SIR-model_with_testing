from model import Model


def main():
    # model = Model(duration=365*2, timeStep=1, susceptible=1000,
    #               infected=1, removed=0, rateSI=0.05, rateIR=0.01)

    model = Model(duration=40, timeStep=1, susceptible=100,
                  infected=10, removed=0, rateSI=.2,
                  servers=1)
    model.run()
    model.plot()


if __name__ == '__main__':
    main()
