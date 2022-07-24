# -*- coding: utf-8 -*-

import numpy as np



def compute_transition_matrix(seq):
    """ Function for computing the transition matrix between characters for a given sequence in input. """

    unique_states = np.unique(seq)
    nb_states = len(unique_states)

    A = np.zeros((nb_states+1, nb_states+1)) # +1 = an additional state for beginning or ending a sentence.

    # count the transitions
    for i in range(len(seq)-1):

        if seq[i] in ['.', '!', '?']:
            A[np.where(unique_states == seq[i]), -1] += 1
            if seq[i+1]==' ' and i+2<len(seq): # If this is a space, we focus on the next character
                A[-1, np.where(unique_states == seq[i + 2])] += 1
                i += 1
            else:
                A[-1, np.where(unique_states == seq[i + 1])] += 1
        else:
            A[np.where(unique_states == seq[i]), np.where(unique_states == seq[i + 1])] += 1

    # normalization
    for i in range(nb_states+1):
        norm = A[i,:].sum()
        A[i,:] /= norm

    return A


def generate_sequences(set_states, A, N):
    """ Generate N sequences using the transition matrix A and according to the possible states defined in set_states """

    list_seq_gen = []
    for i in range(N):

        seq_gen = ''
        elmt_gen = np.random.choice(set_states, p=A[-1,:-1]) # first term
        index_elmt = int(np.where(set_states==elmt_gen)[0])
        seq_gen += elmt_gen
        while elmt_gen not in ['.', '!', '?']:
            #print(elmt_gen, index_elmt)
            elmt_gen = np.random.choice(set_states, p=A[index_elmt,:-1])
            index_elmt = int(np.where(set_states == elmt_gen)[0])
            seq_gen += elmt_gen

        list_seq_gen.append(seq_gen)

    return list_seq_gen


if __name__ == '__main__':


    # load book. The book with be a list of characters
    with open('../tp1_seq_analysis/oliver_twist.txt') as my_file:
        book = []
        for line in my_file.readlines():
            new_line = line.replace('\n', ' ')
            book += new_line

    # book = ['A', 'B', 'B', '.', 'A', 'A', 'C', 'B', 'B', 'A'] # test example

    # analysis
    unique_states = np.unique(book)
    print("STATES (characters) = ", unique_states, "\nNumber of states  = ", len(unique_states))


    # character modeling
    A = compute_transition_matrix(book)
    print("TRANSITION MATRIX")
    print(A)

    # generation
    N = 10
    gen_sequences = generate_sequences(unique_states, A, N)
    print("GENERATED SENTENCES")
    for gen_seq in gen_sequences:
        print(gen_seq)
