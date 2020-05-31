from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import os
import psutil
import sys
from subprocess import Popen
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
import sqlite3
import pandas as pd
import io
import base64
from io import BytesIO
import matplotlib.pyplot as plt
plt.style.use('ggplot')

"""
pretty awesome styles
# seaborn-darkgrid
# ggplot
# seaborn
# seaborn-paper
# seaborn-notebook
# Solarize_Light2
"""


def home_view(request):
    return "Hello World!"


def geeks_view(request):
    # render function takes argument  - request
    # and return HTML as response
    return render(request, "templates/index.html")


def testlog(request):
    file_map = {
        "dm_report_gen.py": "dm_log",
        "db_refresh.py": "refresh_log",
        "start_bot.py": "auto_insta.log"}

    f_name = file_map.get(request.GET.get('file_name'))
    f_path = os.path.join("..", "auto-insta", f_name)

    # orignal path, DO NO DELETE
    # file_ = open(os.path.join("..", "auto-insta", "auto_insta.log"))
    # file_ = open(os.path.abspath(f_path))
    file_ = open(f_path)
    # return HttpResponse(file_)
    return JsonResponse({'data': file_.readlines()[-100:]})


def bool_running(request):
    process_name = request.GET.get('file_name')
    flag = False
    for process in psutil.process_iter():
        # check if python process & then check if process name == filename
        if (process.name() == 'python' or process.name() == 'python3') and process_name in process.cmdline()[1]:
            print(process)
            print(process.cmdline())
            flag = True
            break
    return JsonResponse({'status': flag})


def get_visual(request):
    f_path = os.path.join("..", "auto-insta", 'auto-insta.db')

    db_conn = sqlite3.connect(f_path)
    bot_foll_df = pd.read_sql(
        "select * from instaDb where bot_lead=1 AND following=1 AND acc_status=1", db_conn)
    hash_df = bot_foll_df.groupby(['hash_tag'], as_index=False).sum()
    hash_df.sort_values("followers", ascending=False, inplace=True)
    hash_df.plot(title="Most Followed hashtags", kind='bar',
                 x='hash_tag', y='followers')
    plt.tight_layout()

    # plt.show()
    figfile = BytesIO()
    plt.savefig(figfile, format='png')

    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(figfile.getvalue()).decode('utf8')

    return JsonResponse({'img': pngImageB64String})


def get_calendar_dates(request):
    f_path = os.path.join("..", "auto-insta", 'auto-insta.db')
    db_conn = sqlite3.connect(f_path)

    if request.GET.get('tab') == 'smart_log':
        log_df = pd.read_sql(
            f"""select session_start from smartlog ORDER BY session_start""", db_conn)
        log_df['session_start'] = pd.to_datetime(
            log_df['session_start']).dt.strftime("%Y-%m-%d")
        dates = list(log_df['session_start'].unique())
        min = log_df['session_start'].min()
        max = log_df['session_start'].max()
    else:
        log_df = pd.read_sql(
            f"""select timestamp from instaDB
            WHERE bot_lead=1 AND (followers=1 OR following=1)
            ORDER BY timestamp""", db_conn)
        log_df['timestamp'] = pd.to_datetime(
            log_df['timestamp']).dt.strftime("%Y-%m-%d")
        dates = list(log_df['timestamp'].unique())
        min = log_df['timestamp'].min()
        max = log_df['timestamp'].max()
    return JsonResponse({'dates': dates, 'min': min, 'max': max})


def get_smart_log(request):
    f_path = os.path.join("..", "auto-insta", 'auto-insta.db')
    db_conn = sqlite3.connect(f_path)
    date = request.GET.get('date', '2020-05-22')

    log_df = pd.read_sql(f"""select * from smartlog
                        where session_start LIKE '{date}%'
                        """, db_conn)

    log_df['session_start'] = pd.to_datetime(
        log_df['session_start']).dt.strftime("%I:%M %p")

    log_df.plot(title="Smart Log", kind='bar', x='session_start',
                y=['delta_followers_cnt', 'delta_following_cnt'], rot=15)
    plt.tight_layout()

    figfile = BytesIO()
    plt.savefig(figfile, format='png')

    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(figfile.getvalue()).decode('utf8')

    return JsonResponse({'img': pngImageB64String})


def get_daily_log(request):
    f_path = os.path.join("..", "auto-insta", 'auto-insta.db')
    db_conn = sqlite3.connect(f_path)
    date = request.GET.get('date', '2020-05-22')

    log_df = pd.read_sql(f"""SELECT * FROM instaDB
                        WHERE timestamp='{date}' AND bot_lead=1
                        AND (followers=1 OR following=1)
                        """, db_conn)
    print(log_df)
    log_df.plot(title="Bot Action", kind='bar', stacked=True,
                x='hash_tag', y=['followers', 'following'], rot=90)

    plt.tight_layout()

    figfile = BytesIO()
    plt.savefig(figfile, format='png')

    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(figfile.getvalue()).decode('utf8')

    return JsonResponse({'img': pngImageB64String})
