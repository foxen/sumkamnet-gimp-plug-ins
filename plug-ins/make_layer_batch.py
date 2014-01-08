#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SUMKAM.NET
#
# GIMP Python-Fu скрипт обработки изображений
# для каталога товаров.
#
# Считывает файл конфигурации cfgHomeFile.
# Последовательно открывает файлы из директории uXcfPath
# Создает из выделения слой.
# Копирует файл в директорию xcfPath.


from gimpfu import *
import os
import ConfigParser
import datetime
import sys

err = open(os.path.expanduser("~/sumkamnet/gimp-plug-ins-logs/gimp-plug-ins.error.log"), "a+")
log = open(os.path.expanduser("~/sumkamnet/gimp-plug-ins-logs/gimp-plug-ins.log"), "a+")
sys.stderr = err
sys.stdout = log

def plugin_func(cfgHomeFile):
  cfgHomeFile = "~/sumkamnet/gimp-plug-ins-config/gimp-plug-ins.cfg"

  config = ConfigParser.ConfigParser()
  config.read(os.path.expanduser(cfgHomeFile))

  logPath = config.get("Paths","log")
  now = datetime.datetime.now()
  logFile = open(logPath+now.strftime("%Y-%m-%d")+".make-layer.log","a+")

  basePath = config.get("Paths","base")

  uXcfPath = basePath + config.get("Paths","uXcf")
  xcfPath = basePath + config.get("Paths","xcf")
  xcfExtension = config.get("Extensions","xcf")

  for root, dirs, files in os.walk(uXcfPath):
    for name in files:
      if name.endswith(xcfExtension):
        image = pdb.gimp_xcf_load(0, uXcfPath+ name, name)
        layer = image.layers[0]
        pdb.gimp_edit_named_copy(layer,"cp")
        floating_sel = pdb.gimp_edit_named_paste(layer,"cp",False)
        pdb.gimp_buffer_delete("cp")
        pdb.gimp_floating_sel_to_layer(floating_sel)
        pdb.gimp_image_remove_layer(image, layer)
        layer = image.layers[0]
        pdb.gimp_image_resize_to_layers(image)
        width = pdb.gimp_drawable_width(layer)
        height = pdb.gimp_drawable_height(layer)
        
        if width > height*0.75:
          heightN = int(round(width*1.1/3))*4
        else:
          heightN = round(float(height + height*0.1)/4)*4
        
        widthN = heightN*0.75
        offY = int((heightN - height)/2)
        offX = int((widthN - width)/2)
        pdb.gimp_image_resize(image, widthN, heightN, offX, offY)
        pdb.gimp_file_save(image, image.layers[0], xcfPath + name, name)
        pdb.gimp_image_delete(image)
        now = datetime.datetime.now()
        logFile.write(now.strftime("%H:%M:%S")+";"+uXcfPath+";"+xcfPath+";"+name+"\n")
        
  logFile.close()
  return

register(
          "python-fu-sumkamnet-make-layer-batch", # Имя регистрируемой функции
          "sumkam.net. Make layers in batch mode", # Информация о дополнении
          "Make layers in batch mode", # Короткое описание выполняемых скриптом действий
          "Eugene Polyakov", # Информация об авторе
          "Eugene Polyakov (foxen@foxen.ru)", # Информация о копирайте
          "28.12.2013", # Дата изготовления
          "make layer batch", # Название пункта меню, с помощью которого дополнение будет запускаться
          "", # Типы изображений, с которыми может работать дополнение
          [
          (PF_STRING,"cfgHomeFile", "path to config", ~/sumkamnet/gimp-plug-ins-config/gimp-plug-ins.cfg)
          ],# Параметры, которые будут переданы дополнению
          [],# Список переменных, которые вернет дополнение
          plugin_func, 
          menu="<Image>/SUMKAMNET/")# Имя исходной функции и меню, в которое будет помещён пункт, запускающий дополнение

main()