import os
import math
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from LongtermModule import LongtermFunction


class Longterm_ReturnRate_D:
    def __init__(self, All_File_Data , Target_Path , Total_Period , Start_Day , End_Day, Insample_Length_Month , Outsample_Length_Month ,
                 Initial_Capital , Plateau_Condition , Longterm_Period , Longterm_Minimum):

        self.All_File_Data = All_File_Data
        self.Target_Path = Target_Path
        self.Total_Period = Total_Period
        self.Start_Day = Start_Day
        self.End_Day = End_Day
        self.Insample_Length_Month = Insample_Length_Month
        self.Outsample_Length_Month = Outsample_Length_Month
        self.Initial_Capital = Initial_Capital
        self.Plateau_Condition = Plateau_Condition
        self.Longterm_Period = Longterm_Period
        self.Longterm_Minimum = Longterm_Minimum

    def Analysis(self):

        All_File_Data = self.All_File_Data
        Target_Path = self.Target_Path
        Total_Period = self.Total_Period
        Start_Day = self.Start_Day
        End_Day = self.End_Day
        Insample_Length_Month = self.Insample_Length_Month
        Outsample_Length_Month = self.Outsample_Length_Month
        Initial_Capital = self.Initial_Capital
        Plateau_Condition = self.Plateau_Condition
        Longterm_Period = self.Longterm_Period
        Longterm_Minimum = self.Longterm_Minimum

        ReturnRateD_LongtermFunction = LongtermFunction.LongtermFunction(Target_Path, Start_Day, End_Day, Insample_Length_Month, Outsample_Length_Month)

        # 回傳結果參數
        Result = False

        # 最少要要執行到第幾期
        LastPeriod = math.ceil((1 - Longterm_Period) * Total_Period)

        #每期開始回測之通過紀錄
        TotalWindowPass = []

        for i in range(1, LastPeriod + 1):

            StartDay = datetime.datetime.strptime(Start_Day, '%Y-%m-%d').date()
            StartDay += relativedelta(months=+(Outsample_Length_Month * (i - 1)))
            SamplePeriod = ReturnRateD_LongtermFunction.CutTime(str(StartDay), End_Day)

            #紀錄該次回測每次結果
            WindowPass = []

            for j in range(0, len(SamplePeriod)):

                Training_Window_Start = ReturnRateD_LongtermFunction.StartDayChange(SamplePeriod[j][0][0])
                Training_Window_End = ReturnRateD_LongtermFunction.EndDayChange(SamplePeriod[j][0][1])
                Training_Window_Length = SamplePeriod[j][0][2]
                Testing_Window_Start_Day = ReturnRateD_LongtermFunction.StartDayChange(SamplePeriod[j][1][0])
                Testing_Window_End_Day = ReturnRateD_LongtermFunction.EndDayChange(SamplePeriod[j][1][1])
                Testing_Window_Length = SamplePeriod[j][1][2]

                # 紀錄InSample推薦參數
                InSamplePassPara = []
                #記錄推薦參數於樣本外又滿足推薦參數報酬
                PassParainOutSample = []

                #抓出該其窗格樣本內通過門檻之參數組
                for Filename in os.listdir(Target_Path):
                    if (Training_Window_Start == 0):
                        InSampleNumerator = All_File_Data[Filename]['NetProfit'][Training_Window_End] - All_File_Data[Filename]['NetProfit'][Training_Window_Start]
                        InSampleDenominator = All_File_Data[Filename]['NetProfit'][Training_Window_Start] + Initial_Capital
                        InSampleAvgNet = (InSampleNumerator / InSampleDenominator) / Training_Window_Length * 12

                    else:
                        InSampleNumerator = All_File_Data[Filename]['NetProfit'][Training_Window_End] - All_File_Data[Filename]['NetProfit'][Training_Window_Start - 1]
                        InSampleDenominator = All_File_Data[Filename]['NetProfit'][Training_Window_Start - 1] + Initial_Capital
                        InSampleAvgNet = (InSampleNumerator / InSampleDenominator) / Training_Window_Length * 12

                    if (InSampleAvgNet >= Plateau_Condition):
                        InSamplePassPara.append(Filename)

                #看推薦參數於樣本外是否仍符合
                for Para in InSamplePassPara:
                    OutSampleNumerator = All_File_Data[Para]['NetProfit'][Testing_Window_End_Day] - All_File_Data[Para]['NetProfit'][Testing_Window_Start_Day - 1]
                    OutSampleDenominator = All_File_Data[Para]['NetProfit'][Testing_Window_Start_Day - 1] + Initial_Capital
                    OutSampleAvgNet = (OutSampleNumerator / OutSampleDenominator) / Testing_Window_Length * 12

                    if (OutSampleAvgNet >= Plateau_Condition):
                        PassParainOutSample.append(Para)

                if((len(InSamplePassPara)>=Longterm_Minimum) and (len(PassParainOutSample)>=Longterm_Minimum)):
                    if((len(PassParainOutSample)/len(InSamplePassPara)>=0.5)):
                        WindowPass.append(True)
                else:
                    WindowPass.append(False)
                    break

            TotalWindowPass.append(WindowPass)

        # 判斷是否合格
        # 最少須通過幾期回測，利用math.ceil(Longterm_Period*Total_Period)之值來當次數
        for i in range(0, len(TotalWindowPass)):
            CountTrue = 0
            for j in range(0, len(TotalWindowPass[i])):
                if (TotalWindowPass[i][j] == True):
                    CountTrue += 1
            if (CountTrue >= math.ceil(Longterm_Period * Total_Period)):
                Result = True

        return Result


