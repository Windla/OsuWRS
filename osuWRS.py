# coding = uft-8
import urllib.request  # 网站读取
import win32api  # 启动游戏
import os  # 杀死游戏
import time  # 降低占用

print("OsuWRS作者: B站 @Wind_la\nOsuWRS版本: 2.0.1\n")
print("少女祈祷中\n正在为您检测更新\n模式: 速度优先\n\n如果该界面长时间没有自动退出[请检查您的网络]\n")

# 配置文件读取
with open("config.ini", 'r') as f:
    Path = f.read()  # osu 路径
    f.close()
osuPath = Path + "\\osu!.exe"  # osu.exe 路径  |  去tm的转译字符.jpg
bgPath = Path + "\\Data\\bg"  # bg文件夹 路径

# 启动osu  |  非常激进的做法,但是可以减少启动时间
win32api.ShellExecute(0, 'open', osuPath, '', '', 1)

# 检测ppy变化  |  数据类型: bin
ppyUrl = urllib.request.urlopen("https://osu.ppy.sh/web/osu-getseasonal.php").read()  # ppy数据
with open("bg.php", 'r') as f:  # 原数据
    ppyUrlOld = (f.read()).encode()
    f.close()

# 数据变化判断
if ppyUrl != ppyUrlOld:  # seasonal background 更新后开始进行 bg更新
    # 杀死osu 当前启动的osu
    os.system("taskkill /F /IM osu!.exe")
    # 删除旧图&开放权限
    os.system('2_update.bat')

    #
    # ---------------------  手动拉取更新 -----------------------------
    #

    # bg文件夹更新时间
    bgOldTime = os.path.getmtime(bgPath)
    bgNewTime = os.path.getmtime(bgPath)
    # 拉起osu
    win32api.ShellExecute(0, 'open', osuPath, '', '', 1)

    # 监测更新
    while bgOldTime == bgNewTime:
        bgNewTime = os.path.getmtime(bgPath)
        print("bg文件夹更新时间:", bgNewTime, "没有变化?[请检查网络 或 反复进入游戏选铺界面]")
        time.sleep(1)

    # 杀死osu
    os.system("taskkill /F /IM osu!.exe")
    # 开始替换
    os.system('1_replace.bat')  # 重复锁定警告!
    # 将新数据写入bg.php
    with open("bg.php", "wb") as f:
        f.write(ppyUrl)
    # 启动osu(替换成功后)
    win32api.ShellExecute(0, 'open', osuPath, '', '', 1)
    print("更新成功!")
else:
    print("本次检测无更新\n正在为您打开osu!\n祝您愉快!")
