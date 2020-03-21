from SystemParameter import Strategy_Root

def ResetAPX(user_Strategy , user_Symbol , user_StartDay , user_EndDay):

    Strategy_Path = Strategy_Root + user_Strategy + ".apx"
    New_Strategy_Path = Strategy_Root + "New" + user_Strategy + ".apx"
    File = open(Strategy_Path, "r+")          #開啟檔案,須以r+讀寫模式
    FileString = File.read()

    # 修正AFL
    Start = FileString.find('.afl')
    FileString = FileString[:Start] + "_New" + FileString[Start:]

    #修正輸出路徑
    addPath = "+" + "\"" + "_" + user_StartDay + "_" + user_EndDay +"\""
    OutMkDirStart = FileString.find('symbolname);')
    FileString = FileString[:OutMkDirStart+10] +  addPath  + FileString[OutMkDirStart+10:]
    OutMkDirStart = FileString.find('symbolname+"\\\\\\\\"')
    FileString = FileString[:OutMkDirStart + 10] + addPath  + FileString[OutMkDirStart + 10:]

    #修正起訖日
    Start_DayStart = FileString.find('<FromDate>')
    OriginalStart_Day = FileString[Start_DayStart+10:Start_DayStart+20]
    FileString = FileString.replace(OriginalStart_Day,user_StartDay)
    End_DayStart = FileString.find('<ToDate>')
    OriginalEnd_Day = FileString[End_DayStart+8:End_DayStart+18]
    FileString = FileString.replace(OriginalEnd_Day,user_EndDay)
    File.close()
    NewFile = open(New_Strategy_Path, "w")          #開啟檔案,須以r+讀寫模式
    NewFile.write(FileString)
    NewFile.close()

    return New_Strategy_Path


