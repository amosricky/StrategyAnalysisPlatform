import os
import time
import WalkForwardModule.WalkForward_Parameter_Function as Parameter_Function
import WalkForwardModule.WalkForward_Calculate_Function as Calculate_Function


def CallWalkForward(Target_Path,Target_DirPath , Start_Day , End_Day , Insample_Length_Month , Outsample_Length_Month ,Initial_Capital):

    if (not (os.path.exists(Target_DirPath))):
        os.makedirs(Target_DirPath)

    #參數檢查
    Source = Parameter_Function.Parameter_Check(Target_Path , Start_Day, End_Day, Insample_Length_Month, Outsample_Length_Month)
    Source.CheckFolder()
    Source.CheckParameter()
    Real_Start_Index , Real_Start_Day = Source.CheckStartDay(Start_Day)
    Real_End_Index , Real_End_Day = Source.CheckEndDay(End_Day)
    Source.CheckSameDay(Start_Day , Real_Start_Day)
    Source.CheckSameDay(End_Day , Real_End_Day)

    #開始計算
    Calculate = Calculate_Function.Calculate(Target_Path , Target_DirPath , Start_Day , End_Day , Insample_Length_Month , Outsample_Length_Month ,Initial_Capital)
    print ("計算開始時間 : " + time.strftime("%H:%M:%S"))
    Calculate.Sliding_Window()
    print ("計算結束時間 : " + time.strftime("%H:%M:%S"))

    return 0