import requests
from bs4 import BeautifulSoup
import datetime
import pytz

def get_API(nx, ny):
    currentdate = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%Y%m%d')
    currenthour = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%H')
    currentminute = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%M')

    if int(currentminute) >= 30:
        pass
    elif int(currentminute) < 30:
        currenthour = int(currenthour) - 1
    if len(str(currenthour)) < 2:
        currenthour = "0" + str(currenthour)


    URI = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst?"
    serviceKey = "oH7Ka3pHFV6tlkknSOGHpi5zCFaWyWUHC1MXmLCrwosu5D%2Bw9Xun%2BI25lqyLs4Vhls178qpID%2B2WNWB%2F6h%2Bywg%3D%3D"
    base_date = "base_date=" + str(currentdate)
    base_time = "&base_time=" + str(currenthour) + "00"
    numOfRows = "&numOfRows=10"
    pageNo = "&pageNo=1"
    Service = "&ServiceKey=" + str(serviceKey)
    URI = URI + base_date + base_time + nx + ny + numOfRows + pageNo + Service
    return URI

def ITEMLIST(Itemlist, weather):
    for item in Itemlist:
        basedate = item.find('basedate').text #발표일자
        basetime = item.find('basetime').text #발표시각
        category = item.find("category").text #날씨코드
        obsValue = item.find("obsrvalue").text

        if category == "PTY": #강수형태
            # (없음(0), 비(1), 비 / 눈(2), 눈(3), 소나기(4) 여기서 비 / 눈은 비와 눈이 섞여 오는 것을 의미 (진눈개비))
            obsValue = item.find("obsrvalue").text
            weather.append('강수형태')
            if obsValue == '0':
                weather.append('없음')
            elif obsValue == '1':
                weather.append('진눈개비')
            elif obsValue == '2':
                weather.append('눈')
            elif obsValue == '3':
                weather.append('소나기')
        elif category == "REH": #습도
            obsValue = item.find("obsrvalue").text
            weather.append('습도')
            weather.append(obsValue + '%')
        elif category == "RN1": #1시간 강우량
            obsValue = item.find("obsrvalue").text
            weather.append('강우량')
            weather.append(obsValue + 'mm')
        elif category == "T1H": #기온
            obsValue = item.find("obsrvalue").text
            weather.append('기온')
            weather.append(obsValue + 'C')
        elif category == "WSD": #풍속
            obsValue = item.find("obsrvalue").text
            weather.append('풍속')
            weather.append(obsValue + 'm/s')
        else:
            continue
    return weather, basedate, basetime


location = [['60', '127'], #서울
            ['98', '76'], #부산
            ['89', '90'], #대구
            ['55', '124'], #인천
            ['58', '74'], #광주
            ['67', '100'], #대전
            ['102', '84'], #울산
            ['60', '120'], #경기도
            ['73', '134'], #강원도
            ['69', '107'], #충북
            ['68', '100'], #충남
            ['63', '89'], #전북
            ['51', '67'], #전남
            ['89', '91'], #경북
            ['91', '77'], #경남
            ['52', '38'], #제주
            ['66', '103'], #세종
            ]
place = []

for i in range(len(location)):
    xx = "&nx="
    yy = "&ny="
    area = location[i]
    nx = xx + area[0]
    ny = yy + area[1]
    URI = get_API(nx, ny)
    response = requests.get(URI)
    soup = BeautifulSoup(response.text, 'html.parser')
    Itemlist = soup.findAll('item')
    weather = []
    weather, basedate, basetime = ITEMLIST(Itemlist, weather)
    place.append(weather)
place.insert(0, basedate)
place.insert(1, basetime)



weather_place = {
    'date' : place[0],
    'time' : place[1],
    'seoul': place[2],
    'busan': place[3],
    'daegu': place[4],
    'incheon': place[5],
    'gwangju': place[6],
    'daejeon': place[7],
    'ulsan': place[8],
    'gyeonggi': place[9],
    'gangwon': place[10],
    'chungbuk': place[11],
    'chungnam': place[12],
    'jeonbuk': place[13],
    'jeonnam': place[14],
    'gyeongbuk': place[15],
    'gyeongnam': place[16],
    'jeju': place[17],
    'sejong': place[18]
}

for i in weather_place.items():
    print(i)



