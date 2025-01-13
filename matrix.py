from itertools import permutations, combinations


def arrange(n: int) -> list:
    return list(permutations(range(1, n+1)))


def combine(n: int, m: int) -> list:
    return list(combinations(range(1, n+1), m))


def solve(arg_mat, constant_vec) -> list:
    result = []
    if not arg_mat.det:
        raise ValueError('Singular matrix')
    for n in range(len(arg_mat)):
        d_mat = []
        for i in range(len(arg_mat.transpose)):
            if i != n:
                d_mat.append(arg_mat.transpose[i])
            else:
                d_mat.extend(constant_vec.transpose.value)
        result.append(Matrix(d_mat).det/arg_mat.det)
    return result


'''
def combine(n: int, m: int) -> list:
    c, sub_set_list = list(range(1, n+1)), []
    for i in range(2**len(c)):
        sub_set = []
        for j in range(len(c)):
            if (i >> j) % 2 != 0:
                sub_set.append(c[j])
        sub_set_list.append(sub_set)
    return [i for i in sub_set_list if len(i) == m]
'''


def count_n(arrangement: list) -> int:
    result = 0
    for i in range(len(arrangement)):
        for j in range(i):
            result += 1 if arrangement[j] > arrangement[i] else 0
    return result


class Matrix(list):
    def __init__(self, value: list):
        if len({len(value[i]) for i in range(len(value))}) == 1:
            self.i, self.j = len(value), len(value[0])
            self.is_square = self.i == self.j
            self.value = value
            super().__init__(self.value)
        else:
            raise ValueError("This object cannot be as a matrix")

    def __str__(self) -> str:
        string = f'\n{self.__class__.__name__}({self.i}×{self.j})=\n'
        for i in range(self.i):
            for j in range(self.j):
                string += f'{self[i][j]:<20.4f}'
            string += '\n'
        return string

    def __neg__(self):
        return Matrix([[self[i][j] * (-1) for j in range(self.j)] for i in range(self.i)])

    def __add__(self, other):
        if type(other) not in [Vector, Matrix]:
            raise TypeError(f'Cannot add {type(self)} object and {type(other)} object')
        elif other.i != self.i or other.j != self.j:
            raise ValueError(f'Cannot add {self.i}*{self.j} matrix and {other.i}*{other.j} matrix')
        else:
            return Matrix([[self[i][j] + other[i][j] for j in range(self.j)] for i in range(self.i)])

    def __sub__(self, other):
        if type(other) not in [Vector, Matrix]:
            raise TypeError(f'Cannot sub {type(self)} object and {type(other)} object')
        elif other.i != self.i or other.j != self.j:
            raise ValueError(f'Cannot sub {self.i}*{self.j} matrix and {other.i}*{other.j} matrix')
        else:
            return Matrix([[self[i][j] - other[i][j] for j in range(self.j)] for i in range(self.i)])

    def __mul__(self, other):
        if type(other) in [float, int, complex]:
            return Matrix([[self[i][j] * other for j in range(self.j)] for i in range(self.i)])
        elif type(other) in [Matrix, Vector]:
            if self.j != other.i:
                raise ValueError(f'Cannot multiply {self.i}*{self.j} matrix and {other.i}*{other.j} matrix')
            else:
                array = []
                for i in range(self.i):
                    row = []
                    for j in range(other.j):
                        vector_r, vector_c = self[i], other.transpose[j]
                        row.append(sum([vector_r[a] * vector_c[a] for a in range(len(vector_r))]))
                    array.append(row)
                return Matrix(array)
        else:
            TypeError(f'Cannot multiply {type(self)} object and {type(other)} object')

    @property
    def det(self) -> int | float:
        if not self.is_square:
            raise ValueError('Is not a square matrix')
        else:
            det = 0
            for arr in arrange(self.i):
                item = 1
                for i in range(self.i):
                    item *= self[i][arr[i] - 1]
                det += (-1) ** count_n(arr) * item
        return det

    @property
    def rank(self) -> int:
        n, rank = 1, 0
        while any(self.sub_determinant_list(n)) and n <= min(self.j, self.i):
            rank += 1
            n += 1
        return rank

    def sub_determinant_list(self, n) -> list:
        all_possibilities = []
        sub_index_list_i = combine(self.i, n)
        sub_index_list_j = combine(self.j, n)
        for i_list in sub_index_list_i:
            for j_list in sub_index_list_j:
                all_possibilities.append(Matrix([[self[_i-1][_j-1] for _j in j_list] for _i in i_list]).det)
        return all_possibilities

    def algebraic_complement(self, i, j) -> int | float:
        i_list = [m for m in range(self.i) if m != i - 1]
        j_list = [n for n in range(self.j) if n != j - 1]
        return Matrix([[(-1) ** (_i + _j) * self[_i][_j] for _j in j_list] for _i in i_list]).det

    @property
    def transpose(self):
        new_value = [[self[j][i] for j in range(self.i)] for i in range(self.j)]
        return Matrix(new_value)

    @property
    def adj(self):
        return Matrix(
            [[self.algebraic_complement(i + 1, j + 1) for j in range(self.j)] for i in range(self.i)]).transpose

    @property
    def inv(self):
        if not self.is_square:
            raise ValueError('Is not a square matrix')
        elif self.det == 0:
            raise ValueError('Singular matrix')
        else:
            return self.adj * (1 / self.det)

    def exchange(self, method, *tar) -> None:
        if method == 'r':
            self[tar[0] - 1], self[tar[1] - 1] = self[tar[1] - 1], self[tar[0] - 1]
        elif method == 'c':
            mat_t = self.transpose
            mat_t[tar[0] - 1], mat_t[tar[1] - 1] = mat_t[tar[1] - 1], mat_t[tar[0] - 1]
            super().__init__(mat_t.transpose)
        else:
            raise ValueError('Unsupported function')

    def mul_k(self, method, index, k) -> None:
        if method == 'r':
            for i in range(len(self[index-1])):
                self[index-1][i] *= k
        elif method == 'c':
            mat_t = self.transpose
            for i in range(len(mat_t[index-1])):
                mat_t[index-1][i] *= k
                super().__init__(mat_t.transpose)
        else:
            raise ValueError('Unsupported function')

    def add_vector(self, method, i, j, k) -> None:
        if method == 'r':
            for _i in range(self.j):
                self[i-1][_i] += k * self[j-1][_i]
        elif method == 'c':
            mat_t = self.transpose
            for _i in range(self.j):
                mat_t[i-1][_i] += k * mat_t[j-1][_i]
                super().__init__(mat_t.transpose)
        else:
            raise ValueError('Unsupported function')

    def mat_append(self, method, other):
        if type(other) in [Vector, Matrix]:
            if method == 'r' and self.i == other.i:
                return Matrix([self[_i] + other[_i] for _i in range(self.i)])
            if method == 'c' and self.j == other.j:
                return Matrix(self.value + other.value)
            else:
                raise ValueError('Unsupported opi')
        else:
            raise TypeError(f'Can not use {type(other)}')

    @property
    def get_standard_mat(self):
        flag, flag1, flag2 = self.i, -1, 0
        for _i in range(flag):
            ls = list(range(flag))
            ls.pop(_i)
            for _j in ls:
                print(self)
                while True:
                    if self[_i][_i + flag2] and any(self[_i]):
                        self[_j] = [self[_j][k] - (self[_j][_i + flag2] / self[_i][_i + flag2]) * self[_i][k] for k in range(self.j)]
                        break
                    elif not self[_i][_i + flag2]:
                        flag2 += 1
                    else:
                        break
                if not any(self[_j]) and _j != flag1:
                    print(any(self[_j]), _j, self[_j], flag1)
                    self[_j], self[flag1] = self[flag1], self[_j]
                    flag1 -= 1
                    ls.insert(_j, _i + 1)
        return self
                
            

class Vector(Matrix):
    def __init__(self, value, is_t=0):
        if is_t:
            value = [list(value)]
        else:
            value = [[i] for i in value]
        super().__init__(value)


if __name__ == '__main__':
    matrix1 = Matrix([[1, 1, 1, 1, 1],
                      [2, 2, 2, 2, 2],
                      [3, 3, 3, 3, 3],
                      [3, 3, 3, 4, 5]])
    matrix2 = Matrix([[29.73, 89.28, 10.00],
                      [10.02, 34.92, 13.23],
                      [71.17, 56.66, 73.33],
                      [11.11, 24.40, 79.11]])
    matrix3 = Matrix([[1, 4, 9]])
    #print(solve(matrix1, Vector([1, 2, 8, 7])))
    print(matrix1.get_standard_mat)
