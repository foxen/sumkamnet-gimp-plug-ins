#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SUMKAM.NET
#
# GIMP Python-Fu скрипт обработки изображений
# для каталога товаров.
#
# Считывает файл конфигурации cfgHomeFile.
# Парсит имя файла и, если требуется, меняет формат строки имени
# Сохраняет открытый jpeg файл с обтравленным фоном
# в формате xcf в директорию xcfPath.
# Перемещает исходный jpeg файл из директории uJpegPath 
# в директорию srcJpegPath.


from gimpfu import *
import os
import shutil
import ConfigParser

def plugin_func():
  cfgHomeFile = ~/sumkamnet/gimp-plug-ins-config/gimp-plug-ins.cfg

  config = ConfigParser.ConfigParser()
  config.read(os.path.expanduser(cfgHomeFile))

  basePath = config.get("Paths","base")

  uJpegPath = basePath + config.get("Paths","uJpeg")
  uXcfPath = basePath + config.get("Paths","uXcf")
  srcJpegPath = basePath + config.get("Paths","srcJpeg")
  xcfExtension = basePath + config.get("Extensions","xcf")

  image = gimp.image_list()[0]

  name = pdb.gimp_image_get_name(image)[0:-4]

  if name[0:1] == "!":
    name = name[1:] + "-1"

  if name[0:2] == "1-":
    name = name[2:] + "-1"
  
  pdb.gimp_file_save(image, image.layers[0], uXcfPath + name + xcfExtension, name + xcfExtension)

  shutil.move( uJpegPath + pdb.gimp_image_get_name(image), srcJpegPath)

  return

register(
          "python-fu-sumkamnet-save-xcf", # Имя регистрируемой функции
          "sumkam.net. Save jpeg file into xcf", # Информация о дополнении
          "Save jpeg file into xcf", # Короткое описание выполняемых скриптом действий
          "Eugene Polyakov", # Информация об авторе
          "Eugene Polyakov (foxen@foxen.ru)", # Информация о копирайте
          "28.12.2013", # Дата изготовления
          "save xcf", # Название пункта меню, с помощью которого дополнение будет запускаться
          "*", # Типы изображений, с которыми может работать дополнение
          [],# Параметры, которые будут переданы дополнению
          [],# Список переменных, которые вернет дополнение
          plugin_func, 
          menu="<Image>/SUMKAMNET/")# Имя исходной функции и меню, в которое будет помещён пункт, запускающий дополнение

main()