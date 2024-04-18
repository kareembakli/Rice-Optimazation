#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np

# Read the dataset from CSV
dataset = pd.read_csv('rice_dataset.csv')

# Genetic Algorithm parameters
population_size = 10
num_generations = 100
mutation_rate = 0.1

# Function to evaluate the fitness of an individual
def evaluate_fitness(individual):
    # Here, we define fitness as the sum of yield and disease resistance, you can adjust this according to your needs
    return individual['yield'] + individual['disease_resistance']

# Function to initialize a population
def initialize_population():
    population = []
    for _ in range(population_size):
        individual = {}
        for gene in dataset.columns[1:]:
            # For simplicity, we randomly initialize genes for each individual
            individual[gene] = np.random.uniform(0, 1)
        population.append(individual)
    return population

# Function to perform mutation
def mutate(individual):
    for gene in individual.keys():
        if np.random.rand() < mutation_rate:
            # Mutate gene by adding a small random value
            individual[gene] += np.random.uniform(-0.1, 0.1)
            # Ensure gene stays within bounds [0, 1]
            individual[gene] = max(0, min(1, individual[gene]))
    return individual

# Function to perform crossover
def crossover(parent1, parent2):
    child = {}
    for gene in parent1.keys():
        # Crossover by selecting gene from either parent
        child[gene] = np.random.choice([parent1[gene], parent2[gene]])
    return child

# Function to select individuals for the next generation
def select(population, fitness_scores):
    # Select individuals based on their fitness scores (higher fitness is better)
    sorted_indices = np.argsort(fitness_scores)[::-1]
    selected_indices = sorted_indices[:population_size]
    return [population[i] for i in selected_indices]

# Main genetic algorithm loop
population = initialize_population()
for generation in range(num_generations):
    fitness_scores = [evaluate_fitness(individual) for individual in population]
    selected_population = select(population, fitness_scores)
    next_population = []

    while len(next_population) < population_size:
        parent1, parent2 = np.random.choice(selected_population, size=2, replace=False)
        child = crossover(parent1, parent2)
        child = mutate(child)
        next_population.append(child)

    population = next_population

# Get the best individual from the final population
best_individual = max(population, key=evaluate_fitness)
print("Best individual:", best_individual)
print("Fitness:", evaluate_fitness(best_individual))

