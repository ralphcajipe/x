# DNA

# Importing the csv and sys modules.
import csv
import sys


def main():
    """
    This function takes in two command-line arguments,
    a database file and a DNA sequence file, and prints the name of the individual in the database whose
    STR counts match the STR counts in the DNA sequence.
    :return: the value of the function.
    """

    # Check for command-line usage part 1.
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        return

    # Check for command-line usage part 2.
    # This is assigning the first and second command-line arguments to the variables `database_file`
    # and `sequence_file`.
    database_file = sys.argv[1]
    sequence_file = sys.argv[2]

    # Read database file into a variable
    # This is reading the first line of the database file and storing the STRs in a list.
    with open(database_file, "r") as file:
        database = csv.reader(file)
        subsequence = []
        for row in database:
            for i in range(len(row)):
                if i != 0:
                    subsequence.append(row[i])
            break

    # Read DNA sequence file into a variable
    # Opening the file and reading the contents into a variable.
    with open(sequence_file, "r") as file:
        sequence = file.read()

    # Find longest match of each STR in DNA sequence
    # This is creating a list of the longest runs of each STR in the DNA sequence.
    dna_pattern = []
    for i in range(len(subsequence)):
        dna_pattern.append(longest_match(sequence, subsequence[i]))

    # Check database for matching profiles
    # This is opening the database file and reading it into a dict. Then, it is iterating
    # through the dict and comparing the STR counts in the DNA sequence to the STR counts in the
    # database. If the STR counts match, it prints the name of the matching individual. If the STR
    # counts do not match, it prints "No match".
    with open(database_file, "r") as file:
        dict = csv.DictReader(file)

        for row in dict:
            counter = 0
            for k in range(len(subsequence)):
                if dna_pattern[k] == int(row[subsequence[k]]):
                    counter += 1
            if counter == len(subsequence):
                print(row["name"])
                sys.exit()

    print("No match")

    # `return` is returning the value of the function.
    return


def longest_match(sequence, subsequence):
    """
    Returns length of longest run of subsequence in sequence.

    Given a sequence and a subsequence, return the longest match of the subsequence in the sequence

    :param sequence: a string of characters
    :param subsequence: a string of characters
    """

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


if __name__ == "__main__":
    main()
