#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SUMKAM.NET
#
# GIMP Python-Fu скрипт обработки изображений
# для каталога товаров.
#
# Считывает файл конфигурации cfgHomeFile.
# Сохраняет изображение в формате JPEG в пяти размерах, 
# с белым фоном и увеличением резкости,
# в соответствующие директории.
# Удаляет метаданные в экспортированном JPEG файле.

from gimpfu import *
import os

import ConfigParser

import sys

err = open(os.path.expanduser("~/sumkamnet/gimp-plug-ins-logs/gimp-plug-ins.error.log"), "a+")
log = open(os.path.expanduser("~/sumkamnet/gimp-plug-ins-logs/gimp-plug-ins.log"), "a+")
sys.stderr = err
sys.stdout = log

def plugin_func():
  cfgHomeFile = "~/sumkamnet/gimp-plug-ins-config/gimp-plug-ins.cfg"
  config = ConfigParser.ConfigParser()
  config.read(os.path.expanduser(cfgHomeFile))

  basePath = config.get("Paths","base")

  jpegPath = basePath + config.get("Paths","jpeg")
  jpegLpath = basePath + config.get("Paths","jpegL")
  jpegMpath = basePath + config.get("Paths","jpegM")
  jpegSpath = basePath + config.get("Paths","jpegS")
  jpegXsPath = basePath + config.get("Paths","jpegXs")

  heightL = config.getint("Heights","l")
  heightM = config.getint("Heights","m")
  heightS = config.getint("Heights","s")
  heightXs = config.getint("Heights","xs")

  jpegCompress = config.getfloat("JpegParams","compress")
  jpegSaturation = config.getfloat("JpegParams","saturation")
  jpegSharpen = config.getfloat("JpegParams","sharpen")
  
      
  image = gimp.image_list()[0]

  layer = image.layers[0]
  pdb.gimp_layer_resize_to_image_size(layer)
  name = pdb.gimp_image_get_name(image)[0:-4]
  nameJpg = name+".jpg"

  layer = pdb.gimp_layer_new(image, 10, 10, 1, "s", 1, 0)
  pdb.gimp_image_insert_layer(image, layer, None, 2)
  pdb.gimp_layer_resize_to_image_size(layer)
  
  pdb.gimp_drawable_fill(layer, 2)

  layer = pdb.gimp_image_merge_visible_layers(image, 0)
  pdb.gimp_hue_saturation(layer, 0, 0, 0, jpegSaturation)

  imageD = pdb.gimp_image_duplicate(image)
  layerD = imageD.layers[0]

  pdb.plug_in_sharpen(imageD, layerD, jpegSharpen)
  pdb.file_jpeg_save(imageD,layerD,jpegPath+nameJpg,nameJpg,jpegCompress,0.1,1,1,"",0,0,0,1)

  pdb.gimp_image_delete(imageD)
  imageD = pdb.gimp_image_duplicate(image)
  layerD = imageD.layers[0]

  pdb.gimp_image_scale_full(imageD, heightL*0.75, heightL,1)
  pdb.plug_in_sharpen(imageD, layerD, jpegSharpen) 
  pdb.file_jpeg_save(imageD,layerD,jpegLpath+nameJpg,nameJpg,jpegCompress,0.1,1,1,"",0,0,0,0)

  pdb.gimp_image_delete(imageD)
  imageD = pdb.gimp_image_duplicate(image)
  layerD = imageD.layers[0]

  pdb.gimp_image_scale_full(imageD, heightM*0.75, heightM,1)
  pdb.plug_in_sharpen(imageD, layerD, jpegSharpen)
  pdb.file_jpeg_save(imageD,layerD,jpegMpath+nameJpg,nameJpg,jpegCompress,0.1,1,1,"",0,0,0,0)

  pdb.gimp_image_delete(imageD)
  imageD = pdb.gimp_image_duplicate(image)
  layerD = imageD.layers[0]

  pdb.gimp_image_scale_full(imageD, heightS*0.75, heightS,1)
  pdb.plug_in_sharpen(imageD, layerD, jpegSharpen)
  pdb.file_jpeg_save(imageD,layerD,jpegSpath+nameJpg,nameJpg,jpegCompress,0.1,1,1,"",0,0,0,0)

  pdb.gimp_image_delete(imageD)
  imageD = pdb.gimp_image_duplicate(image)
  layerD = imageD.layers[0]

  pdb.gimp_image_scale_full(imageD, heightXs*0.75, heightXs,1)
  pdb.plug_in_sharpen(imageD, layerD, jpegSharpen)
  pdb.file_jpeg_save(imageD,layerD,jpegXsPath+nameJpg, nameJpg,jpegCompress,0.1,1,1,"",0,0,0,0)

  pdb.gimp_image_delete(imageD)

  os.system(" exiftool -all= " + jpegPath + nameJpg)
  os.system("rm " + jpegPath + "/*.jpg_original")

  os.system(" exiftool -all= " + jpegLpath + nameJpg)
  os.system("rm " + jpegLpath + "/*.jpg_original")

  os.system(" exiftool -all= " + jpegMpath + nameJpg)
  os.system("rm " + jpegMpath + "/*.jpg_original")

  os.system(" exiftool -all= " + jpegSpath + nameJpg)
  os.system("rm " + jpegSpath + "/*.jpg_original")

  os.system(" exiftool -all= " + jpegXsPath + nameJpg)
  os.system("rm " + jpegXsPath + "/*.jpg_original")

  return

register(
          "python-fu-sumkamnet-to-jpg", # Имя регистрируемой функции
          "sumkam.net. Save xcf into jpg with preconfigured sizes", # Информация о дополнении
          "Save xcf into jpg with preconfigured sizes", # Короткое описание выполняемых скриптом действий
          "Eugene Polyakov", # Информация об авторе
          "Eugene Polyakov (foxen@foxen.ru)", # Информация о копирайте
          "30.12.2013", # Дата изготовления
          "to jpg", # Название пункта меню, с помощью которого дополнение будет запускаться
          "", # Типы изображений, с которыми может работать дополнение
          [],# Параметры, которые будут переданы дополнению
          [],# Список переменных, которые вернет дополнение
          plugin_func, 
          menu="<Image>/SUMKAMNET/")# Имя исходной функции и меню, в которое будет помещён пункт, запускающий дополнение

main()