import os
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta

class LongtermFunction:
    def __init__(self, Target_Path , Start_Day , End_Day , Insample_Length_Month , Outsample_Length_Month):

        self.Target_Path = Target_Path
        self.Start_Day = Start_Day
        self.End_Day = End_Day
        self.Insample_Length_Month = Insample_Length_Month
        self.Outsample_Length_Month = Outsample_Length_Month

    def CutTime(self, Start_Day, End_Day):

        Insample_Length_Month = self.Insample_Length_Month
        Outsample_Length_Month = self.Outsample_Length_Month
        All = []

        # datetime
        Start_Day = datetime.datetime.strptime(Start_Day, '%Y-%m-%d').date()
        End_Day = datetime.datetime.strptime(End_Day, '%Y-%m-%d').date()

        # 初始 InSample Time
        InSampleStart = Start_Day
        InSampleEnd = InSampleStart
        InSampleEnd += relativedelta(months=+Insample_Length_Month, days=-1)
        InSampleStartNum = 1
        InSampleEndNum = Insample_Length_Month

        OutSampleStart = InSampleEnd
        OutSampleStart += relativedelta(days=1)
        OutSampleEnd = OutSampleStart
        OutSampleEnd += relativedelta(months=+(Outsample_Length_Month), days=-1)
        OutSampleStartNum = InSampleEndNum + 1
        OutSampleEndNum = InSampleEndNum + Outsample_Length_Month

        while (True):

            InSamplePeriod = []
            OutSamplePeriod = []
            InSampleAddMonth = round((Insample_Length_Month/(Insample_Length_Month+Outsample_Length_Month))*Outsample_Length_Month)
            OutSampleAddMonth = Outsample_Length_Month-InSampleAddMonth

            if (OutSampleEnd >= End_Day):
                diffDay = int((OutSampleEnd - End_Day).days)
                OutSampleEndNum -= (round(diffDay / 30.4))

                InSamplePeriod.append(str(InSampleStart))
                InSamplePeriod.append(str(InSampleEnd))
                InSamplePeriod.append(InSampleEndNum - InSampleStartNum + 1)

                OutSamplePeriod.append(str(OutSampleStart))
                OutSamplePeriod.append(str(End_Day))
                OutSamplePeriod.append(OutSampleEndNum - OutSampleStartNum + 1)

                Temp = [InSamplePeriod, OutSamplePeriod]
                All.append(Temp)
                break

            else:
                InSamplePeriod.append(str(InSampleStart))
                InSamplePeriod.append(str(InSampleEnd))
                InSamplePeriod.append(InSampleEndNum - InSampleStartNum + 1)

                OutSamplePeriod.append(str(OutSampleStart))
                OutSamplePeriod.append(str(OutSampleEnd))
                OutSamplePeriod.append(OutSampleEndNum - OutSampleStartNum + 1)

                Temp = [InSamplePeriod, OutSamplePeriod]
                All.append(Temp)

                InSampleEnd += relativedelta(months=+InSampleAddMonth)
                InSampleEndNum += InSampleAddMonth
                OutSampleStart += relativedelta(months=+InSampleAddMonth)
                OutSampleStartNum += InSampleAddMonth
                OutSampleEnd += relativedelta(months=+(Outsample_Length_Month))
                OutSampleEndNum += (Outsample_Length_Month)

        return All

    def StartDayChange(self, Window_Start_Day):

        Target_Path = self.Target_Path
        Day = datetime.datetime.strptime(Window_Start_Day, '%Y-%m-%d').date()
        File = pd.read_csv(os.path.join(Target_Path, os.listdir(Target_Path)[0]), engine='python')
        File['Day'] = pd.to_datetime(File['Day'], format='%Y/%m/%d')
        if (len(File[File['Day'] == Day]) == 1):
            index = File[File['Day'] == Day].index.tolist()[0]
        else:
            Day += relativedelta(days=1)
            return self.StartDayChange(str(Day))
        return index

    def EndDayChange(self, Window_End_Day):
        Target_Path = self.Target_Path
        Day = datetime.datetime.strptime(Window_End_Day, '%Y-%m-%d').date()
        File = pd.read_csv(os.path.join(Target_Path, os.listdir(Target_Path)[0]), engine='python')
        File['Day'] = pd.to_datetime(File['Day'], format='%Y/%m/%d')
        if (len(File[File['Day'] == Day]) == 1):
            index = File[File['Day'] == Day].index.tolist()[0]
        else:
            Day -= relativedelta(days=1)
            return self.EndDayChange(str(Day))
        return index