###########變動參數##########
###########記得刪除中文######
# TargetList = ['1101 台泥' , '1102 亞泥' , '1216 統一' , '1301 台塑' , '1303 南亞' , '1326 台化' , '1402 遠東新' , '2002 中鋼' ,
#           '2105 正新' , '2303 聯電' , '2801 彰銀']
# TargetList = ['1504 東元' , '1605 華新' , '2312 金寶' , '2313 華通' , '2324 仁寶' , '2327 國巨' ,  '2337 旺宏'  ,
#               '2344 華邦電' , '2347 聯強' , '2352 佳世達' , '2353 宏碁' ,'2356 英業達' , '2360 致茂' ,  '2371 大同'  ,
#                '2376 技嘉' , '2377 微星' , '2379 瑞昱']

TargetList = ['1402']
Period = [36,48, 60]
PassPercent = [0.6, 0.7 , 0.8]
PassMinimum = [10 , 30 , 50]

#以下為固定參數
Strategy = 'BollingStrategy'
Target = ''
Start_Day = '1988-01-01'
End_Day = '2017-12-31'
Insample_Length_Month = ''
Outsample_Length_Month = ''
Initial_Capital = 1000000

#高原條件
Plateau_Condition = 0.10
Plateau_Amount = 20

#基本門檻
SelectedFunction = 'WFE'
TheilsU = 0.5
MAPE = 0.5
WFE = 0.5
Profit_Factor_Score = 1.5
NetProfit_MDD_Score = 1.5

# 依序追蹤門檻
TraceAll_Exist = ''
TraceAll_ExistPass = ''
TraceAll_Minimum = ''

#移動窗格門檻
WalkForward_PassWindow = ''
WalkForward_Minimum = ''

#長期追蹤門檻
Longterm_Period = ''
Longterm_Minimum = ''

#是否輸出報表
isOutputFile = True
