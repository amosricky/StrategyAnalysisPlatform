import time
import pandas as pd
from WFAModule import WFA_ReturnRate_A , WFA_ReturnRate_B , WFA_ReturnRate_C , WFA_ReturnRate_D , WFA_ReturnRate_E , WFA_RiskFactor_A ,WFA_RiskFactor_B


class CallWFA:
    def __init__(self,WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month , Outsample_Length_Month ,
                 Initial_Capital , Plateau_Condition , Plateau_Amount , WalkForward_PassWindow , WalkForward_Minimum ,
                 isOutputFile , SelectedFunction, TheilsU, MAPE, WFE , Profit_Factor_Score , NetProfit_MDD_Score):

        self.WalkForward_DF = WalkForward_DF
        self.Total_Period = Total_Period
        self.Target_DirPath = Target_DirPath
        self.Insample_Length_Month = Insample_Length_Month
        self.Outsample_Length_Month = Outsample_Length_Month
        self.Initial_Capital = Initial_Capital
        self.Plateau_Condition = Plateau_Condition
        self.Plateau_Amount = Plateau_Amount
        self.WalkForward_PassWindow = WalkForward_PassWindow
        self.WalkForward_Minimum = WalkForward_Minimum
        self.isOutputFile = isOutputFile
        self.SelectedFunction = SelectedFunction
        self.TheilsU = TheilsU
        self.MAPE = MAPE
        self.WFE = WFE
        self.Profit_Factor_Score = Profit_Factor_Score
        self.NetProfit_MDD_Score = NetProfit_MDD_Score

    def WFAAnalysis(self):

        WalkForward_DF = self.WalkForward_DF
        Total_Period = self.Total_Period
        Target_DirPath = self.Target_DirPath
        Insample_Length_Month = self.Insample_Length_Month
        Outsample_Length_Month = self.Outsample_Length_Month
        Initial_Capital = self.Initial_Capital
        Plateau_Condition = self.Plateau_Condition
        Plateau_Amount = self.Plateau_Amount
        WalkForward_PassWindow = self.WalkForward_PassWindow
        WalkForward_Minimum = self.WalkForward_Minimum
        isOutputFile = self.isOutputFile
        SelectedFunction = self.SelectedFunction
        TheilsU = self.TheilsU
        MAPE = self.MAPE
        WFE = self.WFE
        Profit_Factor_Score = self.Profit_Factor_Score
        NetProfit_MDD_Score = self.NetProfit_MDD_Score


        WFARR_A = WFA_ReturnRate_A.WFA_ReturnRate_A(WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month ,
                Outsample_Length_Month , Initial_Capital , Plateau_Condition , Plateau_Amount , WalkForward_PassWindow ,
                WalkForward_Minimum , isOutputFile)

        WFARR_B = WFA_ReturnRate_B.WFA_ReturnRate_B(WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month ,
                Outsample_Length_Month , Initial_Capital , Plateau_Condition , Plateau_Amount , WalkForward_PassWindow ,
                WalkForward_Minimum , isOutputFile , SelectedFunction, TheilsU, MAPE, WFE)

        WFARR_C = WFA_ReturnRate_C.WFA_ReturnRate_C(WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month ,
                Outsample_Length_Month , Initial_Capital , Plateau_Condition , Plateau_Amount , WalkForward_PassWindow ,
                WalkForward_Minimum , isOutputFile , SelectedFunction, TheilsU, MAPE, WFE)

        WFARR_D = WFA_ReturnRate_D.WFA_ReturnRate_D(WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month ,
                Outsample_Length_Month , Initial_Capital , Plateau_Condition , Plateau_Amount , WalkForward_PassWindow ,
                WalkForward_Minimum , isOutputFile)

        WFARR_E = WFA_ReturnRate_E.WFA_ReturnRate_E(WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month ,
                Outsample_Length_Month , Initial_Capital , Plateau_Condition , Plateau_Amount , WalkForward_PassWindow ,
                WalkForward_Minimum , isOutputFile , SelectedFunction, TheilsU, MAPE, WFE)

        WFARF_A = WFA_RiskFactor_A.WFA_RiskFactor_A(WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month ,
                Outsample_Length_Month , Initial_Capital , Plateau_Condition , Plateau_Amount , WalkForward_PassWindow ,
                WalkForward_Minimum , isOutputFile , Profit_Factor_Score)

        WFARF_B = WFA_RiskFactor_B.WFA_RiskFactor_B(WalkForward_DF , Total_Period , Target_DirPath , Insample_Length_Month ,
                Outsample_Length_Month , Initial_Capital , Plateau_Condition , Plateau_Amount , WalkForward_PassWindow ,
                WalkForward_Minimum , isOutputFile , NetProfit_MDD_Score)

        WFA_RR_A_WFResult , WFA_RR_A_PlateauResult = WFARR_A.Analysis()
        WFA_RR_B_WFResult , WFA_RR_B_PlateauResult = WFARR_B.Analysis()
        WFA_RR_C_WFResult , WFA_RR_C_PlateauResult = WFARR_C.Analysis()
        WFA_RR_D_WFResult , WFA_RR_D_PlateauResult = WFARR_D.Analysis()
        WFA_RR_E_WFResult , WFA_RR_E_PlateauResult = WFARR_E.Analysis()
        WFA_RF_A_WFResult , WFA_RF_A_PlateauResult = WFARF_A.Analysis()
        WFA_RF_B_WFResult , WFA_RF_B_PlateauResult = WFARF_B.Analysis()

        WFA_WFResult = pd.Series([WFA_RR_A_WFResult, WFA_RR_B_WFResult, WFA_RR_C_WFResult, WFA_RR_D_WFResult,
                           WFA_RR_E_WFResult, WFA_RF_A_WFResult, WFA_RF_B_WFResult])

        WFA_PlateauResult = pd.Series([WFA_RR_A_PlateauResult , WFA_RR_B_PlateauResult , WFA_RR_C_PlateauResult,
                             WFA_RR_D_PlateauResult , WFA_RR_E_PlateauResult , WFA_RF_A_PlateauResult,
                             WFA_RF_B_PlateauResult])

        return WFA_WFResult , WFA_PlateauResult




