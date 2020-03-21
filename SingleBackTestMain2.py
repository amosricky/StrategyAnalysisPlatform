import os , time
import pandas as pd
from SingleBackTestParameter2 import *
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
WalkForward = CreateWalkForwardDataFrame.WalkForwardDataFrame(Strategy , Target , Start_Day , End_Day , InSample_Length , OutSample_Length , Initial_Capital)
WalkForward_DF, Total_Period  = WalkForward.CreateDataFrame()
Target_DirPath = WalkForward.CreateOutputDir(PassPercent , PassMinimum)

TraceAll_Exist, TraceAll_ExistPass , WalkForward_PassWindow , Longterm_Period = PassPercent , PassPercent , PassPercent , PassPercent
TraceAll_Minimum , WalkForward_Minimum , Longterm_Minimum = PassMinimum , PassMinimum , PassMinimum

TraceAll = CallTraceAll.CallTraceAll(WalkForward_DF , Total_Period , Target_DirPath , InSample_Length , OutSample_Length ,
           Initial_Capital , Plateau_Condition , TraceAll_Exist , TraceAll_ExistPass , TraceAll_Minimum , isOutputFile,
           SelectedFunction , TheilsU , MAPE , WFE , Profit_Factor_Score , NetProfit_MDD_Score)

WFA = CallWFA.CallWFA(WalkForward_DF , Total_Period , Target_DirPath , InSample_Length , OutSample_Length  ,
      Initial_Capital , Plateau_Condition , Plateau_Amount , WalkForward_PassWindow , WalkForward_Minimum ,
      isOutputFile , SelectedFunction, TheilsU, MAPE, WFE , Profit_Factor_Score , NetProfit_MDD_Score)

Longterm = CallLongterm.CallLongterm(Strategy , Target , Total_Period , Start_Day , End_Day, InSample_Length , OutSample_Length ,
           Initial_Capital , Plateau_Condition , Longterm_Period , Longterm_Minimum , SelectedFunction , TheilsU , MAPE ,
           WFE , Profit_Factor_Score , NetProfit_MDD_Score)

TraceAll_Result = TraceAll.TraceAllAnalysis()
WFA_WFResult , WFA_PlateauResult = WFA.WFAAnalysis()
Longterm_Result = Longterm.LongtermAnalysis()
print("計算結束時間 : " + time.strftime("%H:%M:%S"))

OutputFile(TraceAll_Result , WFA_WFResult , WFA_PlateauResult , Longterm_Result , Target_DirPath)