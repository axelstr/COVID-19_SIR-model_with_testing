from model import Model
import example_simulation
import example_analysis
import os


def main():
    model = Model(servers=0)
    model.run()
    model.plot()


if __name__ == '__main__':
    main()
    os.system('python example_simulation.py')
    os.system('python example_analysis.py')
