import os
import pandas as pd


class TraceAll_ReturnRate_D:
    def __init__(self, WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month , Outsample_Length_Month ,
                 Initial_Capital , Plateau_Condition , TraceAll_Exist , TraceAll_ExistPass , TraceAll_Minimum , isOutputFile):

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

        # 建立表格  統計各窗格過門檻參數組分析結果
        Table = pd.DataFrame()

        for Period in range(1, Total_Period + 1):

            # 判斷年化報酬率是否通過門檻
            isOverCondition = (WalkForward_DF["Training_" + str(Period)]["NetProfit_Percent"] / Insample_Length_Month * 12) >= Plateau_Condition

            # 起碼InSample有一點過門檻，進入尋找
            if (len(isOverCondition[isOverCondition == True]) > 0):

                # 符合條件的參數組為推薦參數
                Para = WalkForward_DF["Training_" + str(Period)].loc[isOverCondition]["Filename"]
                Para.name = 'Para' + str(Period)

                # 符合條件的參數組的InSample年化報酬率
                InSamepleNet_Numerator = WalkForward_DF["Training_" + str(Period)].loc[isOverCondition]["NetProfit"]
                InSamepleNet_Denominator = WalkForward_DF["Training_" + str(Period)].loc[isOverCondition]["Start_NetProfit"] + Initial_Capital
                InSamepleNet = (InSamepleNet_Numerator / InSamepleNet_Denominator) / Insample_Length_Month * 12
                InSamepleNet.name = 'InSample' + str(Period) + '_Annual_RateOfReturn'

                # 符合條件的參數組的OutSample年化報酬率
                OutSampleNet_Numerator = WalkForward_DF["Testing_" + str(Period)].loc[isOverCondition]["NetProfit"]
                OutSampleNet_Denominator = WalkForward_DF["Testing_" + str(Period)].loc[isOverCondition]["Start_NetProfit"] + Initial_Capital
                OutSampleNet = (OutSampleNet_Numerator / OutSampleNet_Denominator) / Outsample_Length_Month * 12
                OutSampleNet.name = 'OutSample' + str(Period) + '_Annual_RateOfReturn'

                #判斷該窗格是否合格
                InSamplePassAmount = len(InSamepleNet)
                OutSamplePass = OutSampleNet > Plateau_Condition
                OutSamplePassAmount = len(OutSamplePass[OutSamplePass == True])
                Pass = (((OutSamplePassAmount / InSamplePassAmount) >= 0.5)  and (OutSamplePassAmount>=TraceAll_Minimum))
                Pass = pd.Series([Pass])
                Pass.name = 'Pass' + str(Period)
                Pass.replace(True, 'Yes', inplace=True)
                Pass.replace(False, 'No', inplace=True)

                # 合併以上DataFrame
                Table = pd.concat([Table, Para], axis=1)
                Table = pd.concat([Table, InSamepleNet], axis=1)
                Table = pd.concat([Table, OutSampleNet], axis=1)
                Table = pd.concat([Table, Pass], axis=1)

            # 該InSample窗期沒有過門檻的參數組
            elif (len(isOverCondition[isOverCondition == True]) <= 0):
                Para = pd.Series(['No Plateau'])
                Para.name = 'Para' + str(Period)
                Pass = pd.Series(['No'])
                Pass.name = 'Pass' + str(Period)
                Table = pd.concat([Table, Para], axis=1)
                Table = pd.concat([Table, Pass], axis=1)

        self.OutputFile(Table)
        WindowResult = self.AnalysisResult(Table)

        return WindowResult

    def OutputFile(self, Table):

        Target_DirPath = self.Target_DirPath
        isOutputFile = self.isOutputFile

        if (isOutputFile == True):
            if (not (os.path.exists(Target_DirPath))):
                os.makedirs(Target_DirPath)
            Table.to_csv(Target_DirPath + '//TraceAll_報酬率D_各窗格結果.csv', mode='a', header=True, index=False)

        return 0

    def AnalysisResult(self, Table):

        Total_Period = self.Total_Period
        TraceAll_Exist = self.TraceAll_Exist

        Result = False

        # 是否通過測驗
        PassAmount = 0
        for Period in range(1, Total_Period + 1):
            # print(Table['Pass' + str(Period)][0])
            if (Table['Pass' + str(Period)][0] == 'Yes'):
                PassAmount += 1

        if ((PassAmount / Total_Period) >= TraceAll_Exist):
            Result = True

        return Result