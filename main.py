import copy
from fractions import Fraction
from pprint import pprint
import numpy as np
import sympy as sp

class MatrixModule:
    @staticmethod
    def printMatrix(matrix):
        for row in matrix:
            print(" ".join(str(element) for element in row))

        print()

    @staticmethod
    def swapRow(matrix, rowIndex1, rowIndex2):
        if not 0 <= rowIndex1 < len(matrix) or not 0 <= rowIndex2 < len(matrix):
            return matrix
        
        matrix[rowIndex1], matrix[rowIndex2] = matrix[rowIndex2], matrix[rowIndex1]

    @classmethod
    def setCorrectLeadingElementsRows(cls, matrix):
        currentLeadingElementRowIndex = 0
        currentLeadingElementColIndex = 0
        swapped = False
        
        for row in range(len(matrix)):
            if swapped:
                currentLeadingElementRowIndex += 1
                currentLeadingElementColIndex += 1

            #print(currentLeadingElementRowIndex, currentLeadingElementColIndex)
            
            if currentLeadingElementRowIndex >= len(matrix) or currentLeadingElementColIndex >= len(matrix[0]):
                break
            
            if matrix[currentLeadingElementRowIndex][currentLeadingElementColIndex] != 0:
                currentLeadingElementRowIndex += 1
                currentLeadingElementColIndex += 1
                continue

            for i in range(row + 1, len(matrix)):
                if matrix[i][currentLeadingElementColIndex] == 0:
                    swapped = False
                    continue

                cls.swapRow(matrix, row, i)
                swapped = True

                #print(matrix)

                break

    @classmethod
    def moveAllZeroRowsToBottom(cls, matrix):
        isAllZeros = False
        currentRowZeroCount = 0
        swapFromIndex = 0
        swapWithIndex = 0

        for row in range(len(matrix)):
            currentRowZeroCount = 0

            for col in range(len(matrix[0])):
                if matrix[row][col] == 0:
                    currentRowZeroCount += 1

            if currentRowZeroCount == len(matrix[0]):
                if not isAllZeros:
                    swapFromIndex = row

                isAllZeros = True
                swapFromIndex = row

                #print(f"All zero row: {row}")
            elif isAllZeros:
                swapWithIndex = row

                cls.swapRow(matrix, swapFromIndex, swapWithIndex)

                swapFromIndex += 1

        matrix.sort(key = lambda row: all(x == 0 for x  in row))

    @classmethod
    def rowEchelonForm(cls, matrix):
        matrix_copy = copy.deepcopy(matrix)

        cls.moveAllZeroRowsToBottom(matrix_copy)

        currentLeadingElementRowIndex = 0
        currentLeadingElementColIndex = 0

        isRowEchelonFormFinished = False

        for _ in range(len(matrix)):
            for currentRow in range(currentLeadingElementRowIndex + 1, len(matrix)):
                if currentLeadingElementColIndex == len(matrix[0]) or currentLeadingElementRowIndex == len(matrix) :
                    isRowEchelonFormFinished = True
                    break

                if matrix[currentLeadingElementRowIndex][currentLeadingElementColIndex] == 0:
                    cls.swapRow(matrix_copy, currentRow, len(matrix) - 1)

                if matrix_copy[currentLeadingElementRowIndex][currentLeadingElementColIndex] == 0:
                    continue

                multiplyByLeadingRow = -matrix_copy[currentRow][currentLeadingElementColIndex] / matrix_copy[currentLeadingElementRowIndex][currentLeadingElementColIndex]
                #print(multiplyByLeadingRow)

                for j in range(len(matrix_copy[0])):
                    matrix_copy[currentRow][j] += Fraction(multiplyByLeadingRow * matrix_copy[currentLeadingElementRowIndex][j]).limit_denominator()

            if isRowEchelonFormFinished:
                break

            currentLeadingElementRowIndex += 1
            currentLeadingElementColIndex += 1

        
        cls.setCorrectLeadingElementsRows(matrix_copy)
        
        return matrix_copy

matrix = [
    [1, 2],
    [2, 4]
]

A1 = [
    [1, 2],
    [2, 4]
]

A2 = [
    [1, 2, 3],
    [2, 5, 7],
    [3, 8, 10]
]

A3 = [
    [1, 2, 3, 4],
    [2, 4, 6, 8],
    [3, 5, 7, 9]
]

A4 = [
    [1, 2, 3],
    [2, 3, 5],
    [3, 4, 7],
    [4, 5, 9]
]

A5 = [
    [1, 2, 1, 3],
    [2, 5, 3, 7],
    [3, 7, 4, 10],
    [4, 9, 5, 13]
]

A6 = [
    [0,0,0],
    [1,2,3],
    [0,0,0],
    [0,0,5],
    [0,1,0],
    [0,0,0],
    [0,0,0],
    [0,0,0]
]

A7 = [
    [0,0,0,1],
    [0,0,1,0],
    [0,1,0,0],
    [0,0,0,0],
    [1,0,0,1]
]

A8 = [
    [2, 1, 3, 4],
    [1, 2, 1, 3],
    [3, 1, 2, 5],
    [1, 1, 1, 2]
]

A8sp = sp.Matrix([
    [2, 1, 3, 4],
    [1, 2, 1, 3],
    [3, 1, 2, 5],
    [1, 1, 1, 2]
])

MatrixModule.printMatrix(MatrixModule.rowEchelonForm(A7))

MatrixModule.setCorrectLeadingElementsRows(A6)
MatrixModule.printMatrix(A6)

MatrixModule.printMatrix(MatrixModule.rowEchelonForm(A8))

print(A8sp.echelon_form())