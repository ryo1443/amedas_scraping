# -*- coding: utf-8 -*-
import os
import datetime
import csv
import urllib.request
from bs4 import BeautifulSoup

def str2float(weather_data):
    try:
        return float(weather_data)
    except:
        return 0

def scraping(url, date):

    # 気象データのページを取得
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    trs = soup.find("table", { "class" : "data2_s" })

    data_list_per_hour = []

    # table の中身を取得
    for tr in trs.findAll('tr')[2:]:
        tds = tr.findAll('td')

        if tds[1].string == None:
            break;

        data_list = [
            date,
            tds[0].string,
            str2float(tds[4].string),  # 気温
            str2float(tds[3].string),  # 降水量
            str2float(tds[7].string)   # 湿度
        ]

        data_list_per_hour.append(data_list)

    return data_list_per_hour

def create_csv():
    # CSV 出力先ディレクトリ
    output_dir = r"C:\\Users\\hrdafrst\\Downloads\\金澤亮"

    # 出力ファイル名
    output_file = "weather.csv"

    # データ取得開始・終了日
    start_date = datetime.date(1990, 1, 1)
    end_date   = datetime.date(2019, 7, 8)

    #end_date   = datetime.date(2019, 7, 8)

    # CSV の列
    fields = ["年月日", "時間", "気温", "降水量", "湿度"]

    with open(os.path.join(output_dir, output_file), 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

        date = start_date
        while date <= end_date:

            # 対象url（今回は東京）
            url = "http://www.data.jma.go.jp/obd/stats/etrn/view/hourly_s1.php?" \
                  "prec_no=82&block_no=47807&year=%d&month=%d&day=%d&view="%(date.year, date.month, date.day)

            data_per_day = scraping(url, date)

            for dpd in data_per_day:
                writer.writerow(dpd)

            date += datetime.timedelta(1)

if __name__ == '__main__':
    create_csv()
