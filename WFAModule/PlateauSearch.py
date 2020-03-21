import pandas as pd
import sys
import math
sys.setrecursionlimit(10000000)

class PlateauSearch:
    def __init__(self, ParaSeries , Plateau_Amount):

        self.ParaSeries = ParaSeries
        self.Plateau_Amount = Plateau_Amount

        #回傳結果
        self.Result = False

    def ConvertToList(self):

        ParaSeries = self.ParaSeries
        StartPoint = [[20,20],[0.75,0.25],[50,25],[4,2]]

        #回傳List ， 共有3種分類
        ParaList1 = []
        ParaList2 = []
        ParaList3 = []

        for i in range (0,len(ParaSeries)):
            Para = ParaSeries.iloc[i]
            Para = Para.split('_')
            Temp = []

            Class = int(Para[0])
            CoordinatePoint1 = (float(Para[1]) - StartPoint[0][0])/StartPoint[0][1]
            CoordinatePoint2 = (float(Para[2]) - StartPoint[1][0])/StartPoint[1][1]
            CoordinatePoint3 = (float(Para[3]) - StartPoint[2][0])/StartPoint[2][1]
            CoordinatePoint4 = (float(Para[4].split('.')[0]) - StartPoint[3][0])/StartPoint[3][1]
            Coordinate = [Class , CoordinatePoint1 , CoordinatePoint2 , CoordinatePoint3 , CoordinatePoint4]

            Temp.append(Coordinate)
            Temp.append(ParaSeries.iloc[i])

            if(Class == 1):
                ParaList1.append(Temp)
            elif(Class == 2):
                ParaList2.append(Temp)
            elif(Class == 3):
                ParaList3.append(Temp)

        return ParaList1 , ParaList2 ,ParaList3

    def StartSearch(self):

        Plateau_Amount = self.Plateau_Amount
        ParaList1, ParaList2, ParaList3 = self.ConvertToList()
        Result = self.Result

        if (len(ParaList1) >= Plateau_Amount):
            Class1 = self.PlateauAssign(ParaList1)
            if(max(Class1)>=Plateau_Amount):
                Result = True

        if (len(ParaList2) >= Plateau_Amount):
            Class2 = self.PlateauAssign(ParaList2)
            if (max(Class2) >= Plateau_Amount):
                Result = True

        if (len(ParaList3) >= Plateau_Amount):
            Class3 = self.PlateauAssign(ParaList3)
            if (max(Class3) >= Plateau_Amount):
                Result = True

        return Result


    def PlateauAssign(self , ParaList):

        Plateau_Amount = self.Plateau_Amount
        ThisClassPlateauAmount = []

        for i in range(0 , len(ParaList)):

            StartPoint = ParaList[i]
            SearchBucket = ParaList.copy()
            SearchBucket[i] = True
            PlateauBucket = []
            PlateauBucket.append(StartPoint)
            Amount = self.PlateauSearch(StartPoint , SearchBucket , PlateauBucket)
            ThisClassPlateauAmount.append(Amount)
            if(Amount>=Plateau_Amount):
                break

        return ThisClassPlateauAmount

    def PlateauSearch(self , StartPoint , SearchBucket , PlateauBucket):

        for i in range(0 , len(SearchBucket)):
            if(SearchBucket[i] != True):
                Distance1 = (float(StartPoint[0][1]) - float(SearchBucket[i][0][1]))**2
                Distance2 = (float(StartPoint[0][2]) - float(SearchBucket[i][0][2]))**2
                Distance3 = (float(StartPoint[0][3]) - float(SearchBucket[i][0][3]))**2
                Distance4 = (float(StartPoint[0][4]) - float(SearchBucket[i][0][4]))**2
                Distance = math.sqrt(Distance1+Distance2+Distance3+Distance4)
                if(Distance==1):
                    if (SearchBucket[i] not in PlateauBucket):
                        NewStartPoint = SearchBucket[i]
                        PlateauBucket.append(SearchBucket[i])
                        SearchBucket[i] = True
                        # if(len(PlateauBucket)>Plateau_Amount):
                        #     # print(len(PlateauBucket))
                        #     break
                        self.PlateauSearch(NewStartPoint , SearchBucket , PlateauBucket)
                    else:
                        SearchBucket[i] = True
        return len(PlateauBucket)