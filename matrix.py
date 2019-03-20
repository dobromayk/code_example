from sys import stdin


def elem1(i, j, lum, newMatr):
    for k in range(len(newMatr[0])):
        newMatr[i][k] += newMatr[j][k] * lum


def elem2(i, j, newMatr):
    for k in range(len(newMatr[0])):
        newMatr[i][k], newMatr[j][k] = newMatr[j][k], newMatr[i][k]


def elem3(i, lum, newMatr):
    for k in range(len(newMatr[0])):
        newMatr[i][k] *= lum


class MatrixError(BaseException):
    def __init__(self, matrix1, matrix2):
        self.matrix1 = Matrix(matrix1)
        self.matrix2 = Matrix(matrix2)


class Matrix:
    def __init__(self, matr):
        self.matrix = list()
        amountLines = 0
        for i in range(len(matr)):
            amountLines += 1
            line = list()
            amountColumns = 0
            for j in range(len(matr[i])):
                line.append(matr[i][j])
                amountColumns += 1
            self.matrix.append(line)
            self.amountLines = amountLines
            self.amountColumns = amountColumns

    def __str__(self):
        ans = ''
        for i in range(self.amountLines):
            for j in range(self.amountColumns):
                ans += str(self.matrix[i][j])
                if j != self.amountColumns - 1:
                    ans += '\t'
            if i != self.amountLines - 1:
                ans += '\n'
        return(ans)

    def size(self):
        return(self.amountLines, self.amountColumns)

    def __add__(self, other):
        eqLines = self.amountLines == other.amountLines
        eqColumns = self.amountColumns == other.amountColumns
        if eqLines and eqColumns:
            sumMatr = list()
            for i in range(self.amountLines):
                sumLine = list()
                for j in range(self.amountColumns):
                    sumLine.append(self.matrix[i][j] + other.matrix[i][j])
                sumMatr.append(sumLine)
            return Matrix(sumMatr)
        else:
            raise MatrixError(self.matrix, other.matrix)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            newMatr = list()
            for i in range(self.amountLines):
                newLine = list()
                for j in range(self.amountColumns):
                    newLine.append(self.matrix[i][j] * other)
                newMatr.append(newLine)
            return Matrix(newMatr)
        elif isinstance(other, Matrix):
            if self.amountColumns != other.amountLines:
                raise MatrixError(self.matrix, other.matrix)
            else:
                newMatr = list()
                for i in range(self.amountLines):
                    newLine = list()
                    for j in range(other.amountColumns):
                        newElem = 0
                        for k in range(self.amountColumns):
                            newElem += self.matrix[i][k] * other.matrix[k][j]
                        newLine.append(newElem)
                    newMatr.append(newLine)
                return Matrix(newMatr)

    __rmul__ = __mul__

    def transpose(self):
        newMatr = list()
        for i in range(self.amountColumns):
            newLine = list()
            for j in range(self.amountLines):
                newLine.append(0)
            newMatr.append(newLine)
        for i in range(self.amountLines):
            for j in range(self.amountColumns):
                newMatr[j][i] = self.matrix[i][j]
        self.matrix = newMatr
        t = self.amountColumns
        self.amountColumns = self.amountLines
        self.amountLines = t
        return Matrix(self.matrix)

    def transposed(self):
        newMatr = list()
        for i in range(self.amountColumns):
            newLine = list()
            for j in range(self.amountLines):
                newLine.append(0)
            newMatr.append(newLine)
        for i in range(self.amountLines):
            for j in range(self.amountColumns):
                newMatr[j][i] = self.matrix[i][j]
        return Matrix(newMatr)

    def solve(self, freeMembers):
        newMatr = list()
        for i in range(self.amountLines):
            newLine = list()
            for j in range(self.amountColumns):
                newLine.append(self.matrix[i][j])
            newLine.append(freeMembers[i])
            newMatr.append(newLine)
        amountColumns = self.amountColumns
        amountLines = self.amountLines
        startLine = 0
        startColumn = 0
        while startColumn < amountColumns and startLine < amountLines:
            firstNotZeroLine = -1
            for i in range(startLine, amountLines):
                if newMatr[i][startColumn] != 0:
                    firstNotZeroLine = i
            if firstNotZeroLine == -1:
                startColumn += 1
            else:
                elem2(startLine, firstNotZeroLine, newMatr)
                for numLine in range(startLine + 1, amountLines):
                    a = newMatr[numLine][startColumn]
                    lum = -a / newMatr[startLine][startColumn]
                    elem1(numLine, startLine, lum, newMatr)
                startColumn += 1
                startLine += 1
        if amountLines < amountColumns:
            raise MatrixError(self, self)
        else:
            for i in range(amountColumns):
                if newMatr[i][i] == 0:
                    raise MatrixError(self, self)
            for i in range(amountColumns):
                elem3(i, 1/newMatr[i][i], newMatr)
            for i in range(amountColumns - 1, -1, -1):
                for j in range(i - 1, -1, -1):
                    elem1(j, i, -newMatr[j][i], newMatr)
            ans = list()
            for i in range(amountColumns):
                ans.append(newMatr[i][-1] / newMatr[i][i])
            return ans


class SquareMatrix(Matrix):
        def __pow__(self, power):
            if power == 0:
                e = list()
                for i in range(self.amountLines):
                    eLine = list()
                    for j in range(self.amountColumns):
                        if i == j:
                            eLine.append(1)
                        else:
                            eLine.append(0)
                    e.append(eLine)
                return SquareMatrix(e)
            if power % 2 == 0:
                return (SquareMatrix((self * self).matrix)) ** (power // 2)
            else:
                return self * self ** (power - 1)

exec(stdin.read())
