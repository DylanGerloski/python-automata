import matplotlib.pyplot as plt
import numpy as np

class Totalistic_CA_Grid:

    def __init__(self, height=200, width=400, initial_number_of_black_cell=1):
        self.height = height
        self.width = width
        self.initial_number_of_black_cell = initial_number_of_black_cell
        self.grid = None


    def __initialize(self,height, width, initial_number_of_black_cell):
        self.height = height
        self.width = width
        self.grid = None
        self.initial_number_of_black_cell = initial_number_of_black_cell

    def get_grid(self):

        if self.initial_number_of_black_cell==1:
            self.__single_black_cell_grid()
        else:
            self.__multiple_black_cell_grid()

        return self.grid

    def __single_black_cell_grid(self):

        """
        This function creates matrix in heightXwidth dimensions and
        assigns 1 to the middle cell in the top row of the matrix.

        :return:
        """
        self.grid = np.zeros((self.height, self.width), dtype=np.int32)
        self.grid[0, int(self.width / 2)] = 2




    def __multiple_black_cell_grid(self):

        """
        This function assigns a value of 1 to the desired
        number of cells of the top row of the heightXwitdth matrix.
        It ensures that the middle cell is 1.
        :return:
        """



        #Calling the function that assigns the value of the middle cell of the top row to 1.
        self.__single_black_cell_grid()

        """remove 1 from the self.initial_number_of_black_cell variable
        because the value has been assigned to the middle cell"""
        n=self.initial_number_of_black_cell-1
        for i in range(n):
            random_col = np.random.randint(0, self.width)
            self.grid[0, random_col] = 2


class Totalistic_CA(Totalistic_CA_Grid):

    def __init__(self,grid_apparence="normal",**kwargs):
        super().__init__(**kwargs)

        self.grid_apparence=grid_apparence

        self.rule=None

        self.rule_tenary=None

    def set_grid_parameters(self,
                            height,
                            width,
                            initial_number_of_black_cell=1,
                            grid_apparence="normal"):
        self.height = height
        self.width = width
        self.initial_number_of_black_cell = initial_number_of_black_cell

        self.grid = None
        self.grid_apparence=grid_apparence

    def __get_rule_tenary(self):
        length=7
        if self.rule==0:
            padding=length
        else:
            padding=length-len(np.base_repr(self.rule,base=3))

        self.rule_tenary = np.array([int(b) for b in np.base_repr(
            number=self.rule,
            base=3,
            padding=padding)], dtype=np.int8)


    def generate(self, rule):

        self.rule=rule
        self.get_grid()
        self.__get_rule_tenary()

        for i in range(self.height-1):
            self.grid[i+1,:]=self.step(self.grid[i,:])

        if self.grid_apparence=='normal':
            self.grid[self.grid==2]=255
            self.grid[self.grid==1]=128
            self.grid[self.grid==0]=0

        if self.grid_apparence=='wolfram':
            self.grid[self.grid==1]=128
            self.grid[self.grid==0]=255
            self.grid[self.grid==2]=0

        return self.grid


    def __get_neighborhood_matrix(self, center):
        #vector that holds the neighbors on the left by shifting the row vector to the right
        left=np.roll(center, 1)


        #vector that holds the neighbors on the rights by shifting the row vector to the left
        right=np.roll(center, -1)

        neighborhood_matrix=np.vstack((left, center, right)).astype(np.int8)

        return neighborhood_matrix

    def step(self, row):
        neighborhood_matrix=self.__get_neighborhood_matrix(center=row)

        rmts=np.sum(neighborhood_matrix, axis=0)
        #print("rmts",rmts)

        return self.rule_tenary[6-rmts].astype(np.int8)


totalistic_rules=[1599, 912, 2040, 2049, 1635, 1041]
for totalistic_rule in totalistic_rules:
    totalistic_ca=Totalistic_CA(grid_apparence="wolfram")
    ca_pattern=totalistic_ca.generate(totalistic_rule)
    plt.figure(figsize=(12,6))
    plt.imshow(ca_pattern,cmap="RdBu")
    plt.xticks([])
    plt.yticks([])
    plt.title("Totalistic CA Pattern for Code:{}".format(totalistic_rule))
    plt.show()