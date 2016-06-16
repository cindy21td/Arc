# Name: Marcella Cindy Prasetio
# ID  : 1335797
# mcp21@cs.washington.edu
#
# CSE 490U - Homework 5
#
# Main module for the NER perceptron

import sys
import numpy as np
from scipy.sparse import csr_matrix
from parser import parse_file
from features import build_vector_template, phi, total_phi


# HYPER PARAMETERS
# Number of iteration (T)
EPOCH = 15


# Returns the dot product of the w and feature vector
def dot(w, feature):
    total = 0
    for f in feature:
        if f not in w:
            continue
        total += w[f]
    return total


# Returns the index and maximum pi value with the given params
def get_max_pi(x, i, tag_curr_idx, pi, tags, w):
    max_val = None
    idx = -1

    # For initial pi (index = 1) at the begining of sentence    
    if i == 1:
        tag_prev = None
        pi_prev = pi[i-1][0]

        feature = phi(x, i-1, tag_prev, tags[tag_curr_idx])

        val = pi_prev + dot(w, feature)
        return (0, val)

    # iterate over tag prev
    for k in range(0, len(tags)):
        tag_prev_idx = k
        pi_prev = pi[i-1][k]

        feature = phi(x, i-1, tags[tag_prev_idx], tags[tag_curr_idx])
        
        val = pi_prev + dot(w, feature)

        if max_val == None or max_val < val:
            max_val = val
            idx = tag_prev_idx

    # return the index and max val
    return (idx, max_val)


# Returns the optimal NER tags for the given sentence
def viterbi(sen, w, tags):
    pi = np.empty([len(sen) + 1, len(tags)], dtype=np.int)
    bp = np.empty([len(sen) + 1, len(tags)], dtype=np.int)

    # initialize
    for i in range(0, len(tags)):
        pi[0][i] = 0
        bp[0][i] = -1

    # run viterbi
    for i in range(1, len(sen) + 1):
        # iterate for every curr tag
        for j in range(0, len(tags)):
            tag_curr_idx = j
            (idx, val) = get_max_pi(sen, i, tag_curr_idx, pi, tags, w)
            # set curr value in pi and bp
            pi[i][tag_curr_idx] = val
            bp[i][tag_curr_idx] = idx

    # get the last idx
    max_val = None
    last_idx = -1
    for i in range(0, len(tags)):
        val = pi[len(sen)][i]
        if max_val == None or max_val < val:
            max_val = val 
            last_idx = i

    # iterate the bp
    predict = []
    for i in range(len(sen), 0, -1):
        predict.insert(0, tags[last_idx])
        last_idx = bp[i][last_idx]

    return predict


# Updates the given w
def update_w(w, Phi_actual, Phi_predict):
    for i in Phi_actual:
        if i not in w:
            continue
        w[i] += Phi_actual[i]
    for i in Phi_predict:
        if i not in w:
            continue
        w[i] -= Phi_predict[i]
    return w


# Updates the W_average
def update_w_ave(w, w_ave):
	for k in w:
		w_ave[k] += w[k]
	return w_ave


# Trains the perceptron with the given data and returns W
def train(data, template, tags):
    # initialize w
    # mu, std
    w = template
    w_ave = dict(w)

    count = 0

    for t in range(0, EPOCH):
        print("\tStarting epoch: ", t)
        # process each sentence 
        for i in range(0, len(data)):
            print("\t\t--Processing sentence", i, "--")

            d = data[i]
            predict = viterbi(d, w, tags)
            actual = d[:, 3].tolist()
			

            update = False
            for i in range(0, len(predict)):
                if predict[i] != actual[i]:
                    update = True
            if not update:
                continue

            Phi_predict = total_phi(d, predict)
            Phi_actual = total_phi(d, actual)

            # update w
            w = update_w(w, Phi_actual, Phi_predict)    

            # update w_ave
            w_ave = update_w_ave(w, w_ave)

            count += 1

    # average out w
    for k in w_ave:
    	w_ave[k] = float(w_ave[k])/ count
    return w_ave


# Tests the given data with the given w
def test(data, w, tags):
    output = []
    for i in range(0, len(data)):
        print("\t\tTesting sentence ", i)
        sen = []
        d = data[i]
        predict = viterbi(d, w, tags)

        for j in range(0, len(d)):
            ans = np.append(d[j], [predict[j]])
            sen.append(ans)

        output.append(sen)
    return output


# Writes the output to the given fname
def write_output(fname, output):
    with open(fname, 'w') as f:
        for d in output:
            for x in d:
                txt = ""
                for y in x:
                    txt += y + " "
                f.write(txt + '\n')
            f.write('\n')
    f.close()


# Main module to run the perceptron
def main():
    # check argument
    if len(sys.argv) < 4:
        print("Incorrect number of argument")
        print("Usage: python NER.py <train-file> <test-file> <output-file>")
        exit()

    # get the data
    train_data = parse_file(sys.argv[1])
    test_data = parse_file(sys.argv[2])

    # build the feature template and tags
    print("--Building feature templates--")
    (temp, tags) = (build_vector_template(train_data))   

    # train the data
    print("--Training the regression--")
    w = train(train_data, temp, tags)

    # test the data
    print("--Testing the regression")
    output = test(test_data, w, tags)

    # write output
    print("--Writing output--")
    write_output(sys.argv[3], output)

    print("--Finished--")

    return


if __name__ == "__main__":
    main()
