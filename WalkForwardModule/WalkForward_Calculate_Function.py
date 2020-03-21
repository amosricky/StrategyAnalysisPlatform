import os
import math
import operator
import pandas as pd
import csv
import datetime
import threading
from dateutil.relativedelta import relativedelta

class Calculate:
    def __init__(self, Target_Path ,Target_DirPath, Start_Day , End_Day , Insample_Length_Month , Outsample_Length_Month ,Initial_Capital):

        self.Target_Path = Target_Path
        self.Target_DirPath = Target_DirPath
        self.Start_Day = Start_Day
        self.End_Day = End_Day
        self.Insample_Length_Month = Insample_Length_Month
        self.Outsample_Length_Month = Outsample_Length_Month
        self.Initial_Capital = Initial_Capital

    def InSampleOtherColumn(self, All_File_Data, Parameter_Filename, Training_Window_Start , Training_Window_End):

        #需回傳之參數
        Transcation_Number = 0

        #交易次數計算
        Window = (All_File_Data[Parameter_Filename][(All_File_Data[Parameter_Filename].index >= Training_Window_Start)&(All_File_Data[Parameter_Filename].index <= Training_Window_End)])
        Transcation_Number = len(Window[Window['action']=='Buy'])

        return Transcation_Number

    def OutSampleOtherColumn(self, All_File_Data, Parameter_Filename, Training_Window_Start, Training_Window_End, Testing_Window_Start, Testing_Window_End):

        # 需回傳之參數
        Transcation_Number = 0
        Window_Gross_Profit = 0
        Window_Gross_Loss = 0
        WindowMDD = 0

        # 累積淨利、MaxNet輔以MDD計算
        WindowPresentNet = 0
        WindowMaxNet = 0

        # OutSample交易次數計算
        OutSampleWindow = (All_File_Data[Parameter_Filename][(All_File_Data[Parameter_Filename].index >= Testing_Window_Start) & (All_File_Data[Parameter_Filename].index <= Testing_Window_End)])
        Transcation_Number = len(OutSampleWindow[OutSampleWindow['action'] == 'Buy'])

        #計算MDD等欄位
        Window = All_File_Data[Parameter_Filename].loc[Training_Window_Start:Testing_Window_End]
        Net_Shifted = All_File_Data[Parameter_Filename]['NetProfit'].copy().shift().loc[Training_Window_Start:Testing_Window_End]
        Window = Window.assign(Net_Shifted=Net_Shifted.values)

        for row in Window.itertuples():
            if (math.isnan(row.Net_Shifted)):
                pass
            else:
                GrossValue = row.NetProfit - row.Net_Shifted
                WindowPresentNet += GrossValue

                if (GrossValue > 0):
                    Window_Gross_Profit += GrossValue
                elif(GrossValue < 0):
                    Window_Gross_Loss += GrossValue

                if (WindowPresentNet > WindowMaxNet):
                    WindowMaxNet = WindowPresentNet
                if ((WindowPresentNet - WindowMaxNet) < WindowMDD):
                    WindowMDD = (WindowPresentNet - WindowMaxNet)

        return Transcation_Number, Window_Gross_Profit, Window_Gross_Loss, WindowMDD

        #   (原寫法)用For Loop 會很慢
        # for i in range(Training_Window_Start, Testing_Window_End + 1):
        #     # 不算第一天
        #     if (i > 0):
        #         GrossValue = All_File_Data[Parameter_Filename]['NetProfit'][i] - All_File_Data[Parameter_Filename]['NetProfit'][i - 1]
        #         WindowPresentNet += GrossValue
        #
        #         if(GrossValue>0):
        #             Window_Gross_Profit += GrossValue
        #         elif(GrossValue<0):
        #             Window_Gross_Loss += GrossValue
        #
        #         if (WindowPresentNet > WindowMaxNet):
        #             WindowMaxNet = WindowPresentNet
        #         elif ((WindowPresentNet - WindowMaxNet) < WindowMDD):
        #             WindowMDD = WindowPresentNet - WindowMaxNet

    def InSampleWindowResult(self, All_File_Data , Training_Window_Start,Training_Window_End, Factor_Sort ,Initial_Capital, Training_File_Output):

        Start_NetProfit_Value = 0
        End_NetProfit_Value = 0
        NetProfit_Value = 0
        Transcation_Number = 0

        for index in range(0, len(All_File_Data)):
            Parameter_Filename = Factor_Sort[index][0]
            Start_Day = All_File_Data[Parameter_Filename]["Day"][Training_Window_Start]
            End_Day = All_File_Data[Parameter_Filename]["Day"][Training_Window_End]
            Transcation_Number = self.InSampleOtherColumn(All_File_Data,Parameter_Filename,Training_Window_Start,Training_Window_End)

            if (Training_Window_Start == 0):
                Start_NetProfit_Value = All_File_Data[Parameter_Filename]['NetProfit'][Training_Window_Start]
                End_NetProfit_Value = All_File_Data[Parameter_Filename]['NetProfit'][Training_Window_End]
                NetProfit_Value = End_NetProfit_Value - Start_NetProfit_Value
                NetProfit_Percent = NetProfit_Value / (Start_NetProfit_Value + Initial_Capital)

            elif (Training_Window_Start != 0):
                Start_NetProfit_Value = All_File_Data[Parameter_Filename]['NetProfit'][Training_Window_Start - 1]
                End_NetProfit_Value = All_File_Data[Parameter_Filename]['NetProfit'][Training_Window_End]
                NetProfit_Value = End_NetProfit_Value - Start_NetProfit_Value
                NetProfit_Percent = NetProfit_Value / (Start_NetProfit_Value + Initial_Capital)

            Output = [Parameter_Filename, Start_Day, End_Day, Start_NetProfit_Value, End_NetProfit_Value, NetProfit_Value,NetProfit_Percent, Transcation_Number]
            Training_File_Output.writerow(Output)
        return 0

    def OutSampleWindowResult(self, All_File_Data , Training_Window_Start,Training_Window_End , Testing_Window_Start,Testing_Window_End, Factor_Sort ,Initial_Capital, Testing_File_Output):

        Start_NetProfit_Value = 0
        End_NetProfit_Value = 0
        NetProfit_Value = 0
        Transcation_Number = 0

        for index in range(0, len(All_File_Data)):
            Parameter_Filename = Factor_Sort[index][0]
            Start_Day = All_File_Data[Parameter_Filename]["Day"][Testing_Window_Start]
            End_Day = All_File_Data[Parameter_Filename]["Day"][Testing_Window_End]
            Transcation_Number, WindowGrossProfit, WindowGrossLoss , WindowMDD = self.OutSampleOtherColumn(All_File_Data,Parameter_Filename,Training_Window_Start,Training_Window_End,Testing_Window_Start,Testing_Window_End)

            if (Training_Window_Start==0):
                Start_NetProfit_Value = All_File_Data[Parameter_Filename]['NetProfit'][Testing_Window_Start]
                End_NetProfit_Value = All_File_Data[Parameter_Filename]['NetProfit'][Testing_Window_End]
                NetProfit_Value = End_NetProfit_Value - Start_NetProfit_Value
                NetProfit_Percent = NetProfit_Value / (Start_NetProfit_Value + Initial_Capital)
                WindowNet = End_NetProfit_Value - All_File_Data[Parameter_Filename]['NetProfit'][Training_Window_Start]

            elif(Training_Window_Start!=0):
                Start_NetProfit_Value = All_File_Data[Parameter_Filename]['NetProfit'][Testing_Window_Start-1]
                End_NetProfit_Value = All_File_Data[Parameter_Filename]['NetProfit'][Testing_Window_End]
                NetProfit_Value =  End_NetProfit_Value - Start_NetProfit_Value
                NetProfit_Percent = NetProfit_Value / (Start_NetProfit_Value + Initial_Capital)
                WindowNet = End_NetProfit_Value - All_File_Data[Parameter_Filename]['NetProfit'][Training_Window_Start-1]

            Output = [Parameter_Filename, Start_Day, End_Day, Start_NetProfit_Value, End_NetProfit_Value, NetProfit_Value,
                    NetProfit_Percent, Transcation_Number, WindowGrossProfit, WindowGrossLoss, WindowNet ,WindowMDD]
            Testing_File_Output.writerow(Output)
        return 0

    def Cutting_Time(self):

        #窗格設定變數
        Start_Day = self.Start_Day
        End_Day = self.End_Day
        Insample_Length_Month = self.Insample_Length_Month
        Outsample_Length_Month = self.Outsample_Length_Month

        #回傳InSample , OutSample 切割區間
        InSample = []
        OutSample = []

        #datetime
        Start_Day = datetime.datetime.strptime(Start_Day, '%Y-%m-%d').date()
        End_Day = datetime.datetime.strptime(End_Day, '%Y-%m-%d').date()

        # 初始 InSample Time
        InSampleStart = Start_Day
        InSampleEnd = InSampleStart
        InSampleEnd += relativedelta(months=+Insample_Length_Month, days=-1)

        while (InSampleEnd < End_Day):
            InSamplePeriod = []
            InSamplePeriod.append(str(InSampleStart))
            InSamplePeriod.append(str(InSampleEnd))
            InSample.append(InSamplePeriod)
            InSampleStart += relativedelta(months=+Outsample_Length_Month)
            InSampleEnd += relativedelta(months=+Outsample_Length_Month)

        # 初始 OutSample Time
        OutSampleStart = Start_Day
        OutSampleStart += relativedelta(months=+Insample_Length_Month)
        OutSampleEnd = OutSampleStart
        OutSampleEnd += relativedelta(months=+Insample_Length_Month, days=-1)

        while (OutSampleStart < End_Day):
            OutSamplePeriod = []
            if (OutSampleEnd > End_Day):
                OutSamplePeriod.append(str(OutSampleStart))
                OutSamplePeriod.append(str(End_Day))
                OutSample.append(OutSamplePeriod)

            else:
                OutSamplePeriod.append(str(OutSampleStart))
                OutSamplePeriod.append(str(OutSampleEnd))
                OutSample.append(OutSamplePeriod)

            OutSampleStart += relativedelta(months=+Outsample_Length_Month)
            OutSampleEnd += relativedelta(months=+Outsample_Length_Month)
        return InSample , OutSample

    def StartDayChange(self,Window_Start_Day):

        Target_Path = self.Target_Path
        Day = datetime.datetime.strptime(Window_Start_Day, '%Y-%m-%d').date()
        File = pd.read_csv(os.path.join(Target_Path, os.listdir(Target_Path)[0]), engine='python')
        File['Day'] = pd.to_datetime(File['Day'], format='%Y/%m/%d')
        if (len(File[File['Day'] == Day]) == 1):
            index = File[File['Day'] == Day].index.tolist()[0]
        else:
            Day += relativedelta(days=1)
            return self.StartDayChange(str(Day))
        return index

    def EndDayChange(self,Window_End_Day):

        Target_Path = self.Target_Path
        Day = datetime.datetime.strptime(Window_End_Day, '%Y-%m-%d').date()
        File = pd.read_csv(os.path.join(Target_Path, os.listdir(Target_Path)[0]), engine='python')
        File['Day'] = pd.to_datetime(File['Day'], format='%Y/%m/%d')
        if (len(File[File['Day'] == Day]) == 1):
            index = File[File['Day'] == Day].index.tolist()[0]
        else:
            Day -= relativedelta(days=1)
            return self.EndDayChange(str(Day))
        return index

    def Sliding_Window(self):

        Target_Path = self.Target_Path
        Target_DirPath = self.Target_DirPath
        Start_Day = self.Start_Day
        End_Day = self.End_Day
        Insample_Length_Month = self.Insample_Length_Month
        Outsample_Length_Month = self.Outsample_Length_Month
        Initial_Capital = self.Initial_Capital

        # 切割InSample , OutSample 區間
        InSample , OutSample = self.Cutting_Time()

        # 讀入所有細節資料。
        All_File_Data = {}
        # 紀錄該回測窗格所有參數組於InSample移動窗格的績效。
        Training_Data_Result = {}
        # 紀錄此次計算為第幾期移動窗格。
        Window_Number = 1

        print('Loading start')
        for Filename in os.listdir(Target_Path):
            Temp_File = open(os.path.join(Target_Path, Filename), 'rb')
            File = pd.read_csv(Temp_File)
            All_File_Data[Filename] = File
            Temp_File.close()
        print('Loading finished')

        # 進行移動窗格的計算，透過迴圈來推進移動窗格。
        # K_bars : 為回測起始日開始，結束於回測結束日，每次移動以測試集長度做推移。
        for Period in range(0,len(InSample)):

            # 宣告InSample起始日與結束日
            Training_Window_Start_Day = InSample[Period][0]
            Training_Window_End_Day = InSample[Period][1]
            #找出正確交易日
            Training_Window_Start = self.StartDayChange(Training_Window_Start_Day)
            Training_Window_End = self.EndDayChange(Training_Window_End_Day)

            # 宣告OutSample起始日與結束日
            Testing_Window_Start_Day = OutSample[Period][0]
            Testing_Window_End_Day = OutSample[Period][1]
            # 找出正確交易日
            Testing_Window_Start = self.StartDayChange(Testing_Window_Start_Day)
            Testing_Window_End = self.EndDayChange(Testing_Window_End_Day)

            for Filename in os.listdir(Target_Path):
                Numerator = All_File_Data[Filename]['NetProfit'][Training_Window_End] - All_File_Data[Filename]['NetProfit'][Training_Window_Start]
                Denominator = All_File_Data[Filename]['NetProfit'][Training_Window_Start] + Initial_Capital
                Cal_Value = Numerator / Denominator
                Training_Data_Result[Filename] = Cal_Value

            # Factor_Sort :將所有參數組依據NetProfit之績效由「大到小」做排序並儲存。
            Factor_Sort = sorted(Training_Data_Result.items(), key=operator.itemgetter(1), reverse=True)

            Output_Training_Data = open(Target_DirPath +"\\" + str(Window_Number) + "_" + str(
                    Training_Window_Start_Day) + "~" + str(Training_Window_End_Day) + "_InSample_Result.csv", 'w',newline='')
            Output_Testing_Data = open(Target_DirPath +"\\" + str(Window_Number) + "_" + str(
                    Testing_Window_Start_Day) + "~" + str(Testing_Window_End_Day) + "_OutSample_Result.csv", 'w',newline='')
            Training_File_Output = csv.writer(Output_Training_Data, quoting=csv.QUOTE_ALL)
            Testing_File_Output = csv.writer(Output_Testing_Data, quoting=csv.QUOTE_ALL)
            Training_File_Output.writerow(['Filename', 'Begin', 'End', 'Start_NetProfit' ,'End_NetProfit' ,'NetProfit', 'NetProfit_Percent' , 'Number_of_Transactions' ])
            Testing_File_Output.writerow(['Filename', 'Begin', 'End', 'Start_NetProfit' ,'End_NetProfit' ,'NetProfit', 'NetProfit_Percent' , 'Number_of_Transactions' , 'Window_GrossProfit' , 'Window_GrossLoss' ,  'Window_Net' , 'Window_MDD'])

            # 該期移動窗格InSample計算
            threading.Thread(target=self.InSampleWindowResult(All_File_Data, Training_Window_Start, Training_Window_End, Factor_Sort,Initial_Capital, Training_File_Output)).start()

            # 該期移動窗格OutSample計算
            threading.Thread(target=self.OutSampleWindowResult(All_File_Data, Training_Window_Start, Training_Window_End,Testing_Window_Start, Testing_Window_End, Factor_Sort,Initial_Capital, Testing_File_Output)).start()

            Output_Training_Data.close()
            Output_Testing_Data.close()

            # print(Window_Number)
            # 移動窗格期數編號根據可推移次數增加。
            Window_Number = Window_Number + 1

        return 0
