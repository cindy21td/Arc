# Name: Marcella Cindy Prasetio
# ID: 1335797
# Email: mcp21@cs.washington.edu
# CSE 446 - Homework 3
#
# Train a perceptron given a Kernel function
import random
from math import exp, sqrt
from data import load_valid_data, load_test_data

# Calculates the dot product between two vectors
def dot(x, y):
    s = 0
    # iterate each dimension in the lists
    for i in range(0, len(x)):
		s += (x[i] * y[i])
    return s

# Calculates the magnitude between the two vectors
def magnitude(x, y):
	s = []
	# get the diff
	for i in range(0, len(x)):
		s.append(x[i] - y[i])
	# calculate the magnitude
	mag = 0
	for n in s:
		mag += pow(n, 2)

	return sqrt(mag)

# Predicts the given point label based on the list of mistakes
# and the given kernel function and parameter
def predict(point, mistakes, kernel_fn, kp):
	val = 0
	for m in mistakes:
		val += m['label'] * kernel_fn(point['pixels'], m['pixels'], kp)
	# return the sign
	if val > 0:
		return 1
	else:
		return -1

# Trains the perceptron with the given kernel
def train(data, kernel_fn, kp, mistakes):
	# each pass of the data
	for d in data:
		# classify with current weights
		y = predict(d, mistakes, kernel_fn, kp)
		# check for mistake
		if y != d['label']:
			# wrong, put point to mistakes
			mistakes.append(d)
	return mistakes

# Submissions function to run Task 1-3
def submission():
	# load the data
	v_data = load_valid_data()
	t_data = load_test_data()

	# calculate the average loss
	print "===== #1 ====="
	# ======================
	# 	Task number 1
	# ======================
	start = 0
	end = 100
	mistakes = []
	# Train from steps 0 - 1000
	for i in range(0, 10):
		# Train using the first kernel
		mistakes = train(v_data[start:end], kernel_one, 1, mistakes)
		avg = calculate_loss(end, mistakes)

		print "  Average on step ", start, "-", end , ": ", avg
		# next
		start = end
		end += 100

	print
	print "===== #2 ====="
	# ===================
	# 	Task number 2
	# ===================
	steps = 1000
	d = [1, 3, 5, 7, 10, 15, 20]
	# Try over all d
	for p in d:
		mistakes = []
		# Train using the second kernel
		mistakes = train(v_data[:steps], kernel_two, p, mistakes)
		avg = calculate_loss(steps, mistakes)

		print "  For d ", p , " steps=", steps, ": ", avg

	print
	print "===== #3 ====="
	# =====================
	# 	Task number 3
	# =====================
	# choosen d = 5
	# do kernel two first
	d = 5
	start = 0
	end = 100
	mistakes = []
	# Iterate from steps 0 - 1000
	for i in range(0, 10):
		# train using second kernel with d = 5
		mistakes = train(t_data[start:end], kernel_two, d, mistakes)
		avg = calculate_loss(end, mistakes)

		print "  d=", d, " k2 average on step ", start, "-", end , ": ", avg

		start = end
		end += 100

	print

	# do kernel three now
	sigma = 10
	start = 0
	end = 100
	mistakes = []
	# Iterate from steps 0 - 1000
	for i in range(0, 10):
		# Train using the third kernel with sigma = 10
		mistakes = train(t_data[start:end], kernel_three, sigma, mistakes)
		avg = calculate_loss(end, mistakes)

		print "  sigma=", sigma, " k3 average on step ", start, "-", end , ": ", avg

		start = end
		end += 100

# Calculates the average loss from the given steps and mistakes
def calculate_loss(steps, mistakes):
	return (float(len(mistakes)) / steps)


# The first kernel with dot product + 1, kp param always = 1
def kernel_one(u, v, kp):
	return dot(u, v) + 1

# The second kernel, kp param = d
def kernel_two(u, v, kp):
	# d = [1, 3, 5, 7, 10, 15, 20]
	d = kp
	return pow((dot(u, v) + 1), d)

# The third kernel, kp = sigma
def kernel_three(u, v, kp):
	sigma = kp
	return exp((-1 * magnitude(u, v)) / (2 * pow(sigma, 2)))



# run submission()
submission()