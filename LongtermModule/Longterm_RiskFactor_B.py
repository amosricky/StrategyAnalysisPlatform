import os
import math
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from LongtermModule import LongtermFunction


class Longterm_RiskFactor_B:
    def __init__(self, All_File_Data , Target_Path , Total_Period , Start_Day , End_Day, Insample_Length_Month , Outsample_Length_Month ,
                 Initial_Capital , Plateau_Condition , Longterm_Period , Longterm_Minimum , NetProfit_MDD_Score):

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
        self.NetProfit_MDD_Score = NetProfit_MDD_Score

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
        NetProfit_MDD_Score = self.NetProfit_MDD_Score

        RiskFactorB_LongtermFunction = LongtermFunction.LongtermFunction(Target_Path, Start_Day, End_Day, Insample_Length_Month, Outsample_Length_Month)

        # 回傳結果參數
        Result = False

        # 最少要要執行到第幾期
        LastPeriod = math.ceil((1 - Longterm_Period) * Total_Period)

        # 每期開始回測之通過紀錄
        TotalWindowPass = []

        #由不同窗格開始檢驗
        for i in range(1, LastPeriod + 1):

            StartDay = datetime.datetime.strptime(Start_Day, '%Y-%m-%d').date()
            StartDay += relativedelta(months=+(Outsample_Length_Month * (i - 1)))
            SamplePeriod = RiskFactorB_LongtermFunction.CutTime(str(StartDay), End_Day)

            # 紀錄該次回測每次結果
            WindowPass = []

            for j in range(0, len(SamplePeriod)):

                Training_Window_Start = RiskFactorB_LongtermFunction.StartDayChange(SamplePeriod[j][0][0])
                Training_Window_End = RiskFactorB_LongtermFunction.EndDayChange(SamplePeriod[j][0][1])
                Training_Window_Length = SamplePeriod[j][0][2]
                Testing_Window_Start_Day = RiskFactorB_LongtermFunction.StartDayChange(SamplePeriod[j][1][0])
                Testing_Window_End_Day = RiskFactorB_LongtermFunction.EndDayChange(SamplePeriod[j][1][1])

                CountPass = 0

                for Filename in os.listdir(Target_Path):
                    if (Training_Window_Start == 0):
                        InSampleNumerator = All_File_Data[Filename]['NetProfit'][Training_Window_End] - All_File_Data[Filename]['NetProfit'][Training_Window_Start]
                        InSampleDenominator = All_File_Data[Filename]['NetProfit'][Training_Window_Start] + Initial_Capital
                        InSampleAvgNet = (InSampleNumerator / InSampleDenominator) / Training_Window_Length * 12
                        WindowNet = All_File_Data[Filename]['NetProfit'][Testing_Window_End_Day] - All_File_Data[Filename]['NetProfit'][Training_Window_Start]

                    else:
                        InSampleNumerator = All_File_Data[Filename]['NetProfit'][Training_Window_End] - All_File_Data[Filename]['NetProfit'][Training_Window_Start - 1]
                        InSampleDenominator = All_File_Data[Filename]['NetProfit'][Training_Window_Start - 1] + Initial_Capital
                        InSampleAvgNet = (InSampleNumerator / InSampleDenominator) / Training_Window_Length * 12
                        WindowNet = All_File_Data[Filename]['NetProfit'][Testing_Window_End_Day] - All_File_Data[Filename]['NetProfit'][Training_Window_Start - 1]

                    if(InSampleAvgNet>=Plateau_Condition):

                        # 累積淨利、MaxNetsentNet用來輔助MDD計算
                        WindowMDD = 0
                        WindowPresentNet = 0
                        WindowMaxNet = 0

                        Window = All_File_Data[Filename].loc[Training_Window_Start:Testing_Window_End_Day]
                        Net_Shifted = All_File_Data[Filename]['NetProfit'].copy().shift().loc[Training_Window_Start:Testing_Window_End_Day]
                        Window = Window.assign(Net_Shifted=Net_Shifted.values)

                        for row in Window.itertuples():
                            if (math.isnan(row.Net_Shifted)):
                                pass
                            else:
                                GrossValue = row.NetProfit - row.Net_Shifted
                                WindowPresentNet += GrossValue

                                if (WindowPresentNet > WindowMaxNet):
                                    WindowMaxNet = WindowPresentNet
                                if ((WindowPresentNet - WindowMaxNet) < WindowMDD):
                                    WindowMDD = (WindowPresentNet - WindowMaxNet)

                        #若獲利因子大於門檻
                        if((WindowNet/abs(WindowMDD))>=NetProfit_MDD_Score):
                            CountPass += 1

                #若該次窗期回測通過長期追蹤最小門檻
                if(CountPass>=Longterm_Minimum):
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
