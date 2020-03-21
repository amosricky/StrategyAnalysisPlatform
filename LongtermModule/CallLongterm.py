import os , time
import pandas as pd
from SystemParameter import *
from LongtermModule import Longterm_ReturnRate_A , Longterm_ReturnRate_B , Longterm_ReturnRate_C , Longterm_ReturnRate_D , \
    Longterm_ReturnRate_E , Longterm_RiskFactor_A , Longterm_RiskFactor_B


class CallLongterm:
    def __init__(self , Strategy ,  Target , Total_Period ,Start_Day,End_Day, Insample_Length_Month , Outsample_Length_Month ,
                 Initial_Capital , Plateau_Condition , Longterm_Period , Longterm_Minimum , SelectedFunction , TheilsU , MAPE ,
                 WFE , Profit_Factor_Score , NetProfit_MDD_Score):

        self.Strategy = Strategy
        self.Target = Target
        self.Total_Period = Total_Period
        self.Start_Day = Start_Day
        self.End_Day = End_Day
        self.Insample_Length_Month = Insample_Length_Month
        self.Outsample_Length_Month = Outsample_Length_Month
        self.Initial_Capital = Initial_Capital
        self.Plateau_Condition = Plateau_Condition
        self.Longterm_Period = Longterm_Period
        self.Longterm_Minimum = Longterm_Minimum
        self.SelectedFunction = SelectedFunction
        self.TheilsU = TheilsU
        self.MAPE = MAPE
        self.WFE = WFE
        self.Profit_Factor_Score = Profit_Factor_Score
        self.NetProfit_MDD_Score = NetProfit_MDD_Score

    def Read_All_File_Data(self):

        Strategy = self.Strategy
        Target = self.Target
        Start_Day = self.Start_Day
        End_Day = self.End_Day
        Target_Path = InputPath_Root + Strategy + "\\" +  Target + "_" + Start_Day + "_" + End_Day

        # 讀入所有細節資料。
        All_File_Data = {}
        print('Loading start')
        for Filename in os.listdir(Target_Path):
            Temp_File = open(os.path.join(Target_Path, Filename), 'rb')
            File = pd.read_csv(Temp_File)
            All_File_Data[Filename] = File
            Temp_File.close()
        print('Loading finished')

        return All_File_Data , Target_Path

    def LongtermAnalysis(self):

        All_File_Data , Target_Path = self.Read_All_File_Data()
        Total_Period = self.Total_Period
        Start_Day = self.Start_Day
        End_Day = self.End_Day
        Insample_Length_Month = self.Insample_Length_Month
        Outsample_Length_Month = self.Outsample_Length_Month
        Initial_Capital = self.Initial_Capital
        Plateau_Condition = self.Plateau_Condition
        Longterm_Period = self.Longterm_Period
        Longterm_Minimum = self.Longterm_Minimum
        SelectedFunction = self.SelectedFunction
        TheilsU = self.TheilsU
        MAPE = self.MAPE
        WFE = self.WFE
        Profit_Factor_Score = self.Profit_Factor_Score
        NetProfit_MDD_Score = self.NetProfit_MDD_Score


        LTRR_A = Longterm_ReturnRate_A.Longterm_ReturnRate_A(All_File_Data , Target_Path , Total_Period , Start_Day , End_Day,
                Insample_Length_Month , Outsample_Length_Month , Initial_Capital , Plateau_Condition , Longterm_Period ,
                Longterm_Minimum )

        LTRR_B = Longterm_ReturnRate_B.Longterm_ReturnRate_B(All_File_Data , Target_Path , Total_Period ,Start_Day , End_Day,
                Insample_Length_Month , Outsample_Length_Month , Initial_Capital , Plateau_Condition , Longterm_Period ,
                Longterm_Minimum , SelectedFunction , TheilsU , MAPE , WFE)

        LTRR_C = Longterm_ReturnRate_C.Longterm_ReturnRate_C(All_File_Data , Target_Path , Total_Period ,Start_Day , End_Day,
                Insample_Length_Month , Outsample_Length_Month , Initial_Capital , Plateau_Condition , Longterm_Period ,
                Longterm_Minimum , SelectedFunction , TheilsU , MAPE , WFE)

        LTRR_D = Longterm_ReturnRate_D.Longterm_ReturnRate_D(All_File_Data , Target_Path , Total_Period , Start_Day , End_Day,
                Insample_Length_Month , Outsample_Length_Month , Initial_Capital , Plateau_Condition , Longterm_Period ,
                Longterm_Minimum)

        LTRR_E = Longterm_ReturnRate_E.Longterm_ReturnRate_E(All_File_Data , Target_Path , Total_Period , Start_Day , End_Day,
                Insample_Length_Month , Outsample_Length_Month , Initial_Capital , Plateau_Condition , Longterm_Period ,
                Longterm_Minimum , SelectedFunction , TheilsU , MAPE , WFE)

        LTRF_A = Longterm_RiskFactor_A.Longterm_RiskFactor_A(All_File_Data , Target_Path , Total_Period , Start_Day , End_Day,
                Insample_Length_Month , Outsample_Length_Month , Initial_Capital , Plateau_Condition , Longterm_Period ,
                Longterm_Minimum , Profit_Factor_Score)

        LTRF_B = Longterm_RiskFactor_B.Longterm_RiskFactor_B(All_File_Data , Target_Path , Total_Period , Start_Day , End_Day,
                Insample_Length_Month , Outsample_Length_Month , Initial_Capital , Plateau_Condition , Longterm_Period ,
                Longterm_Minimum , NetProfit_MDD_Score)

        Longterm_RR_A_Result = LTRR_A.Analysis()
        Longterm_RR_B_Result = LTRR_B.Analysis()
        Longterm_RR_C_Result = LTRR_C.Analysis()
        Longterm_RR_D_Result = LTRR_D.Analysis()
        Longterm_RR_E_Result = LTRR_E.Analysis()
        Longterm_RF_A_Result = LTRF_A.Analysis()
        Longterm_RF_B_Result = LTRF_B.Analysis()

        Longterm_Result = pd.Series([Longterm_RR_A_Result , Longterm_RR_B_Result , Longterm_RR_C_Result , Longterm_RR_D_Result ,
                           Longterm_RR_E_Result , Longterm_RF_A_Result , Longterm_RF_B_Result])

        return Longterm_Result






