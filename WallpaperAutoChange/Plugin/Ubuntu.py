# -*- coding: utf-8 -*-

from xml.dom.minidom import Document
import os
import random

#咳咳，类的名字不要改变，函数名称也不要改变，下面三个参数会自动传入
#path是传过来的图片所在的文件夹
#key是用户操作的图片的名字
#files是path目录下的所有文件

class WallpaperSetter:
    """docstring for WallpaperSetter"""
    def __init__(self):
        pass

    def setWallpaper(self, path, key):
        os.system( "gsettings set org.gnome.desktop.background picture-uri \"file://%s/%s.jpg\""%(path, key))

    
    def puresetWallpaper(self, url):
        os.system( "gsettings set org.gnome.desktop.background picture-uri \"file://%s\""%(url))


class AutoSlide:
    """docstring for AutoSlide"""
    def __init__(self,path = os.path.expanduser('~') + "/.background.xml"):
        self.xml = path

    def BeginSlide(self, files,time):
        doc = Document()

        background = doc.createElement("background")
        doc.appendChild(background)

        starttime = doc.createElement("starttime")
       
        year = doc.createElement("year")
        year_text = doc.createTextNode("2009")
        year.appendChild(year_text)

        month = doc.createElement("month")
        month_text = doc.createTextNode("08")
        month.appendChild(month_text)

        day = doc.createElement("day")
        day_text = doc.createTextNode("04")
        day.appendChild(day_text)

        hour = doc.createElement("hour")
        hour_text = doc.createTextNode("00")
        hour.appendChild(hour_text)

        minute = doc.createElement("minute")
        minute_text = doc.createTextNode("00")
        minute.appendChild(minute_text)

        second = doc.createElement("second")
        second_text = doc.createTextNode("00")
        second.appendChild(second_text)

        starttime.appendChild(year)
        starttime.appendChild(month)
        starttime.appendChild(day)
        starttime.appendChild(hour)
        starttime.appendChild(minute)
        starttime.appendChild(second)

        background.appendChild(starttime)

        static_time, transition_time = time
        trans_files = files+[files[0]]
        trans_files.pop(0)
        files=zip(files,trans_files)
        for begin,end in files:
            static = doc.createElement("static")

            file_static = doc.createElement("file")
            file_static.appendChild(doc.createTextNode(begin))

            static_duration = doc.createElement("duration")
            static_duration.appendChild(doc.createTextNode(static_time))

            static.appendChild(static_duration)
            static.appendChild(file_static)
            background.appendChild(static)

            transition = doc.createElement("transition")

            transition_duration = doc.createElement("duration")
            transition_duration.appendChild(doc.createTextNode(transition_time))

            from_ = doc.createElement("from")
            from_.appendChild(doc.createTextNode(begin))

            to_ = doc.createElement("to")
            to_.appendChild(doc.createTextNode(end))

            transition.appendChild(transition_duration)
            transition.appendChild(from_)
            transition.appendChild(to_)

            background.appendChild(transition)
        self.createfile(background)
            
    def createfile(self,result):
                background = open(self.xml,'w')
                background.write(result.toprettyxml(indent="  "))
                background.close()
                os.system("gsettings set org.gnome.desktop.background picture-uri 'file:///"+self.xml + "'")

    def RandomSet(self,files):      
                                    
        mymax = len(files) - 1
        num = random.randint(0,mymax)
        wallpeper = files[num] 

        os.system("gsettings set org.gnome.desktop.background picture-uri 'file:///"+wallpeper+"'")

