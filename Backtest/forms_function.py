import os
import pandas as pd
import json
from SystemParameter import SymbolPath , InputPath_Root , OutputPath_Root

#取得所有股票代碼
def Get_Symbol_List():

    SymbolList = []

    if (os.path.exists(SymbolPath)):
        File = open(SymbolPath, 'rb')
        File = pd.read_csv(File,sep = ',')
        Symbol = pd.DataFrame(File)

        for row in Symbol.itertuples():
            Symbol = str(row.Symbol)
            Fullname = str(row.Fullname)
            rowList = [Symbol , Fullname]
            SymbolList.append(rowList)

    return SymbolList

def Get_ReportDir_List():

    ReportDirList = []

    if(os.path.exists(OutputPath_Root)):
        for Strategy in os.listdir(OutputPath_Root):
            StrategyDir = []
            for Dir in os.listdir(os.path.join(OutputPath_Root , Strategy)):
                StrategyDir.append(Dir)
            DirList = [Strategy , StrategyDir]
            ReportDirList.append(DirList)
    ReportDir = json.dumps(ReportDirList)

    return ReportDir

def Get_Report_List():

    Report_List = []
    Path = OutputPath_Root

    if(os.path.exists(Path)):
        if(os.path.exists(os.path.join(Path , os.listdir(Path)[0]))):
            Path = os.path.join(Path , os.listdir(Path)[0])
            if(os.path.exists(os.path.join(Path , os.listdir(Path)[0]))):
                Path = os.path.join(Path, os.listdir(Path)[0])
                Report_List = os.listdir(Path)
    Report = json.dumps(Report_List , ensure_ascii=False)

    return Report

def Check_isAlreadyBacktest(user_Strategy , user_Symbol , user_StartDay , user_EndDay):

    message = ''
    isExist = False

    Path = InputPath_Root + user_Strategy + "\\" +str(user_Symbol)+"_"+str(user_StartDay)+"_"+str(user_EndDay)
    if(os.path.exists(Path)):
        message = '每日盈虧績效檔案已存在'
        isExist = True
    else:
        message = '每日盈虧績效檔案不存在,開始進行回測'

    return message , isExist

def Check_isAlreadyAnalysis(user_Strategy , user_Target , user_StartDay , user_EndDay ,
                           user_InSample_Length , user_OutSample_Length , user_PassPercent , user_PassMinimum):
    isAnalysis = False
    Path = OutputPath_Root + user_Strategy + "\\" +str(user_Target)+"_"+str(user_StartDay)+"_"+str(user_EndDay)+"_"+str(user_InSample_Length)+"_"+str(user_OutSample_Length)+"_"+str(user_PassPercent)+"_"+str(user_PassMinimum)

    if(os.path.exists(Path)):

        isAnalysis = True
    else:
        pass

    return isAnalysis

