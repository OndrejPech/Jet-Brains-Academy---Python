def main():
    while True:
        show_options()
        choice = int(input('Your choice:'))  # I assume user press only num 0-9
        if choice == 0:
            break
        elif choice == 1:  # adding two matrix
            m1_size = get_matrix_size()
            m1 = get_matrix(m1_size[0])
            m2_size = get_matrix_size()
            m2 = get_matrix(m2_size[0])
            if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
                print('ERROR')
            else:
                final_matrix = add_two_matrix(m1, m2)
                print_matrix(final_matrix)
            continue

        elif choice == 2:  # Multiply matrix by a constant
            m1_size = get_matrix_size()
            m1 = get_matrix(m1_size[0])
            constant = float(input('Enter constant: '))
            final_matrix = multiply_by_constant(m1, constant)
            print_matrix(final_matrix)

        elif choice == 3:  # multiply
            m1_size = get_matrix_size()
            if m1_size == (0, 0):
                continue
            m1 = get_matrix(m1_size[0])

            m2_size = get_matrix_size()
            if m2_size == (0, 0):
                continue
            m2 = get_matrix(m2_size[0])

            if len(m1[0]) != len(m2):
                print('Error')
            else:
                final_matrix = multiply_matrix(m1, m2)
                print_matrix(final_matrix)
            continue

        elif choice == 4:  # transpose
            show_transpose_options()
            transpose_num = int(input('Your choice:'))
            m1_size = get_matrix_size()
            m1 = get_matrix(m1_size[0])

            if transpose_num == 1:
                final_matrix = along_main_diagonal(m1)
            elif transpose_num == 2:
                final_matrix = along_side_diagonal(m1)
            elif transpose_num == 3:
                final_matrix = along_vertical_line(m1)
            elif transpose_num == 4:
                final_matrix = along_horizontal_line(m1)
            else:
                final_matrix = None
                # TODO check input

            print_matrix(final_matrix)

        elif choice == 5:  # determinant
            m1_size = get_matrix_size()

            m1 = get_matrix(m1_size[0])

            if len(m1) != len(m1[0]):
                print('ERROR')
            else:
                determinant = get_determinant(m1)
                print('The result is:')
                print(determinant)

        elif choice == 6:  # inverse
            m1_size = get_matrix_size()
            m1 = get_matrix(m1_size[0])

            if len(m1) != len(m1[0]):
                print('ERROR')
            else:
                final_matrix = inverse_matrix(m1)
                print_matrix(final_matrix)

        elif choice == 7:  # cofactor
            m1_size = get_matrix_size()
            m1 = get_matrix(m1_size[0])

            if len(m1) != len(m1[0]):
                print('ERROR')
            else:
                final_matrix = find_cofactor(m1)
                print_matrix(final_matrix)

        elif choice == 9:  # adjoint
            m1_size = get_matrix_size()
            m1 = get_matrix(m1_size[0])

            if len(m1) != len(m1[0]):
                print('ERROR')
            else:
                final_matrix = adjoint(m1)
                print_matrix(final_matrix)


def show_options():
    print('Choose a number:')

    options = ['1. Add matrices',
               '2. Multiply matrix by a constant',
               '3. Multiply matrices',
               '4. Transpose matrix',
               '5. Calculate a determinant',
               '6. Invert matrix',
               '7. Get cofactor of matrix',
               '8. Adjoint matrix',
               '0. Exit']

    print('\n'.join(options))


def show_transpose_options():
    print('Choose a number:')

    options = ['1. Main diagonal',
               '2. Side diagonal',
               '3. Vertical line',
               '4. Horizontal line']

    print('\n'.join(options))


def get_matrix_size():
    """ ask user to enter two numbers separate by space, return tuple(int, int)"""
    print('Enter size of matrix: ')
    user_string = input()  # assume it will be num,space,num f.e.(2 3)
    try:
        rows = int(user_string.split()[0])
        columns = int(user_string.split()[1])
        return rows, columns
    except IndexError:
        return 0, 0


def get_matrix(rows):
    """ ask user to enter matrix row. Repeat so many times, how much rows the matrix has"""
    matrix = []
    for _ in range(rows):
        row = input('matrix row:')
        matrix.append([float(i) for i in row.split()])

    return matrix


def print_matrix(matrix):
    """ as string line by line"""
    print('The result is:')
    for row in matrix:
        for item in row:
            print(str(item), end=' ')
        print()
    print()


def multiply_by_constant(m1, c):
    """ multiply matrix by constant"""
    m3 = []
    for i in range(len(m1)):
        row = []
        for j in range(len(m1[0])):
            item = c * m1[i][j]
            row.append(item)
        m3.append(row)

    return m3


def add_two_matrix(m1, m2):
    """add two matrices together"""
    m3 = []
    for i in range(len(m1)):
        row = []
        for j in range(len(m1[0])):
            item = m1[i][j] + m2[i][j]
            row.append(item)
        m3.append(row)
    return m3


def multiply_matrix(m1, m2):
    """multiply two matrices by each other"""
    m3 = []
    for i in range(len(m1)):
        row_m1 = m1[i]
        m3_row = []
        for j in range(len(m2[0])):
            column_m2 = [item[j] for item in m2]  # just j. item from each row
            res = 0
            for k in range(len(row_m1)):  # iterate through all elements of row_m1 and column_m2
                res += row_m1[k] * column_m2[k]
            m3_row.append(res)  # add result to position on the row

        m3.append(m3_row)

    return m3


def along_main_diagonal(matrix):
    """ rows became columns and vice versa """
    new_matrix = [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]
    return new_matrix


def along_side_diagonal(matrix):
    """ combinations of three transpose create this transpose """
    m1 = along_main_diagonal(matrix)
    m2 = along_vertical_line(m1)
    m3 = along_horizontal_line(m2)
    return m3


def along_vertical_line(matrix):
    """ first column became last, second column became last but one, last column became first etc...."""
    new_matrix = []
    for row in matrix:
        new_matrix.append(row[::-1])

    return new_matrix


def along_horizontal_line(matrix):
    """ first row became last, second row became last but one, last row became first etc...."""
    new_matrix = []
    for i in range(len(matrix)):
        new_matrix.append(matrix[-(i + 1)])

    return new_matrix


def get_determinant(matrix):
    """ get determinant of squared matrix """
    # for 1x1 matrix , the determinant is simply that one number
    if len(matrix) == 1:
        return matrix[0][0]

    # for 2x2 matrix we multiply elements of main diagonal by each other
    # then subtract the elements of secondary diagonal multiply by each other
    elif len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    # for 3x3 and higher
    # plus A times the determinant of the matrix that is not in first row and A's column
    # minus B times the determinant of the matrix that is not in first row and B's column
    # plus C times the determinant of the matrix that is not in first row and C's column.....
    else:
        running_determinant = 0
        for i in range(len(matrix)):
            # remove first row and column i to make matrix smaller
            minor_i = [[item for j, item in enumerate(row) if j != i] for j, row in enumerate(matrix) if j != 0]
            # multiply item i times determinant of smaller_matrix
            current_determinant_for_i = (matrix[0][i] * get_determinant(minor_i))
            # if i is odd, we must subtract the current_determinant_for_i
            sign = 1 if i % 2 == 0 else -1
            running_determinant += sign * current_determinant_for_i

        return running_determinant


def find_cofactor(matrix):
    """ return cofactor of matrix"""
    # if len(matrix) == 2:
    #     cofactor_matrix = [[matrix[1][1], matrix[1][0] * (-1)], [matrix[0][1] * (-1), matrix[0][0]]]
    #     return cofactor_matrix

    cofactor_matrix = [[0 for _ in row] for row in matrix]  # empty
    for i, row in enumerate(matrix):
        for j, column in enumerate(row):
            # remove first row and column i to make matrix smaller
            minor_ij = [[item for k, item in enumerate(row) if k != j] for q, row in enumerate(matrix) if q != i]

            cofactor = (-1) ** (i + j) * get_determinant(minor_ij)
            cofactor_matrix[i][j] = cofactor

    return cofactor_matrix


def adjoint(matrix):
    """ calculate and return adjoint of squared matrix """
    if len(matrix) == 1:
        return [[1]]
    cofactor = find_cofactor(matrix)
    return along_main_diagonal(cofactor)


def inverse_matrix(matrix):
    """
    The inverse of a matrix can be found using this formula:
    For each item in matrix we do:
    adjoint of matrix * (1 / determinant of matrix)
    """

    determinant = get_determinant(matrix)
    if determinant == 0:
        raise ValueError('Determinant can not be 0 by inverting matrix')

    adj_matrix = adjoint(matrix)

    return multiply_by_constant(adj_matrix, 1/determinant)


if __name__ == '__main__':
    main()
