import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py x y")
        sys.exit(1)
    # TODO: Read database file into a variable
    db = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            db.append(row)
    # print("db: ", db)
    # print("reader: ", reader.fieldnames)
    # print("db: ", db)
    fieldnames = reader.fieldnames

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2]) as file2:
        sq = file2.read()
    # print("sq:", sq)

    # TODO: Find longest match of each STR in DNA sequence
    longest_counts = {}
    # for i in range(1, len(fieldnames)):
    # print(longest_match(sq, fieldnames[i]))
    for fieldname in fieldnames[1:]:  # Start from index 1 to skip the first fieldname
        longest_counts[fieldname] = longest_match(sq, fieldname)

    # TODO: Check database for matching profiles
    matching_profile = None
    for person in db:
        match = True
        for fieldname in fieldnames[1:]:
            if int(person[fieldname]) != longest_counts[fieldname]:
                match = False
                break
        if match:
            matching_profile = person['name']
            break

    # Output the result
    if matching_profile:
        print(matching_profile)
    else:
        print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

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


main()
