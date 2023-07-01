import random
import matplotlib.pyplot as plt


def did_we_loose(pos_state, previous_action, previous_pos):
    if pos_state == "_" or pos_state == "M":
        return False
    elif pos_state == "G":
        return previous_action != "1"  # just if we jump then we can skip the Gumpa
    elif pos_state == "L":
        if previous_pos == "L": return True
        return previous_action != "2"  # just if we dodge then we can skip the Lakipo


def get_score(level, actions):
    if len(level) != len(actions): raise "actions len  and  level len is different."
    score = 0
    complete_steps = []
    complete_step_counter = 0
    step = 0

    while step < len(actions):

        if step == 0:
            result = did_we_loose(level[step], "0", "_")  # at the first home we don't hava previous action
        else:
            result = did_we_loose(level[step], actions[step - 1], level[step - 1])
        if result:  # we have lost
            complete_steps.append(complete_step_counter)
            complete_step_counter = 0
        else:
            complete_step_counter += 1
            if level[step] == "M": score += 2
        step += 1

    complete_steps.append(complete_step_counter)
    score+=10-(len(complete_steps)-1)*3
    return score


def generate_primary_chromosomes(number, length):
    chromosomes = []
    for _ in range(number):
        chromosome = ""
        for _ in range(length):
            chromosome = chromosome + str(random.choice([0, 0, 0, 1, 2]))
        chromosomes.append(chromosome)
    return chromosomes


def chromosomes_score(level, chromosomes):
    chromosome_score = []
    for chromosome in chromosomes:
        chromosome_score.append((chromosome, get_score(level, chromosome)))
    return chromosome_score


def select(chromosomes):
    """    sum_of_scores = sum([x[1] for x in chromosomes])
    normalized_chromosomes = [(x[0], x[1] / sum_of_scores) for x in chromosomes]
    selected = []

    for _ in range(len(chromosomes)//2):
        randNum = random.random()
        for x in normalized_chromosomes:
            if randNum < float(x[0]):
                selected.append(x[0])
                break
            else:
                randNum -= randNum
    return selected"""

    chromosomes.sort(key=lambda x: x[1], reverse=True)
    selected_chromosomes = [x[0] for x in chromosomes]
    return selected_chromosomes[0:len(chromosomes) // 2]




def parents(selected_chromosomes):
    parents = []
    random.shuffle(selected_chromosomes)

    i = 0
    while True:
        if i < len(selected_chromosomes) and i + 1 < len(selected_chromosomes):
            parents.append([selected_chromosomes[i], selected_chromosomes[i + 1]])
            i += 2
        elif i < len(selected_chromosomes):
            parents.append([selected_chromosomes[i], selected_chromosomes[0]])
            break
        else:
            break
    return parents


def recombination(parents):
    children = []
    for i in range(len(parents)):
        f_chrom, s_chrom = parents[i]  # first and second children
        l = len(f_chrom)
        f_child_chrom = f_chrom[0:l // 2] + s_chrom[l // 2:]
        s_child_chrom = s_chrom[0:l // 2] + f_chrom[l // 2:]
        children.append(f_child_chrom)
        children.append(s_child_chrom)
    return children


def mutation(chromosome):
    mutation_chance = 0.1
    if random.random() <= mutation_chance:
        i = random.randrange(0, len(chromosome))
        bits = list(chromosome)
        bits[i] = "0"
        chromosome = ''.join(bits)
    return chromosome


def chromosomes_mutation(chromosomes):
    return [mutation(chromosome) for chromosome in chromosomes]


def chart(min, average, max):
    plt.plot(range(len(min)), min)
    plt.plot(range(len(min)), average)
    plt.plot(range(len(min)), max)
    plt.show()


class Game:
    def __init__(self, levels):
        # Get a list of strings as levels
        # Store level length to determine if a sequence of action passes all the steps

        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0

    def load_next_level(self):
        self.current_level_index += 1
        self.current_level_len = len(self.levels[self.current_level_index])

    def iteration(self, level, ch_number, ch_len, round):
        min_score_iter = []
        average_score_iter = []
        max_score_iter = []
        primary_chromosomes = generate_primary_chromosomes(ch_number, ch_len)
        for _ in range(round):
            chromosomes_scores = chromosomes_score(level, primary_chromosomes)
            all_scores = [int(x[1]) for x in chromosomes_scores]
            min_score_iter.append(min(all_scores))
            average_score_iter.append(sum(all_scores) // len(all_scores))
            max_score_iter.append(max(all_scores))
            selected_chromosomes = select(chromosomes_scores)
            parents_chromosomes = parents(selected_chromosomes)
            recombined_chromosomes = recombination(parents_chromosomes)
            mutated_chromosomes = chromosomes_mutation(recombined_chromosomes)
            other_chromosomes_num = ch_number - len(
                mutated_chromosomes)  # number of chromosomes we have to choose to complete the number of chromosomes
            primary_chromosomes = mutated_chromosomes + selected_chromosomes[:other_chromosomes_num]

        chart(min_score_iter, average_score_iter, max_score_iter)
        return primary_chromosomes


g = Game(["__________", "___________"])
g.load_next_level()
level = "____G_G_MMM___L__L_G_____G___M_L__G__L_GM____L____"
print(g.iteration(level, 200, len(level), 20))
