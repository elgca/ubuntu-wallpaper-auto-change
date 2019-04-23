#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
try:
    import configparser as cparser
except ImportError:
    import ConfigParser as cparser
    reload(sys)
    sys.setdefaultencoding( "utf-8" )
import time
import traceback
#config:
#默认配置路径
#该路径下包含一个config文件，内容格式为ini。
#包含"Path":"Download"(图片路径)和
#"Slide":"freeze"（切换壁纸间隔，整数,单位秒，可选默认:1）
defalut_config_path=os.path.expanduser('~') + "/" + ".config/lovewallpaper/config"
#默认图片文件夹
#当config文件不存在或无法读取时候使用，这里使用用户目录下的'图片'文件夹
default_wallpaper_path = os.path.expanduser('~') + "/图片"
background_path = os.path.expanduser('~') + '/.background.xml'
#输出结果到控制台
#在程序结束时候将记录信息输出到控制台
#本程序只有当出现错误时候会记录日志信息
out_to_console=False
#日志记录路径
log_file_path = os.path.expanduser('~') + "/wallpaper.auto.change.log"

class TextArea(object):
    def __init__(self,default):
        self.buffer = []
        self.stdout = default
    def write(self, *args, **kwargs): 
        self.buffer.append(" ".join(args))
    def save(self,path,mode = 'a+'):
        with open(path,mode) as log:
            for info in self.buffer:
                log.write(info)
    def write_to_default(self):
        for info in sys.stdout.buffer:
            self.stdout.write(info)
    def clear(self):
        pass
    def show(self):
        pass
    def close(self):
        pass
    def flush(self):
        pass

class ConfigSave(object):
    def __init__(self,path_):
        self.toSave = False
        self.path = path_
        self.bgp = os.path.join(os.path.split(path_)[0],".wtmp")
        self.buffer = []
        self.config = cparser.ConfigParser()
        self.config.read(config_path)

    def getConfig(self,section,option,default_value,func = lambda x:x):
        try:
            res = self.config.get(section, option)
            if res == "":
                self.toSave = True
                res = default_value
            res = func(res)
        except Exception as e:
            self.toSave = True
            res = default_value
        print(not self.toSave,section,option,default_value,str(res))
        self.buffer.append((section,option,str(res)))
        return res

    def compareWith(self,section,option,value,default,replace = True):
        try:
            res = self.config.get(section, option)
            if res == "":
                self.toSave = True
                res = default
        except Exception as e:
            self.toSave = True
            res = default
        print(not self.toSave,section,option,default,str(res))
        res = value == res
        if replace and not res:
            self.toSave = True
            self.buffer.append((section,option,value))
        return res

    def set_save(self,flag):
        self.toSave = flag

    def save(self):
        if self.toSave:
            sections = self.config.sections()
            for section,option,value in self.buffer:
                if not section in sections:
                    self.config.add_section(section)
                print("reset config:",section,option,value)
                self.config.set(section, option, value)
            self.config.write(open(self.path, "w")) 

    def tcg(self,cmp):
        res = False
        with open(self.bgp,'a+') as f:
            f.seek(0,0)
            p = f.read()
            print(p,cmp)
            res = p == cmp
        if not res:
            with open(self.bgp,'w') as f:
                f.write(cmp)
        return not res
    def deltcg(self):
        os.remove(self.bgp)
#logging out put:
sys.stdout=TextArea(sys.stdout)
print(sys.version_info)
l_format = ['jpg','jpeg','png','bmp']
print('start time: ' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
try:
    config_save = False
    config_path = defalut_config_path
    if not os.path.exists(config_path):
        raise Exception("config path: \"%s\",not exists" % config_path)
    #get config from config file
    config_cf = ConfigSave(config_path)
    wallpaper_path = config_cf.getConfig("Path", "Download",default_wallpaper_path)
    freeze = config_cf.getConfig("Slide", "freeze",1,lambda x: int(x))
    static = config_cf.getConfig("Slide", "static",str(55.0))
    transition = config_cf.getConfig("Slide", "transition",str(5.0))   
    config_cf.save()
    if not os.path.exists(wallpaper_path):
        raise Exception("wallpaper path: \"%s\",not exists" % wallpaper_path)
    print("wallpaper path is:" + wallpaper_path)
    dfc=os.popen("gsettings get org.gnome.desktop.background picture-uri").read().replace('\n','')
    print('picture-uri: ' + dfc)
    last_time = "-".join([str(int(os.path.getmtime(x))) for x in [wallpaper_path,config_path]])
    if[x for x in l_format if x in dfc] == [] and os.path.exists(background_path) and not config_cf.tcg(last_time):
        print("wallpaper info not modify")
        sys.exit(0)
    print('wallpaper modify,rebuild background.xml')
    print ("freeze is: %s ;path is: %s;file list:" % (freeze,wallpaper_path))
    files = []
    for p,d,f in os.walk(wallpaper_path):
        for myfile in f:
            if myfile.split(".")[-1].lower() in l_format:
                file_path = os.path.join(p, myfile)
                print('    ' + file_path)
                files.append(file_path)
    if files:
        print("new background.xml")
        from Plugin.Ubuntu import AutoSlide
        AutoSlide(background_path).BeginSlide(files, (static,transition))
    print("success update")
except Exception as e:
    os.system("which python")
    exstr = traceback.format_exc()
    print(exstr)
    print('')
    print("failure update")
    sys.stdout.save(log_file_path)
finally:
    if out_to_console:
        sys.stdout.write_to_default()
