
# status enum:
# 0 is empty
# 1 is obstacle
# 2 is one block around obstacle


class cell:
    def __init__(self,x_coordinate,y_coordinate,status):
        self.x_coordinate=x_coordinate
        self.y_coordinate=y_coordinate
        self.status=status

    def occupy_cell(self):
        self.status=1

    def restricted_cell(self):
        self.status=2

    def getstatus(self):
        return self.status

    def setstatus(self,status):
        self.status=status