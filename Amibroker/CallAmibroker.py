import win32com.client
import time, datetime
import pythoncom

def Execute(StrategyPath , Symbol):

    Amibroker = win32com.client.Dispatch("Broker.Application")

    try:
        NewAnalysis = Amibroker.AnalysisDocs.Open(StrategyPath);
        start = datetime.datetime.now()
        Amibroker.Documents.Open(Symbol)
        if (NewAnalysis):

            isSuccess = NewAnalysis.Run(4)
            # Action of Run
            # 0 : Scan
            # 1 : Exploration
            # 2 : Portfolio Backtest
            # 3 : Individual Backtest
            # 4 : Portfolio Optimization
            # 5 : Individual Optimization (supported starting from v5.69)
            # 6 : Walk Forward Test

            while NewAnalysis.IsBusy:
                print("Processing...")

                time.sleep(5)  # check IsBusy every 5 second

            if isSuccess:
                print("Finish: ", isSuccess)

            print(datetime.datetime.now() - start)
            NewAnalysis.Close();  # close new Analysis
    # catch python COM server error
    except pythoncom.com_error as error:
        print(error, vars(error), error.args)
        hr, msg, exc, arg = error.args
