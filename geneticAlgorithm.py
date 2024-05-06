import random
import copy
    
NOTE_RANGE = range(53, 77)

class geneticAlgorithm: 

    def generate_genome(length, num_measures):
        melody = {
        "notes": [],
        "velocity": [],
        "beat": [],
        }

        note_length_choice = [0.25, 0.50, 1, 2, 3, 4]

        for _ in range(length):
            melody["notes"] += random.choices(NOTE_RANGE)
            melody["velocity"] += [127]
            melody["beat"] += [random.choice(note_length_choice)]

        
        while True:
            if sum(melody["beat"]) < 4 * num_measures:
                index = random.randint(0, len(melody["beat"])-1)
                note_length_added = random.choice(note_length_choice)
                melody["beat"][index] += note_length_added
                if melody["beat"][index] == 1.25 or melody["beat"][index] == 1.75:
                    melody["beat"][index] = 2
                elif melody["beat"][index] == 2.25 or melody["beat"][index] == 2.5 or melody["beat"][index] == 2.75:
                    melody["beat"][index] = 3
                elif melody["beat"][index] == 3.25 or melody["beat"][index] == 3.50 or melody["beat"][index] == 3.75:
                    melody["beat"][index] = 4
                elif melody["beat"][index] > 4:
                    melody["beat"][index] = 6

            elif sum(melody["beat"]) > 4 * num_measures:
                index = random.randint(0, len(melody["beat"])-1)
                note_length_added = random.choice(note_length_choice)
                melody["beat"][index] -= note_length_added
                if melody["beat"][index] <= 0:
                    melody["beat"][index] = 0.50
                elif melody["beat"][index] == 1.25 or melody["beat"][index] == 1.75:
                    melody["beat"][index] = 1
                elif melody["beat"][index] == 2.25 or melody["beat"][index] == 2.5 or melody["beat"][index] == 2.75:
                    melody["beat"][index] = 2
                elif melody["beat"][index] == 3.25 or melody["beat"][index] == 3.50 or melody["beat"][index] == 3.75:
                    melody["beat"][index] = 3
                elif melody["beat"][index] > 4:
                    melody["beat"][index] = 4
            
            elif sum(melody["beat"]) == 4 * num_measures:
                break

        return melody

    def generate_population(size, genome_length, num_measures):
        return [geneticAlgorithm.generate_genome(genome_length, num_measures) for i in range(size)]

    def single_point_crossover(parent1, parent2):
        a = copy.deepcopy(parent1)
        b = copy.deepcopy(parent2)
        a1 = copy.deepcopy(parent1)
        b1 = copy.deepcopy(parent2)
        if len(a) != len(b):
            raise ValueError("Genomes a and b must be of same length")

        length = len(a)
        if length < 2:
            return a, b

        p = random.randint(1, length - 1)

        a1["notes"] = a["notes"][0:p] + b["notes"][p: ]
        a1["beat"] = a["beat"][0:p] + b["beat"][p: ]

        b1["notes"] = b["notes"][0:p] + a["notes"][p: ]
        b1["beat"] = b["beat"][0:p] + a["beat"][p: ]
        return a1,b1

    def mutation(genome, num_measures, num = 1):
        note_length_choice = [0.25, 0.50, 1, 2, 3, 4]
        genome1 = copy.deepcopy(genome)
        # print(id(genome1))
        for _ in range(num):
            index = random.randrange(len(genome1["notes"]))
            choice = random.choice(["pluss", "minus"])
            note_length_added = random.choice(note_length_choice)
            if choice == "minus":
                # print("m")
                # print(index)
                # print(genome1["notes"][index])
                genome1["notes"][index] -= 1
                # print(genome1["notes"][index])
                genome1["beat"][index] -= note_length_added
                if genome1["beat"][index] <= 0:
                    genome1["beat"][index] = 0.50
                elif genome1["beat"][index] == 1.25 or genome1["beat"][index] == 1.75:
                    genome1["beat"][index] = 1
                elif genome1["beat"][index] == 2.25 or genome1["beat"][index] == 2.5 or genome1["beat"][index] == 2.75:
                    genome1["beat"][index] = 2
                elif genome1["beat"][index] == 3.25 or genome1["beat"][index] == 3.50 or genome1["beat"][index] == 3.75:
                    genome1["beat"][index] = 3
                elif genome1["beat"][index] > 4:
                    genome1["beat"][index] = 4
                
                while True:
                    if sum(genome1["beat"]) < 4 * num_measures:
                        index = random.randint(0, len(genome1["beat"])-1)
                        note_length_added = random.choice(note_length_choice)
                        genome1["beat"][index] += note_length_added
                        if genome1["beat"][index] == 1.25 or genome1["beat"][index] == 1.75:
                            genome1["beat"][index] = 2
                        elif genome1["beat"][index] == 2.25 or genome1["beat"][index] == 2.5 or genome1["beat"][index] == 2.75:
                            genome1["beat"][index] = 3
                        elif genome1["beat"][index] == 3.25 or genome1["beat"][index] == 3.50 or genome1["beat"][index] == 3.75:
                            genome1["beat"][index] = 4
                        elif genome1["beat"][index] > 4:
                            genome1["beat"][index] = 6

                    elif sum(genome1["beat"]) > 4 * num_measures:
                        index = random.randint(0, len(genome1["beat"])-1)
                        note_length_added = random.choice(note_length_choice)
                        genome1["beat"][index] -= note_length_added
                        if genome1["beat"][index] <= 0:
                            genome1["beat"][index] = 0.50
                        elif genome1["beat"][index] == 1.25 or genome1["beat"][index] == 1.75:
                            genome1["beat"][index] = 1
                        elif genome1["beat"][index] == 2.25 or genome1["beat"][index] == 2.5 or genome1["beat"][index] == 2.75:
                            genome1["beat"][index] = 2
                        elif genome1["beat"][index] == 3.25 or genome1["beat"][index] == 3.50 or genome1["beat"][index] == 3.75:
                            genome1["beat"][index] = 3
                        elif genome1["beat"][index] > 4:
                            genome1["beat"][index] = 4
                    
                    elif sum(genome1["beat"]) == 4 * num_measures:
                        break
            else:
                # print("p")
                # print(index)
                # print(genome1["notes"][index])
                genome1["notes"][index] += 1
                # print(genome1["notes"][index])
                genome1["beat"][index] += note_length_added
                if genome1["beat"][index] <= 0:
                    genome1["beat"][index] = 0.50
                elif genome1["beat"][index] == 1.25 or genome1["beat"][index] == 1.75:
                    genome1["beat"][index] = 1
                elif genome1["beat"][index] == 2.25 or genome1["beat"][index] == 2.5 or genome1["beat"][index] == 2.75:
                    genome1["beat"][index] = 2
                elif genome1["beat"][index] == 3.25 or genome1["beat"][index] == 3.50 or genome1["beat"][index] == 3.75:
                    genome1["beat"][index] = 3
                elif genome1["beat"][index] > 4:
                    genome1["beat"][index] = 4
                
                while True:
                    if sum(genome1["beat"]) < 4 * num_measures:
                        index = random.randint(0, len(genome1["beat"])-1)
                        note_length_added = random.choice(note_length_choice)
                        genome1["beat"][index] += note_length_added
                        if genome1["beat"][index] == 1.25 or genome1["beat"][index] == 1.75:
                            genome1["beat"][index] = 2
                        elif genome1["beat"][index] == 2.25 or genome1["beat"][index] == 2.5 or genome1["beat"][index] == 2.75:
                            genome1["beat"][index] = 3
                        elif genome1["beat"][index] == 3.25 or genome1["beat"][index] == 3.50 or genome1["beat"][index] == 3.75:
                            genome1["beat"][index] = 4
                        elif genome1["beat"][index] > 4:
                            genome1["beat"][index] = 6

                    elif sum(genome1["beat"]) > 4 * num_measures:
                        index = random.randint(0, len(genome1["beat"])-1)
                        note_length_added = random.choice(note_length_choice)
                        genome1["beat"][index] -= note_length_added
                        if genome1["beat"][index] <= 0:
                            genome1["beat"][index] = 0.50
                        elif genome1["beat"][index] == 1.25 or genome1["beat"][index] == 1.75:
                            genome1["beat"][index] = 1
                        elif genome1["beat"][index] == 2.25 or genome1["beat"][index] == 2.5 or genome1["beat"][index] == 2.75:
                            genome1["beat"][index] = 2
                        elif genome1["beat"][index] == 3.25 or genome1["beat"][index] == 3.50 or genome1["beat"][index] == 3.75:
                            genome1["beat"][index] = 3
                        elif genome1["beat"][index] > 4:
                            genome1["beat"][index] = 4
                    
                    elif sum(genome1["beat"]) == 4 * num_measures:
                        break

        return genome1