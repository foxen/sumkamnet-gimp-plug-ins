#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SUMKAM.NET
#
# GIMP Python-Fu скрипт обработки изображений
# для каталога товаров
#
# Считывает файл конфигурации cfgHomeFile.
# Открывает первый jpeg файл в директории uJpgPath.
# Разворачивает изображение.
# Выводит изображение в окно GIMP для последующей обтравки контура.


from gimpfu import *
import os
import ConfigParser
#import sys

#err = open(os.path.expanduser("~/sumkamnet/gimp-plug-ins.error.log"), "a")
#log = open(os.path.expanduser("~/sumkamnet/gimp-plug-ins.log"), "a")
#sys.stderr = err
#sys.stdout = log

def plugin_func():
  cfgHomeFile = "~/sumkamnet/gimp-plug-ins.cfg"

  #pluginLog = open(os.path.expanduser("~/sumkamnet/gimp-plug-ins.plugin.log"), "a")
  #pluginLog.write("pen-plugin\n")

  config = ConfigParser.ConfigParser()
  config.read(os.path.expanduser(cfgHomeFile))

  uJpgPath = config.get("Paths","uJpgPath")
  jpegExtension = config.get("Extension","jpegExtension")
  
  fileName = ""
  fileList = []

  for root, dirs, files in os.walk(uJpgPath):
    for name in files:
      if name.endswith(jpegExtension):
        fileList.append(name)
  if len(fileList) > 0:
    fileList.sort()
    fileName = fileList[0]
  else:
    return None
  
  image = pdb.file_jpeg_load(uJpgPath+fileName, fileName)
  pdb.gimp_image_rotate(image, 2)
  display = pdb.gimp_display_new(image)
  
  enabled = pdb.gimp_image_undo_enable(image)
  return 

register(
          "python-fu-sumkamnet-open-rotate", # Имя регистрируемой функции
          "sumkam.net. Open, rotate unreclaimed jpeg file", # Информация о дополнении
          "Open, rotate unreclaimed jpeg file", # Короткое описание выполняемых скриптом действий
          "Eugene Polyakov", # Информация об авторе
          "Eugene Polyakov (foxen@foxen.ru)", # Информация о копирайте
          "28.12.2013", # Дата изготовления
          "open and rotate", # Название пункта меню, с помощью которого дополнение будет запускаться
          "", # Типы изображений, с которыми может работать дополнение
          [],# Параметры, которые будут переданы дополнению
          [],# Список переменных, которые вернет дополнение
          plugin_func, 
          menu="<Image>/SUMKAMNET/")# Имя исходной функции и меню, в которое будет помещён пункт, запускающий дополнение

main()