import os
import sys
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta


class Parameter_Check:
    def __init__(self, Target_Path , Start_Day , End_Day , Insample_Length_Month , Outsample_Length_Month ):
        self.Target_Path = Target_Path
        self.Start_Day = Start_Day
        self.End_Day = End_Day
        self.Insample_Length_Month = Insample_Length_Month
        self.Outsample_Length_Month = Outsample_Length_Month

    def CheckFolder(self):

        Target_Path = self.Target_Path

        # 進行交易策略盈虧細節檔案之資料夾檢查
        # 如果不存在，印出交易策略盈虧細節資料夾不存在資訊且停止計算
        if (not(os.path.exists(Target_Path))):
            print(Target_Path, "\n策略盈虧細節資料夾不存在，請將盈虧細節資料夾放到指定路徑上。")
            sys.exit()
        else:pass

    def CheckParameter(self):
        Start_Day = self.Start_Day
        End_Day = self.End_Day
        Insample_Length_Month = self.Insample_Length_Month
        Outsample_Length_Month = self.Outsample_Length_Month

        print("-----輸入參數檢查-----")
        # 輸出相關使用者輸入參數之資訊。
        print("回測開始日：", Start_Day)
        print("回測結束日：", End_Day)
        print("Insample(訓練集)移動窗格長度：", Insample_Length_Month, "個月。")
        print("Outsample(測試集)移動窗格長度：", Outsample_Length_Month, "個月。")

    def CheckStartDay(self, Day):
        index = 0
        Real_Day = ''
        Start_Day = self.Start_Day
        Target_Path = self.Target_Path
        Day = datetime.datetime.strptime(Day, '%Y-%m-%d').date()

        File = pd.read_csv(os.path.join(Target_Path,os.listdir(Target_Path)[0]) , engine='python')
        File['Day'] = pd.to_datetime(File['Day'], format='%Y/%m/%d')
        if (len(File[File['Day'] == Day]) == 1):
            index = File[File['Day'] == Day].index.tolist()[0]
        else:
            Day += relativedelta(days=1)
            return self.CheckStartDay(str(Day))
        Real_Day = File.iloc[index]['Day']
        Real_Day = str(Real_Day).split(' ')
        return index , Real_Day[0]

    def CheckEndDay(self, Day):
        index = 0
        Real_Day = ''
        End_Day = self.End_Day
        Target_Path = self.Target_Path
        Day = datetime.datetime.strptime(Day, '%Y-%m-%d').date()

        File = pd.read_csv(os.path.join(Target_Path,os.listdir(Target_Path)[0]) , engine='python')
        File['Day'] = pd.to_datetime(File['Day'], format='%Y/%m/%d')

        if (len(File[File['Day'] == Day]) == 1):
            index = File[File['Day'] == Day].index.tolist()[0]
        else:
            Day -= relativedelta(days=1)
            return self.CheckEndDay(str(Day))
        Real_Day = File.iloc[index]['Day']
        Real_Day = str(Real_Day).split(' ')
        return index , Real_Day[0]

    def CheckSameDay(self , Original_Day , New_Day):
        Start_Day = self.Start_Day
        End_Day = self.End_Day

        Start_Day = datetime.datetime.strptime(Start_Day, '%Y-%m-%d').date()
        End_Day = datetime.datetime.strptime(End_Day, '%Y-%m-%d').date()
        Original_Day = datetime.datetime.strptime(Original_Day, '%Y-%m-%d').date()
        New_Day = datetime.datetime.strptime(New_Day , '%Y-%m-%d').date()

        if (Start_Day == Original_Day):
            if(Start_Day != New_Day):
                print('指定開始日非交易日，實際回測開始日為 : '+ str(New_Day))
        if (End_Day == Original_Day):
            if(End_Day != New_Day):
                print('指定結束日非交易日，實際回測結束日為 : ' + str(New_Day))

