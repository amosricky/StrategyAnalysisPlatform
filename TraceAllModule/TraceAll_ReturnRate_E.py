import os
import pandas as pd


class TraceAll_ReturnRate_E:
    def __init__(self, WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month , Outsample_Length_Month ,
                 Initial_Capital , Plateau_Condition , TraceAll_Exist , TraceAll_ExistPass , TraceAll_Minimum , isOutputFile,
                 SelectedFunction,TheilsU , MAPE , WFE):

        self.WalkForward_DF = WalkForward_DF
        self.Total_Period = Total_Period
        self.Target_DirPath = Target_DirPath
        self.Insample_Length_Month = Insample_Length_Month
        self.Outsample_Length_Month = Outsample_Length_Month
        self.Initial_Capital = Initial_Capital
        self.Plateau_Condition = Plateau_Condition
        self.TraceAll_Exist = TraceAll_Exist
        self.TraceAll_ExistPass = TraceAll_ExistPass
        self.TraceAll_Minimum = TraceAll_Minimum
        self.isOutputFile = isOutputFile
        self.SelectedFunction = SelectedFunction
        self.TheilsU = TheilsU
        self.MAPE = MAPE
        self.WFE = WFE

    def TraceAll_ReturnRate_E_CalculatePass(self , InSampleNetAnnualAvgTrade , OutSampleNetAnnualAvgTrade):

        SelectedFunction = self.SelectedFunction
        TheilsU = self.TheilsU
        MAPE = self.MAPE
        WFE = self.WFE

        # 回傳是否通過Series與評估分數
        ParameterScore = 0
        isWindowPass = 0

        if (SelectedFunction == 'MAPE'):
            ParameterScore = abs((OutSampleNetAnnualAvgTrade - InSampleNetAnnualAvgTrade) / OutSampleNetAnnualAvgTrade)
            isWindowPass = (ParameterScore <= MAPE)

        elif (SelectedFunction == 'TheilsU'):
            ParameterScore = abs(OutSampleNetAnnualAvgTrade - InSampleNetAnnualAvgTrade) / (abs(InSampleNetAnnualAvgTrade) + abs(OutSampleNetAnnualAvgTrade))
            isWindowPass = (ParameterScore <= TheilsU)

        elif (SelectedFunction == 'WFE'):
            ParameterScore = (OutSampleNetAnnualAvgTrade / InSampleNetAnnualAvgTrade)
            isWindowPass = (ParameterScore >= WFE)

        return ParameterScore, isWindowPass

    def Analysis(self):

        WalkForward_DF = self.WalkForward_DF
        Total_Period = self.Total_Period
        Insample_Length_Month = self.Insample_Length_Month
        Outsample_Length_Month = self.Outsample_Length_Month
        Initial_Capital = self.Initial_Capital
        Plateau_Condition = self.Plateau_Condition
        TraceAll_Exist = self.TraceAll_Exist
        TraceAll_ExistPass = self.TraceAll_ExistPass
        TraceAll_Minimum = self.TraceAll_Minimum

        # 建立統計表格
        Table = pd.DataFrame()

        for Period in range(1, Total_Period + 1):

            # 判斷年化報酬率是否通過門檻
            isOverCondition = (WalkForward_DF["Training_" + str(Period)]["NetProfit_Percent"] / Insample_Length_Month * 12) >= Plateau_Condition

            # 起碼InSample有一點過門檻，進入尋找
            if (len(isOverCondition[isOverCondition == True]) > 0):

                # 符合條件的參數組為推薦參數
                Para = WalkForward_DF["Training_" + str(Period)].loc[isOverCondition]["Filename"]
                Para.name = 'Para' + str(Period)

                # 符合條件的參數組的InSample年化報酬率與每筆trade平均年化報酬率
                InSamepleNet_Numerator = WalkForward_DF["Training_" + str(Period)].loc[isOverCondition]["NetProfit"]
                InSamepleNet_Denominator = WalkForward_DF["Training_" + str(Period)].loc[isOverCondition]["Start_NetProfit"] + Initial_Capital
                InSamepleNet = (InSamepleNet_Numerator / InSamepleNet_Denominator)
                InSamepleNet.name = 'InSample' + str(Period) + '_RateOfReturn'
                InSampleTrade = WalkForward_DF["Training_" + str(Period)].loc[isOverCondition]["Number_of_Transactions"]
                InSampleNetAvgTrade = InSamepleNet / InSampleTrade
                InSampleNetAvgTrade.name = 'InSample' + str(Period) + '_AvgTrade'

                # 符合條件的參數組的OutSample年化報酬率與每筆trade平均年化報酬率
                OutSampleNet_Numerator = WalkForward_DF["Testing_" + str(Period)].loc[isOverCondition]["NetProfit"]
                OutSampleNet_Denominator = WalkForward_DF["Testing_" + str(Period)].loc[isOverCondition]["Start_NetProfit"] + Initial_Capital
                OutSampleNet = (OutSampleNet_Numerator / OutSampleNet_Denominator)
                OutSampleNet.name = 'OutSample' + str(Period) + '_RateOfReturn'
                OutSampleTrade = WalkForward_DF["Testing_" + str(Period)].loc[isOverCondition]["Number_of_Transactions"]
                OutSampleNetAvgTrade = OutSampleNet / OutSampleTrade
                OutSampleNetAvgTrade.name = 'OutSample' + str(Period) + '_AvgTrade'

                # 判斷該窗期是否合格
                Score, Pass = self.TraceAll_ReturnRate_E_CalculatePass(InSampleNetAvgTrade, OutSampleNetAvgTrade)
                Score.name = 'Score_' + str(Period)
                Pass.name = 'Pass' + str(Period)
                Pass.replace(True, 'Yes', inplace=True)
                Pass.replace(False, 'No', inplace=True)

                # 合併以上DataFrame
                Table = pd.concat([Table, Para], axis=1)
                Table = pd.concat([Table, InSamepleNet], axis=1)
                Table = pd.concat([Table, OutSampleNet], axis=1)
                Table = pd.concat([Table, InSampleTrade], axis=1)
                Table = pd.concat([Table, OutSampleTrade], axis=1)
                Table = pd.concat([Table, InSampleNetAvgTrade], axis=1)
                Table = pd.concat([Table, OutSampleNetAvgTrade], axis=1)
                Table = pd.concat([Table, Score], axis=1)
                Table = pd.concat([Table, Pass], axis=1)

                # 該InSample窗期沒有過門檻的參數組
            elif (len(isOverCondition[isOverCondition == True]) <= 0):
                Para = pd.Series(['No Plateau'])
                Para.name = 'Para' + str(Period)
                Pass = pd.Series(['No'])
                Pass.name = 'Pass' + str(Period)
                Table = pd.concat([Table, Para], axis=1)
                Table = pd.concat([Table, Pass], axis=1)


        # 統計所有參數組結果
        # 原始全部參數組
        Statitic = pd.DataFrame()
        AllPara = WalkForward_DF["Training_1"]["Filename"]
        AllPara.name = 'AllPara'
        Statitic = pd.concat([Statitic, AllPara], axis=1)

        # 全部窗期高點Concat
        for Period in range(1, Total_Period + 1):
            isExist = AllPara.isin(Table['Para' + str(Period)])
            isExist = pd.DataFrame({'isExist' + str(Period): isExist})
            isExist.replace(True, 'Y', inplace=True)
            isExist.replace(False, 'N', inplace=True)
            Statitic = pd.concat([Statitic, isExist], axis=1)

            if (Table['Para' + str(Period)][0] == 'No Plateau'):
                pass
            else:
                ThisPeriodFrame = pd.DataFrame({'AllPara': Table['Para' + str(Period)], 'Pass' + str(Period): Table['Pass' + str(Period)],'Score_' + str(Period): Table['Score_' + str(Period)]})
                ThisPeriodFrame = ThisPeriodFrame.dropna()
                Statitic = pd.merge(Statitic, ThisPeriodFrame, on=['AllPara'], how='left')

        # 整理好後Count
        Statitic['CountExist'] = (Statitic == 'Y').sum(axis=1)
        Statitic['CountPass'] = (Statitic == 'Yes').sum(axis=1)
        Statitic['TotalExistPercent'] = Statitic['CountExist'] / Total_Period
        Statitic['ExistPassPercent'] = Statitic['CountPass'] / Statitic['CountExist']

        self.OutputFile(Table, Statitic)
        Result = self.AnalysisResult(Statitic)

        return Result

    def OutputFile(self, Table, Statitic):

        Target_DirPath = self.Target_DirPath
        isOutputFile = self.isOutputFile

        if (isOutputFile == True):
            if (not (os.path.exists(Target_DirPath))):
                os.makedirs(Target_DirPath)
            # Table.to_csv(Target_DirPath + '//TraceAll_報酬率E_各窗格結果.csv', mode='a', header=True, index=False)
            Statitic.to_csv(Target_DirPath + '//TraceAll_報酬率E_整體結果.csv', mode='a', header=True, index=False)

        return 0

    def AnalysisResult(self, Statitic):

        TraceAll_Exist = self.TraceAll_Exist
        TraceAll_ExistPass = self.TraceAll_ExistPass
        TraceAll_Minimum = self.TraceAll_Minimum

        Result = False

        # 是否通過測驗
        PassAmount = len(Statitic[(Statitic['TotalExistPercent'] >= TraceAll_Exist) & (Statitic['ExistPassPercent'] >= TraceAll_ExistPass)])
        if (PassAmount >= TraceAll_Minimum):
            Result = True

        return Result