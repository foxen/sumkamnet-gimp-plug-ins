#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SUMKAM.NET
#
# GIMP Python-Fu скрипт обработки изображений
# для каталога товаров.
#
# Создает из выделения слой.
# Изменяет размер изображения, приводя его к формату 4:3


from gimpfu import *

def plugin_func():
  image = gimp.image_list()[0]
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
  
  return

register(
          "python-fu-sumkamnet-make-layer", # Имя регистрируемой функции
          "sumkam.net. Make layer", # Информация о дополнении
          "Make layer", # Короткое описание выполняемых скриптом действий
          "Eugene Polyakov", # Информация об авторе
          "Eugene Polyakov (foxen@foxen.ru)", # Информация о копирайте
          "28.12.2013", # Дата изготовления
          "make layer", # Название пункта меню, с помощью которого дополнение будет запускаться
          "*", # Типы изображений, с которыми может работать дополнение
          [],# Параметры, которые будут переданы дополнению
          [],# Список переменных, которые вернет дополнение
          plugin_func, 
          menu="<Image>/SUMKAMNET/")# Имя исходной функции и меню, в которое будет помещён пункт, запускающий дополнение

main()