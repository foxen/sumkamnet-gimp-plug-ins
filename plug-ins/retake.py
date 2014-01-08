#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SUMKAM.NET
#
# GIMP Python-Fu скрипт обработки изображений
# для каталога товаров.
#
# Считывает файл конфигурации cfgHomeFile.
# Перемещает исходный файл из директории uJpegPath в
# в директорию retakePath/YY-mm-dd/.
# добавляет строку с именем снимка в файл
# retakePath/YY-mm-dd/retake.txt.

from gimpfu import *
import os
import ConfigParser
import datetime
import shutil
#import sys

#err = open(os.path.expanduser("~/sumkamnet/gimp-plug-ins-logs/gimp-plug-ins.error.log"), "a")
#log = open(os.path.expanduser("~/sumkamnet/gimp-plug-ins-logs/gimp-plug-ins.log"), "a")
#sys.stderr = err
#sys.stdout = log

def plugin_func():
 
  cfgHomeFile = ~/sumkamnet/gimp-plug-ins-config/gimp-plug-ins.cfg

  config = ConfigParser.ConfigParser()
  config.read(os.path.expanduser(cfgHomeFile))

  basePath = config.get("Paths","base")

  jpegExtension = basePath + config.get("Extensions","jpeg")
  uJpegPath = basePath + config.get("Paths","uJpeg")
  retakePath = basePath + config.get("Paths","retake")

  now = datetime.datetime.now()
  dateNow = now.strftime("%Y-%m-%d")

  if not os.path.exists(retakePath+dateNow):
    os.makedirs(retakePath+dateNow)

  image = gimp.image_list()[0]

  name = pdb.gimp_image_get_name(image)[0:-4]
  
  shutil.move( uJpegPath + name + jpegExtension, retakePath + dateNow + "/")
  f = open(retakePath + dateNow + "/" + "retake.txt","a+")
  f.write(name + "\n")
  f.close()

  return

register(
          "python-fu-sumkamnet-to-retake", # Имя регистрируемой функции
          "sumkam.net. Marks photo as needed to retaking", # Информация о дополнении
          "Marks photo as needed to retaking", # Короткое описание выполняемых скриптом действий
          "Eugene Polyakov", # Информация об авторе
          "Eugene Polyakov (foxen@foxen.ru)", # Информация о копирайте
          "29.12.2013", # Дата изготовления
          "retake", # Название пункта меню, с помощью которого дополнение будет запускаться
          "*", # Типы изображений, с которыми может работать дополнение
          [],# Параметры, которые будут переданы дополнению
          [],# Список переменных, которые вернет дополнение
          plugin_func, 
          menu="<Image>/SUMKAMNET/")# Имя исходной функции и меню, в которое будет помещён пункт, запускающий дополнение

main()