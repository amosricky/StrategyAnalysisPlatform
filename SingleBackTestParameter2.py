#此為單一回測全部所需參數
############使用者定義參數################
#窗格初始參數
Strategy = 'BollingStrategy'
Target = '1326'
Start_Day = '1988-01-01'
End_Day = '2017-12-31'
InSample_Length = 60
OutSample_Length = 60
Initial_Capital = 1000000

#共用變數
PassPercent = 0.7
PassMinimum = 20

# # 依序追蹤門檻
# TraceAll_Exist = PassPercent
# TraceAll_ExistPass = PassPercent
# TraceAll_Minimum = PassMinimum
#
# #移動窗格門檻
# WalkForward_PassWindow = PassPercent
# WalkForward_Minimum = PassMinimum
#
# #長期追蹤門檻
# Longterm_Period = PassPercent
# Longterm_Minimum = PassMinimum
#
# #高原條件
Plateau_Condition = 0.10
Plateau_Amount = 20

##計算方式
SelectedFunction = 'WFE'


############系統定義參數################
#基本門檻
TheilsU = 0.5
MAPE = 0.5
WFE = 0.5
Profit_Factor_Score = 1.5
NetProfit_MDD_Score = 1.5

#是否輸出報表
isOutputFile = True