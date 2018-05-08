"""Entry point to evolving the neural network. Start here."""
import logging
from optimizer import Optimizer
from tqdm import tqdm
from tkinter import *

class Application:
	def __init__(self, master=None):
		self.dataset =" "
		master.title("Projeto IA")
		self.widget1 = Frame(master)
		self.widget1.pack()
		self.msg = Label(self.widget1, text="Favor selecione a Base de dados a ser utilizada")
		self.msg["font"] = ("Calibri", "10", "bold")
		self.msg.pack ()
		self.button1 = Button(self.widget1)
		self.button1["text"] = "cifar10"
		self.button1["font"] = ("Calibri", "9")
		self.button1["width"] = 10
		self.button1.bind("<Button-1>", self.selBut1)
		self.button1.pack ()
		self.button2 = Button(self.widget1)
		self.button2["text"] = "mnist"
		self.button2["font"] = ("Calibri", "9")
		self.button2["width"] = 10
		self.button2.bind("<Button-1>", self.selBut2)
		self.button2.pack ()
		self.button3 = Button(self.widget1)
		self.button3["text"] = "Selecionar"
		self.button3["font"] = ("Calibri", "9")
		self.button3["width"] = 20
		self.button3.bind("<Button-1>", self.selBut3)
		self.button3.pack ()


	def selBut1(self, event):
		self.dataset = "cifar10"
		self.button1["background"] = "green"
		self.button2["background"] = "#DDDDDD"


	def selBut2(self, event):
		self.dataset = "mnist"
		self.button2["background"] = "green"
		self.button1["background"] = "#DDDDDD"

	def selBut3(self, event):
		if(self.dataset != " "):
			self.button3["command"] = self.widget1.quit



# Setup logging.
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG,
    filename='log.txt'
)

def train_networks(networks, dataset):
    """Train each network.

    Args:
        networks (list): Current population of networks
        dataset (str): Dataset to use for training/evaluating
    """
    pbar = tqdm(total=len(networks))
    for network in networks:
        network.train(dataset)
        pbar.update(1)
    pbar.close()

def get_average_accuracy(networks):
    """Get the average accuracy for a group of networks.

    Args:
        networks (list): List of networks

    Returns:
        float: The average accuracy of a population of networks.

    """
    total_accuracy = 0
    for network in networks:
        total_accuracy += network.accuracy

    return total_accuracy / len(networks)

def generate(generations, population, nn_param_choices, dataset):
    """Generate a network with the genetic algorithm.

    Args:
        generations (int): Number of times to evole the population
        population (int): Number of networks in each generation
        nn_param_choices (dict): Parameter choices for networks
        dataset (str): Dataset to use for training/evaluating

    """
    optimizer = Optimizer(nn_param_choices)
    networks = optimizer.create_population(population)

    # Evolve the generation.
    for i in range(generations):
        logging.info("***Doing generation %d of %d***" %
                     (i + 1, generations))

        # Train and get accuracy for networks.
        train_networks(networks, dataset)

        # Get the average accuracy for this generation.
        average_accuracy = get_average_accuracy(networks)

        # Print out the average accuracy each generation.
        logging.info("Generation average: %.2f%%" % (average_accuracy * 100))
        logging.info('-'*80)

        # Evolve, except on the last iteration.
        if i != generations - 1:
            # Do the evolution.
            networks = optimizer.evolve(networks)

    # Sort our final population.
    networks = sorted(networks, key=lambda x: x.accuracy, reverse=True)

    # Print out the top 5 networks.
    print_networks(networks[:5])

def print_networks(networks):
    """Print a list of networks.

    Args:
        networks (list): The population of networks

    """
    logging.info('-'*80)
    for network in networks:
        network.print_network()

def main():
	"""Evolve a network."""
	generations = 10  # Number of times to evole the population.
	population = 20  # Number of networks in each generation.
	dataset = 'cifar10'
	nn_param_choices = {
		'nb_neurons': [64, 128, 256, 512, 768, 1024],
		'nb_layers': [1, 2, 3, 4],
		'activation': ['relu', 'elu', 'tanh', 'sigmoid'],
		'optimizer': ['rmsprop', 'adam', 'sgd', 'adagrad',
					  'adadelta', 'adamax', 'nadam'],
	}
	root = Tk()
	application = Application(root)
	root.mainloop()
	dataset = application.dataset;


	logging.info("***Evolving %d generations with population %d*** Dataset %s" %
	(generations, population,dataset))

	generate(generations, population, nn_param_choices, dataset)

if __name__ == '__main__':
	main()
