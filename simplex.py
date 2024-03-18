class SimplexSolver():
    def __init__(self, A, b, c) -> None:
        self.A = A
        self.b = b
        self.c = c
        self.num_constraints = len(A)
        self.num_variables = len(A[0])

        self.tableau = self.get_tableau()

    def get_tableau(self):
        tableau = []

        # append constraints
        for i in range(self.num_constraints):
            curr_row = self.A[i] + [0] * i + [1] + [0] * (self.num_constraints-i-1) + [0] + [self.b[i]]
            tableau.append(curr_row)

        # append objective function
        tableau.append([-x for x in self.c] + [0] * self.num_constraints + [1, 0])
        
        return tableau
    
    def find_pivot_col(self):
        res = [None, 0]
        for i, val in enumerate(self.tableau[-1]):
            if val < res[1]:
                res[1] = val
                res[0] = i
        return res[0]

    def find_pivot_row(self, pivot_col):
        res = [0, float('inf')]
        for i in range(self.num_constraints):
            curr_val = self.tableau[i][-1] / self.tableau[i][pivot_col]
            if curr_val < res[1]:
                res[1] = curr_val
                res[0] = i
        return res[0]
    
    def update_pivot_row(self, pivot_row, pivot_element):
        for i in range(self.num_variables + self.num_constraints + 2):
            self.tableau[pivot_row][i] *= 1/pivot_element
        
    def update_other_rows(self, pivot_row, pivot_col):
        for i in range(self.num_constraints + 1):
            if i == pivot_row:
                continue
            ratio = self.tableau[i][pivot_col]
            for j in range(self.num_variables + self.num_constraints + 2):
                self.tableau[i][j] -= ratio * self.tableau[pivot_row][j]

    def solve(self):
        while True:
            pivot_col = self.find_pivot_col()
            if pivot_col is None:
                break
            pivot_row = self.find_pivot_row(pivot_col)
            pivot_element = self.tableau[pivot_row][pivot_col]
            self.update_pivot_row(pivot_row, pivot_element)
            self.update_other_rows(pivot_row, pivot_col)
        
        return self.tableau[-1][-1]

A = [[1, 3, 2], [1, 5, 1]]
b = [10, 8]
c = [8, 10, 7]
ss = SimplexSolver(A, b, c)
res = ss.solve()
print(res)
