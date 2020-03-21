#_*_ encoding: utf-8 *_*
from django import forms
from Backtest.forms_function import Get_Symbol_List

class BacktestForm(forms.Form):
    Strategy = [
        ['BollingStrategy', 'BollingStrategy']
    ]

    Symbol = Get_Symbol_List()

    user_Strategy = forms.ChoiceField(label='交易策略', choices=Strategy)
    user_Symbol = forms.ChoiceField(label='商品選擇', choices=Symbol, initial=3)
    user_StartDay = forms.DateField(label='起始日', widget=forms.SelectDateWidget(years=[y for y in range(1988, 2018)]))
    user_EndDay = forms.DateField(label='結束日', widget=forms.SelectDateWidget(years=[y for y in range(1988, 2018)]))

class AnalysisForm(forms.Form):
    Strategy = [
        ['BollingStrategy', 'BollingStrategy']
    ]

    Function = [
        ['WFE' , 'WFE'],['MAPE' , 'MAPE'],['TheilsU' , 'TheilsU']
    ]

    Symbol = Get_Symbol_List()

    user_Strategy = forms.ChoiceField(label='交易策略', choices=Strategy)
    user_Symbol = forms.ChoiceField(label='商品選擇', choices=Symbol, initial=3)
    user_StartDay = forms.DateField(label='起始日', widget=forms.SelectDateWidget(years=[y for y in range(1988, 2018)]))
    user_EndDay = forms.DateField(label='結束日', widget=forms.SelectDateWidget(years=[y for y in range(1988, 2018)]))
    user_InSample_Lenght = forms.CharField(label='InSample長度(月)', max_length=50 , initial='60')
    user_OutSample_Lenght = forms.CharField(label='OutSample長度(月)', max_length=50 , initial='60')
    user_Initial_Capital = forms.CharField(label='Initial Capital', max_length=50 , initial='1000000')
    user_Plateau_Condition = forms.CharField(label='最小高原年化報酬率', max_length=50 , initial='0.1')
    user_Plateau_Amount = forms.CharField(label='最小高原點數量', max_length=50 , initial='20')
    user_SelectedFunction = forms.ChoiceField(label='Selected Function', choices=Function)
    user_PassPercent = forms.CharField(label='Pass Percent', max_length=50, initial='0.7')
    user_PassMinimum = forms.CharField(label='Pass Minimum', max_length=50, initial='20')

# class ReportForm(forms.Form):
#     Strategy = [
#         ['BollingStrategy', 'BollingStrategy']
#     ]
#
#     user_Strategy = forms.ChoiceField(label='交易策略', choices=Strategy , widget=forms.Select(attrs={'onchange':'renew_reportdir(this.selectedIndex);'}))
#     user_Paradir = forms.ChoiceField(label='參數資料夾', choices='' , widget=forms.Select(attrs={'onchange':'renew_reportlist();' , 'id':'reportdir'}))
#     user_SelecedReport = forms.ChoiceField(label='選擇報表', choices='' , widget=forms.Select(attrs={'id':'reportlist'}))









