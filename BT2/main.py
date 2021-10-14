# Usage
"""
	python main.py -pro_size 10 -func 1MAX -crossover 1X
"""

import os
import math
import argparse
import numpy as np
from sGA import genetic_algorithm
#from config import DISTRIB
from utils import initialize_population
MSSV = 19521242
DISTRIB = {
        0:[0, 0.5],
        1:[0.5, 1],
    }
RANDOM_SEED_VALUES = np.array([[MSSV+i+j for j in range(10)] for i in range(0, 100, 10)])
# print(RANDOM_SEED_VALUES)
# input()

def bisection(problem_size, optimized_function, crossover_way, bisection_th):
	population_size=4
	print("|\t\t ---> Bước 1: tìm cận trên MRPS: ")
	while population_size<=8192:
    	
		population_size=population_size*2
		check=True 
		for i in range(10):
    			
			np.random.seed(RANDOM_SEED_VALUES[bisection_th][i])
			intitial_population = initialize_population(population_size, problem_size,DISTRIB )
			success,converge_config,number_evaluations = genetic_algorithm(intitial_population,optimized_function, crossover_way,tournament_size=4)
			if not success:
				check = False
				break
		if check:
			break
	print("|\t\t ---> Cận trên MRPS là {}".format(population_size))

	# Bước 2: Tìm MRPS
	print("|\t\t ---> Bước 2: tìm MRPS: ")
	upper_N=population_size
	lower_N=population_size//2
	number_evaluations=number_evaluations
	update=False
	while (upper_N - lower_N) / upper_N > 0.1:
		
		N = math.ceil((upper_N + lower_N) / 2)

		check = True

		if not update:
			number_of_evaluations_ = 0
		for i in range(10):
    		
			np.random.seed(RANDOM_SEED_VALUES[bisection_th][i])
			
			intitial_population = initialize_population(population_size, problem_size,DISTRIB ) 	
			success, converge_config, number_of_evaluations = genetic_algorithm(initialized_population=intitial_population, 
															optimized_function=optimized_function, crossover_way=crossover_way, tournament_size=4)
			if not success:
				check = False
				break

			number_of_evaluations_ += number_of_evaluations

		if check:
			upper_N = N
			update = True
		else:
			lower_N = N
			update = True
			
		if upper_N - lower_N <= 2:
			break
	print("|\t\t ---> [INFO] giá trị MRPS {}".format(upper_N))
	print("|\t\t ---> [INFO] Số lượng trung bình phép evaluation  {}".format(number_of_evaluations_/10))

	return (upper_N, number_of_evaluations_/10)
def main(args):
    
	# Create directory to optimized function
	print(os.listdir())
	function_directory = os.path.join('hypothesis', args['function'])
	if not os.path.exists(function_directory):
		os.mkdir(function_directory)

	# Create directory for crossover
	crossover_directory = os.path.join(function_directory, args['crossover_way'])
	if not os.path.exists(crossover_directory):
		os.mkdir(crossover_directory)


	saving_path = os.path.join(crossover_directory, str(args['problem_size']).zfill(3) + '.npy')


	# Run 10 times bisection
	storage_result = []

	for i in range(10):
		print("| ---> Running {}th bisection ...".format(i+1))
		upperbound_popsize, average_evaluations = bisection(problem_size=args['problem_size'], 
							optimized_function=args['function'], crossover_way=args['crossover_way'], bisection_th=i)
		print(upperbound_popsize, average_evaluations)

		storage_result.append(np.array([upperbound_popsize, average_evaluations])) 
	
	with open(saving_path, 'wb+') as f:
		np.save(f, np.array(storage_result))



if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='Solve 1MAX and Trap5 problem using sGA.')
	parser.add_argument('--problem_size', '-pro_size', type=int 
						,required=True, choices=[4, 10, 20, 40, 80, 160] 
	                    , help='The problem size.')
	parser.add_argument('--function', '-func', choices=['1MAX', 'TRAP5'], required=True
						,help='The function need to be optimized')
	parser.add_argument('--crossover_way', '-crossover', choices=['1X', 'UX'], required=True
						,help='The way we make the crossover in each generation.')
	args = vars(parser.parse_args())
	
	main(args)
	
