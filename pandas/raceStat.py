import pandas as pd
import matplotlib.pyplot as plt

def plotLineChart(dataFrame, plotNum:int, title:str, xlabel:str, ylabel:str, ylim=None):
    # dataFrame.transpose().plot(xticks=dataFrame.columns)
    for i in range(plotNum):       
        linestyle = '-' if driverInfo.loc[i+1,'PosInTeam'] == 1 else ':'
        dataFrame.iloc[i, :driverInfo.loc[i+1,'Laps']-1].plot(color=driverInfo.loc[i+1,'Color'], linestyle=linestyle)
    # linestyle = - -- -. :
    plt.legend(loc='lower right')
    plt.xlim(1,lapAmount)
    plt.xticks(dataFrame.columns)

    plt.title(title)
    plt.xlabel(xlabel)   
    plt.ylabel(ylabel)
    if ylim:
        plt.ylim(ylim[0], ylim[1])
    plt.show()

def plotSectorAvg(s1, s2, s3):
    df = pd.DataFrame(index=driverInfo['Driver'], columns=['S1', 'S2', 'S3'])
    for i in range(driverAmount):
        df['S1'].iat[i] = s1.iloc[i, :driverInfo['Laps'].iloc[i]-1].mean()
        df['S2'].iat[i] = s2.iloc[i, :driverInfo['Laps'].iloc[i]-1].mean()
        df['S3'].iat[i] = s3.iloc[i, :driverInfo['Laps'].iloc[i]-1].mean()
    df.plot.barh(stacked=True)

    plt.title('Average Sector Times')
    plt.xlabel('Driver')
    plt.ylabel('Sector Times(s)')
    plt.show()

def getDriverPosInTeam():
    li = []
    driverInfo['PosInTeam'] = 2
    for i in driverInfo.index:
        if driverInfo['Team'].at[i] not in li:
            li.append(driverInfo['Team'].at[i])
            driverInfo['PosInTeam'].at[i] = 1

def getFinishedLap():
    driverInfo['Laps'] = 0
    for i in range(driverAmount):
        for j in range(lapAmount-1, -1, -1):
            if lapTime.iat[i, j] != 0:
                driverInfo['Laps'].iat[i] = j+1
                break

# 0-3  S1       S2      S3      Laptime 
# 4-7  Tyre     Wear    Fuel    ERS deployed 
# 8-11 FL       C       KPIs    Top Speed
filePath = r"F:/BattleFeed/pandas/Excel/Monza.csv"
driverAmount = 20
lapAmount = 27
colorMap = pd.Series({'Mercedes':'#33C7B6', 'Ferrari':'#EA0017', 'Red Bull Racing':'#313FE0', 'Renault':'#F9C65A', 'McLaren':'#E28937',\
    'Racing Point':'#E698C1', 'Alpha Tauri':'#153248', 'Alfa Romeo':'#85030A', 'Haas':'#78787A', 'Williams':'#B8D6F5'},name='Color')

# ----------读取csv的两个区域-----------
driverInfo = pd.read_csv(filePath, sep=';', skiprows=1, nrows=driverAmount, index_col='No.')
driverInfo = driverInfo.join(colorMap, on='Team')
getDriverPosInTeam()

lapInfo = pd.read_csv(filePath, sep=';', skiprows=driverAmount+4, index_col=0)
lapInfo.drop(lapInfo.columns[len(lapInfo.columns)-1], axis=1, inplace=True)

# ----------------绘图-----------------
lapTime = pd.DataFrame(data=[lapInfo.iloc[:,12*i+3] for i in range(driverAmount)],index=driverInfo['Driver'])
getFinishedLap()
plotLineChart(lapTime, driverAmount, 'Match Lap Time', 'Lap', 'Lap Time(sec)', [120,60])

# sector1 = pd.DataFrame(data=[lapInfo.iloc[:,12*i] for i in range(driverAmount)],index=driverInfo['Driver'])
# sector2 = pd.DataFrame(data=[lapInfo.iloc[:,12*i+1] for i in range(driverAmount)],index=driverInfo['Driver'])
# sector3 = pd.DataFrame(data=[lapInfo.iloc[:,12*i+2] for i in range(driverAmount)],index=driverInfo['Driver'])
# plotSectorAvg(sector1, sector2, sector3)

# tyreWear = pd.DataFrame(data=[lapInfo.iloc[:,12*i+5] for i in range(driverAmount)],index=driverInfo['Driver'])
# plotLineChart(tyreWear, driverAmount, 'Tyre Wear', 'Lap', 'Wear(%)', [0,100])

# fuel = pd.DataFrame(data=[lapInfo.iloc[:,12*i+6] for i in range(driverAmount)],index=driverInfo['Driver'])
# plotLineChart(fuel, driverAmount, 'Fuel', 'Lap', 'Fuel Load(kg)', [0,100])

# ERS_deployed = pd.DataFrame(data=[lapInfo.iloc[:,7+12*i] for i in range(driverAmount)],index=driverInfo['Driver'])
# plotLineChart(ERS_deployed, driverAmount, 'ERS deployment', 'Lap', 'ERS deployed')