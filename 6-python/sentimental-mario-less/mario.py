# Mario in Python


def main():
    """Keep doing this prompt if user input is < 1 or > 8 or non-numeric."""
    try:
        height = 0
        while height < 1 or height > 8:
            height = int(input("Height: "))
    except ValueError:
        main()

    # Function call to print pyramid
    print_pyramid(height)


def print_pyramid(height):
    """Prints out a left-aligned half-pyramid of a specified height."""

    # For each row, start, stop, step
    # <- Left side
    # On left side for each line, print a space before a brick
    for i in range(1, height + 1, 1):
        print(" " * (height - i), end="")

        # Then print a brick
        print("#" * i)


if __name__ == '__main__':
    main()