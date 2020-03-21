import os , time , csv
import pandas as pd
import numpy as np
from MultipleBackTestParameter2 import *
from SystemParameter import *
from WalkForwardModule import CreateWalkForwardDataFrame
from TraceAllModule import CallTraceAll
from WFAModule import CallWFA
from LongtermModule import CallLongterm

def OutputFile(TraceAll_Result, WFA_WFResult, WFA_PlateauResult, Longterm_Result , Target_DirPath):

    # 建立分析結果表格
    AnalysisResult = pd.DataFrame()
    TraceAll_Result = pd.Series(TraceAll_Result)
    WFA_WFResult = pd.Series(WFA_WFResult)
    WFA_PlateauResult = pd.Series(WFA_PlateauResult)
    Longterm_Result = pd.Series(Longterm_Result)
    TraceAll_Result.name = 'TraceAll'
    WFA_WFResult.name = 'WFA'
    WFA_PlateauResult.name = 'WFA_Plateau'
    Longterm_Result.name = 'Longterm'
    AnalysisResult = pd.concat([AnalysisResult, TraceAll_Result], axis=1)
    AnalysisResult = pd.concat([AnalysisResult, WFA_WFResult], axis=1)
    AnalysisResult = pd.concat([AnalysisResult, WFA_PlateauResult], axis=1)
    AnalysisResult = pd.concat([AnalysisResult, Longterm_Result], axis=1)

    # 輸出
    if (isOutputFile == True):
        if (not (os.path.exists(Target_DirPath))):
            os.makedirs(Target_DirPath)
        AnalysisResult.to_csv(Target_DirPath + '//分析結果.csv', mode='a', header=True, index=False)

    return 0


print("計算開始時間 : " + time.strftime("%H:%M:%S"))
for thisPeriod in Period:

    #建立該窗格大小結果表格
    TraceAll_Result_Table = []
    WFA_Result_Table = []
    Longterm_Result_Table = []

    for thisPassPercent in PassPercent:

        TraceAll_Result_PassPercentTable = []
        WFA_Result_PassPercentTable = []
        Longterm_Result_PassPercentTable = []

        for thisTarget in TargetList:

            thisTarget_TraceAll_Result = []
            thisTarget_WFA_Result = []
            thisTarget_Longterm_Result = []

            for thisPassMinimum in PassMinimum:
                print(thisPeriod , thisPassPercent , thisPassMinimum , thisTarget)

                #設置變動參數
                Target = thisTarget
                Insample_Length_Month = thisPeriod
                Outsample_Length_Month = thisPeriod
                TraceAll_Exist = thisPassPercent
                TraceAll_ExistPass = thisPassPercent
                TraceAll_Minimum = thisPassMinimum
                WalkForward_PassWindow = thisPassPercent
                WalkForward_Minimum = thisPassMinimum
                Longterm_Period = thisPassPercent
                Longterm_Minimum = thisPassMinimum

                WalkForward = CreateWalkForwardDataFrame.WalkForwardDataFrame(Strategy , thisTarget , Start_Day , End_Day , thisPeriod , thisPeriod , Initial_Capital)
                WalkForward_DF, Total_Period = WalkForward.CreateDataFrame()
                Target_DirPath = WalkForward.CreateOutputDir(thisPassPercent , thisPassMinimum)

                TraceAll = CallTraceAll.CallTraceAll(WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month , Outsample_Length_Month ,
                          Initial_Capital , Plateau_Condition , TraceAll_Exist , TraceAll_ExistPass , TraceAll_Minimum , isOutputFile , SelectedFunction ,
                          TheilsU , MAPE , WFE , Profit_Factor_Score , NetProfit_MDD_Score)

                WFA = CallWFA.CallWFA(WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month , Outsample_Length_Month ,
                          Initial_Capital , Plateau_Condition , Plateau_Amount , WalkForward_PassWindow , WalkForward_Minimum , isOutputFile , SelectedFunction ,
                          TheilsU , MAPE , WFE , Profit_Factor_Score , NetProfit_MDD_Score)

                Longterm = CallLongterm.CallLongterm(Strategy , Target, Total_Period , Start_Day , End_Day , Insample_Length_Month , Outsample_Length_Month ,
                          Initial_Capital , Plateau_Condition , Longterm_Period , Longterm_Minimum , SelectedFunction ,
                          TheilsU , MAPE , WFE , Profit_Factor_Score , NetProfit_MDD_Score)

                TraceAll_Result = TraceAll.TraceAllAnalysis()
                WFA_WFA_Result, WFA_Plateau_Result = WFA.WFAAnalysis()
                Longterm_Result = Longterm.LongtermAnalysis()
                OutputFile(TraceAll_Result, WFA_WFA_Result, WFA_Plateau_Result, Longterm_Result, Target_DirPath)

                Count_TraceAll_Result = len(TraceAll_Result[TraceAll_Result==True])
                Count_WFA_Result = len(WFA_WFA_Result[WFA_WFA_Result == True])
                Count_WFA_Plateau_Result = len(WFA_Plateau_Result[WFA_Plateau_Result == True])
                Count_Longterm_Result = len(Longterm_Result[Longterm_Result == True])
                thisTarget_TraceAll_Result.append(Count_TraceAll_Result)
                thisTarget_WFA_Result.append(Count_WFA_Result)
                thisTarget_WFA_Result.append(Count_WFA_Plateau_Result)
                thisTarget_Longterm_Result.append(Count_Longterm_Result)

            TraceAll_Result_PassPercentTable.append(thisTarget_TraceAll_Result)
            WFA_Result_PassPercentTable.append(thisTarget_WFA_Result)
            Longterm_Result_PassPercentTable.append(thisTarget_Longterm_Result)

        TraceAll_Result_PassPercentTable = np.array(TraceAll_Result_PassPercentTable)
        WFA_Result_PassPercentTable = np.array(WFA_Result_PassPercentTable)
        Longterm_Result_PassPercentTable = np.array(Longterm_Result_PassPercentTable)

        PassMinimum_Columns = []
        for Minimum in PassMinimum:
            num = lambda x:x+str(Minimum)
            PassMinimum_Columns.append(num('PassMinimum:'))

        WFAList_Columns = []
        for Minimum in PassMinimum:
            num = lambda x: x + str(Minimum)
            WFAList_Columns.append(num('WF_PassMinimum:'))
            WFAList_Columns.append(num('Plateau_PassMinimum:'))

        TraceAll_Result_PassPercentTable = pd.DataFrame(TraceAll_Result_PassPercentTable, index=TargetList, columns=PassMinimum_Columns)
        TraceAll_Result_Table.append(TraceAll_Result_PassPercentTable)
        WFA_Result_PassPercentTable = pd.DataFrame(WFA_Result_PassPercentTable, index=TargetList, columns=WFAList_Columns)
        WFA_Result_Table.append(WFA_Result_PassPercentTable)
        Longterm_Result_PassPercentTable = pd.DataFrame(Longterm_Result_PassPercentTable, index=TargetList, columns=PassMinimum_Columns)
        Longterm_Result_Table.append(Longterm_Result_PassPercentTable)

    PassPercent_Keys = []
    for Percent in PassPercent:
        num = lambda x: x + str(Percent)
        PassPercent_Keys.append(num('PassPercent:'))

    All_TraceAll_Result_Table = pd.concat(TraceAll_Result_Table , axis=1 , keys=PassPercent_Keys)
    All_TraceAll_Result_Table.to_csv('C:\\Users\\amosr\\Desktop\\'+str(thisPeriod)+'TraceAll分析結果.csv', mode='a', header=True, index=True,encoding="big5")
    All_WFA_Result_Table = pd.concat(WFA_Result_Table , axis=1 , keys=PassPercent_Keys)
    All_WFA_Result_Table.to_csv('C:\\Users\\amosr\\Desktop\\' + str(thisPeriod) + 'WFA分析結果.csv', mode='a',header=True, index=True, encoding="big5")
    All_Longterm_Result_Table = pd.concat(Longterm_Result_Table, axis=1, keys=PassPercent_Keys)
    All_Longterm_Result_Table.to_csv('C:\\Users\\amosr\\Desktop\\' + str(thisPeriod) + 'Longterm分析結果.csv', mode='a', header=True, index=True, encoding="big5")

print("計算結束時間 : " + time.strftime("%H:%M:%S"))