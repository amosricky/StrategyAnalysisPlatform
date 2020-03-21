import WalkForwardModule.WalkForward_Main as WalkForward_Main
from SystemParameter import *
import pandas as pd
import os , shutil

class WalkForwardDataFrame:
    def __init__(self, Strategy , Target , Start_Day , End_Day , Insample_Length_Month , Outsample_Length_Month , Initial_Capital):

        self.Strategy = Strategy
        self.Target = Target
        Target_Path = InputPath_Root + Strategy +"\\" + str(Target)
        self.Start_Day = Start_Day
        self.End_Day = End_Day
        self.Insample_Length_Month = Insample_Length_Month
        self.Outsample_Length_Month = Outsample_Length_Month
        self.Initial_Capital = Initial_Capital

        # 移動窗格資料夾名
        self.Target_DirName = str(Target)+ "_" + Start_Day + "_" + End_Day + "_" + str(
            Insample_Length_Month) + "_" + str(Outsample_Length_Month)

    def ComputeWalkForward(self):

        Strategy = self.Strategy
        Target = self.Target
        Start_Day = self.Start_Day
        End_Day = self.End_Day
        Target_Path = InputPath_Root + Strategy + "\\" +  Target + "_" + Start_Day + "_" + End_Day
        Target_DirPath = OutputWF_Root + Strategy + '\\' + self.Target_DirName
        Start_Day = self.Start_Day
        End_Day = self.End_Day
        Insample_Length_Month = self.Insample_Length_Month
        Outsample_Length_Month = self.Outsample_Length_Month
        Initial_Capital = self.Initial_Capital

        WalkForward_Main.CallWalkForward(Target_Path, Target_DirPath, Start_Day, End_Day,Insample_Length_Month,Outsample_Length_Month,Initial_Capital)

    def CreateDataFrame(self):

        #建立移動窗格Dataframe
        Strategy = self.Strategy
        Target_DirName = self.Target_DirName
        Target_DirPath = OutputWF_Root + Strategy + '\\' + Target_DirName

        if (not (os.path.exists(Target_DirPath))):
            os.makedirs(Target_DirPath)
            self.ComputeWalkForward()
            WalkForwardDF, TotalPeriod  = self.CreateDataFrame()
        else:
            WalkForwardDF = {}
            TotalPeriod = int(len(os.listdir(Target_DirPath)) / 2)

            for Period in range(1, TotalPeriod + 1):
                for Filename in os.listdir(Target_DirPath):
                    FilePath = os.path.join(Target_DirPath, Filename)

                    if ("InSample" in Filename) and (str(Period) in Filename.split('_')[0]):
                        FrameName = "Training_" + str(Period)
                        File = open(FilePath, 'rb')
                        File = pd.read_csv(File)
                        WalkForwardDF[FrameName] = File

                    if ("OutSample" in Filename) and (str(Period) in Filename.split('_')[0]):
                        FrameName = "Testing_" + str(Period)
                        File = open(FilePath, 'rb')
                        File = pd.read_csv(File)
                        WalkForwardDF[FrameName] = File

        # 回傳窗格DF
        return WalkForwardDF, TotalPeriod

    def CreateOutputDir(self, PassPercent , PassMinimum):

        # 建立報表輸出資料夾
        Strategy = self.Strategy
        Target_DirName = self.Target_DirName + "_" + str(PassPercent) + "_" + str(PassMinimum)
        Target_DirPath = OutputPath_Root + Strategy + "\\" + Target_DirName

        if ((os.path.exists(Target_DirPath))):
            shutil.rmtree(Target_DirPath)
            os.mkdir(Target_DirPath)

        else:
            os.makedirs(Target_DirPath)

        #回傳此次分析的輸出資料夾路徑
        return Target_DirPath











