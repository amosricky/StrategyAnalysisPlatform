from django.shortcuts import render
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from Backtest import forms
from Backtest.forms_function import Check_isAlreadyBacktest , Check_isAlreadyAnalysis
from Amibroker.ResetAPX import ResetAPX
from Amibroker.CallAmibroker import Execute
import win32com.client
import time, datetime , os
import win32api
import pythoncom
from SingleBackTestMain import ExecuteSingleBackTest
from Backtest.forms_function import Get_ReportDir_List , Get_Report_List
from SystemParameter import OutputPath_Root
from django_tables2.tables import Table
import pandas as pd
import django_tables2 as tables

#回測每日盈虧績效
def index(request):
    if request.method == 'POST':
        form = forms.BacktestForm(request.POST)
        if form.is_valid():

            user_Strategy = form.cleaned_data['user_Strategy']
            user_Symbol = form.cleaned_data['user_Symbol']
            user_StartDay = form.cleaned_data['user_StartDay']
            user_EndDay = form.cleaned_data['user_EndDay']
            message , isExist = Check_isAlreadyBacktest(user_Strategy , user_Symbol , user_StartDay , user_EndDay)

            if(isExist==False):
                win32api.MessageBox(0, message, '使用者您好', 0x00001000)
                StrategyPath = ResetAPX(user_Strategy, user_Symbol, str(user_StartDay), str(user_EndDay))
                pythoncom.CoInitialize()
                Execute(StrategyPath , user_Symbol)

        else:
            message = "請檢查您輸入的資訊是否正確！"
    else:
        form = forms.BacktestForm()

    template = get_template('index.html')
    html = template.render(locals())

    return HttpResponse(html)

#執行穩健性分析
def Analysis(request):
    if request.method == 'POST':
        form = forms.AnalysisForm(request.POST)
        if form.is_valid():

            user_Strategy = form.cleaned_data['user_Strategy']
            user_Target = str(form.cleaned_data['user_Symbol'])
            user_StartDay = str(form.cleaned_data['user_StartDay'])
            user_EndDay = str(form.cleaned_data['user_EndDay'])
            user_InSample_Length = int(form.cleaned_data['user_InSample_Lenght'])
            user_OutSample_Length = int(form.cleaned_data['user_OutSample_Lenght'])
            user_Initial_Capital = int(form.cleaned_data['user_Initial_Capital'])
            user_Plateau_Condition = float(form.cleaned_data['user_Plateau_Condition'])
            user_Plateau_Amount = int(form.cleaned_data['user_Plateau_Amount'])
            user_SelectedFunction = form.cleaned_data['user_SelectedFunction']
            user_PassPercent = float(form.cleaned_data['user_PassPercent'])
            user_PassMinimum = int(form.cleaned_data['user_PassMinimum'])

            n,isExist = Check_isAlreadyBacktest(user_Strategy, user_Target, user_StartDay, user_EndDay)

            if(isExist==False):
                message = "每日盈虧績效檔案不存在,請先進行績效回測！"

            else:
                isAnalysis = Check_isAlreadyAnalysis(user_Strategy, user_Target, user_StartDay, user_EndDay,
                                                     user_InSample_Length, user_OutSample_Length, user_PassPercent, user_PassMinimum)
                if((isAnalysis==False)):

                    win32api.MessageBox(0, '開始進行回測', '使用者您好', 0x00001000)

                    ExecuteSingleBackTest(user_Strategy , user_Target , user_StartDay , user_EndDay ,
                               user_InSample_Length ,user_OutSample_Length , user_Initial_Capital , user_Plateau_Condition ,
                               user_Plateau_Amount , user_SelectedFunction , user_PassPercent , user_PassMinimum)

                message = "穩健性分析完成,請查看績效報表"

        else:
            message = "請檢查您輸入的資訊是否正確！"
    else:
        form = forms.AnalysisForm()

    template = get_template('Analysis.html')
    html = template.render(locals())

    return HttpResponse(html)

#績效結果報表
def Report(request):

    if request.method == 'POST':
        #將被選擇的報表轉為dataframe
        Strategy = request.POST['Strategy']
        ReprotDir = request.POST['ReportDir']
        Report = request.POST['ReportList']
        ReportPath = os.path.join(os.path.join(os.path.join(OutputPath_Root , Strategy),ReprotDir),Report)
        Temp_Report = open(ReportPath, 'rb')
        Pd_Temp_Report = pd.read_csv(Temp_Report)

        #開啟原報表html
        OriginalHtml = open('templates\\Report.html', "r+", encoding='utf8')  # 開啟檔案,須以r+讀寫模式
        Temp_Report_String = OriginalHtml.read()

        #抽出新的表格
        NewTableString = Pd_Temp_Report.to_html()
        TableStart = NewTableString.find('<thead>')
        TableEnd = NewTableString.find('</table>')

        #將新的表格插入後輸出成新的html
        htmlStart = Temp_Report_String.find('table-condensed">')
        NewHtmlString = Temp_Report_String[:htmlStart+17] + NewTableString[TableStart:TableEnd] + Temp_Report_String[htmlStart+17:]
        NewHtml = open('templates\\ShowReport.html', "wb+")  # 開啟檔案,須以r+讀寫模式
        NewHtml.write(NewHtmlString.encode('utf-8'))
        NewHtml.close()
        template = get_template('ShowReport.html')
        html = template.render(locals())
        return HttpResponse(html)

    ReportDir = Get_ReportDir_List()
    ReportList = Get_Report_List()
    template = get_template('Report.html')
    html = template.render(locals())
    return HttpResponse(html)



