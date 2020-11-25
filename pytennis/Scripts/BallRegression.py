import numpy as np


class Network:
    def __init__(self, xmin, xmax, ymin, ymax):
        """
        xmin: 150,
        xmax: 450, 
        ymin: 100, 
        ymax: 600
        """

        self.StaticDiscipline = {
            'xmin': xmin,
            'xmax': xmax,
            'ymin': ymin,
            'ymax': ymax
        }

    def network(self, xsource, ysource=100, Ynew=600, divisor=50):  # ysource will always be 100
        """
        For Network A
        ysource: will always be 100
        xsource: will always be between xmin and xmax (static discipline)

        For Network B
        ysource: will always be 600
        xsource: will always be between xmin and xmax (static discipline)
        """

        while True:
            ListOfXsourceYSource = []
            Xnew = np.random.choice([i for i in range(
                self.StaticDiscipline['xmin'], self.StaticDiscipline['xmax'])], 1)
            #Ynew = np.random.choice([i for i in range(self.StaticDiscipline['ymin'], self.StaticDiscipline['ymax'])], 1)

            source = (xsource, ysource)
            target = (Xnew[0], Ynew)

            #Slope and intercept
            slope = (ysource - Ynew)/(xsource - Xnew[0])
            intercept = ysource - (slope*xsource)
            if (slope != np.inf) and (intercept != np.inf):
                break
            else:
                continue

        #print(source, target)
        # randomly select 50 new values along the slope between xsource and xnew (monotonically decreasing/increasing)
        XNewList = [xsource]

        if xsource < Xnew:
            differences = Xnew[0] - xsource
            increment = differences / divisor
            newXval = xsource
            for i in range(divisor):

                newXval += increment
                XNewList.append(int(newXval))
        else:
            differences = xsource - Xnew[0]
            decrement = differences / divisor
            newXval = xsource
            for i in range(divisor):

                newXval -= decrement
                XNewList.append(int(newXval))

        # determine the values of y, from the new values of x, using y= mx + c
        yNewList = []
        for i in XNewList:
            findy = (slope * i) + intercept  # y = mx + c
            yNewList.append(int(findy))

        ListOfXsourceYSource = [(x, y) for x, y in zip(XNewList, yNewList)]

        return XNewList, yNewList

    def DefaultToPosition(self, x1, x2=300, divisor=50):
        DefaultPositionA = 300
        DefaultPositionB = 300
        XNewList = []
        if x1 < x2:
            differences = x2 - x1
            increment = differences / divisor
            newXval = x1
            for i in range(divisor):
                newXval += increment
                XNewList.append(int(np.floor(newXval)))

        else:
            differences = x1 - x2
            decrement = differences / divisor
            newXval = x1
            for i in range(divisor):
                newXval -= decrement
                XNewList.append(int(np.floor(newXval)))
        return XNewList
