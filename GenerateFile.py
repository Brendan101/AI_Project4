import sys
import random

def main():

    outfile = open("generated_test.txt", "w")

    min = -100
    max = 100
    points = 200
    for i in range(0, points):
        outfile.write(str(random.uniform(min, max)) + " " + str(random.uniform(min, max)) + "\n")

    outfile.close()
        

if __name__ == "__main__": main()
