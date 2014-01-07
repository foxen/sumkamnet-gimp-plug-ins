#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SUMKAM.NET
#
# GIMP Python-Fu скрипт обработки изображений
# для каталога товаров.
#
# Считывает файл конфигурации cfgHomeFile.
# Увеличивает контраст на значение val.


from gimpfu import *
import os
import ConfigParser

def plugin_func():
  cfgHomeFile = "~/sumkamnet/gimp-plug-ins.cfg"

  config = ConfigParser.ConfigParser()
  config.read(os.path.expanduser(cfgHomeFile))

  val = config.getint("Contrast","hard")

  image = gimp.image_list()[0]

  drawable = pdb.gimp_image_get_active_drawable(image)
  pdb.gimp_brightness_contrast(drawable, 0, val)

  return

register(
          "python-fu-sumkamnet-contrast-hard", # Имя регистрируемой функции
          "sumkam.net. Increases contrast on preconfigured value", # Информация о дополнении
          "Contrast hard", # Короткое описание выполняемых скриптом действий
          "Eugene Polyakov", # Информация об авторе
          "Eugene Polyakov (foxen@foxen.ru)", # Информация о копирайте
          "29.12.2013", # Дата изготовления
          "contrast hard", # Название пункта меню, с помощью которого дополнение будет запускаться
          "*", # Типы изображений, с которыми может работать дополнение
          [],# Параметры, которые будут переданы дополнению
          [],# Список переменных, которые вернет дополнение
          plugin_func, 
          menu="<Image>/SUMKAMNET/")# Имя исходной функции и меню, в которое будет помещён пункт, запускающий дополнение

main()