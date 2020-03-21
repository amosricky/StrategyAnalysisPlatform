import time
import pandas as pd
from TraceAllModule import TraceAll_ReturnRate_A , TraceAll_ReturnRate_B , TraceAll_ReturnRate_C , TraceAll_ReturnRate_D , \
    TraceAll_ReturnRate_E , TraceAll_RiskFactor_A , TraceAll_RiskFactor_B


class CallTraceAll:
    def __init__(self , WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month , Outsample_Length_Month ,
                 Initial_Capital , Plateau_Condition , TraceAll_Exist , TraceAll_ExistPass , TraceAll_Minimum , isOutputFile,
                 SelectedFunction , TheilsU , MAPE , WFE , Profit_Factor_Score , NetProfit_MDD_Score):

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
        self.Profit_Factor_Score = Profit_Factor_Score
        self.NetProfit_MDD_Score = NetProfit_MDD_Score

    def TraceAllAnalysis(self):

        WalkForward_DF = self.WalkForward_DF
        Total_Period = self.Total_Period
        Target_DirPath = self.Target_DirPath
        Insample_Length_Month = self.Insample_Length_Month
        Outsample_Length_Month = self.Outsample_Length_Month
        Initial_Capital = self.Initial_Capital
        Plateau_Condition = self.Plateau_Condition
        TraceAll_Exist = self.TraceAll_Exist
        TraceAll_ExistPass = self.TraceAll_ExistPass
        TraceAll_Minimum = self.TraceAll_Minimum
        isOutputFile = self.isOutputFile
        SelectedFunction = self.SelectedFunction
        TheilsU = self.TheilsU
        MAPE = self.MAPE
        WFE = self.WFE
        Profit_Factor_Score = self.Profit_Factor_Score
        NetProfit_MDD_Score = self.NetProfit_MDD_Score


        TARR_A = TraceAll_ReturnRate_A.TraceAll_ReturnRate_A(WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month ,
                Outsample_Length_Month , Initial_Capital , Plateau_Condition , TraceAll_Exist , TraceAll_ExistPass , TraceAll_Minimum ,
                isOutputFile)

        TARR_B = TraceAll_ReturnRate_B.TraceAll_ReturnRate_B(WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month ,
                Outsample_Length_Month , Initial_Capital , Plateau_Condition , TraceAll_Exist , TraceAll_ExistPass , TraceAll_Minimum ,
                isOutputFile , SelectedFunction , TheilsU , MAPE , WFE)

        TARR_C = TraceAll_ReturnRate_C.TraceAll_ReturnRate_C(WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month ,
                Outsample_Length_Month , Initial_Capital , Plateau_Condition , TraceAll_Exist , TraceAll_ExistPass , TraceAll_Minimum ,
                isOutputFile , SelectedFunction , TheilsU , MAPE , WFE)

        TARR_D = TraceAll_ReturnRate_D.TraceAll_ReturnRate_D(WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month ,
                Outsample_Length_Month , Initial_Capital , Plateau_Condition , TraceAll_Exist , TraceAll_ExistPass , TraceAll_Minimum ,
                isOutputFile)

        TARR_E = TraceAll_ReturnRate_E.TraceAll_ReturnRate_E(WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month ,
                Outsample_Length_Month , Initial_Capital , Plateau_Condition , TraceAll_Exist , TraceAll_ExistPass , TraceAll_Minimum ,
                isOutputFile , SelectedFunction , TheilsU , MAPE , WFE)

        TARF_A = TraceAll_RiskFactor_A.TraceAll_RiskFactor_A(WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month ,
                Outsample_Length_Month , Initial_Capital , Plateau_Condition , TraceAll_Exist , TraceAll_ExistPass , TraceAll_Minimum ,
                isOutputFile , Profit_Factor_Score)

        TARF_B = TraceAll_RiskFactor_B.TraceAll_RiskFactor_B(WalkForward_DF , Total_Period , Target_DirPath ,Insample_Length_Month ,
                Outsample_Length_Month , Initial_Capital , Plateau_Condition , TraceAll_Exist , TraceAll_ExistPass , TraceAll_Minimum ,
                isOutputFile , NetProfit_MDD_Score)


        TraceALL_RR_A_Result = TARR_A.Analysis()
        TraceALL_RR_B_Result = TARR_B.Analysis()
        TraceALL_RR_C_Result = TARR_C.Analysis()
        TraceALL_RR_D_Result = TARR_D.Analysis()
        TraceALL_RR_E_Result = TARR_E.Analysis()
        TraceALL_RF_A_Result = TARF_A.Analysis()
        TraceALL_RF_B_Result = TARF_B.Analysis()

        TraceAll_Result = pd.Series([TraceALL_RR_A_Result,TraceALL_RR_B_Result,TraceALL_RR_C_Result,TraceALL_RR_D_Result,
                           TraceALL_RR_E_Result,TraceALL_RF_A_Result,TraceALL_RF_B_Result])

        return TraceAll_Result


