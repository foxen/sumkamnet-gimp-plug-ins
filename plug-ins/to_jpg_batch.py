#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SUMKAM.NET
#
# GIMP Python-Fu скрипт обработки изображений
# для каталога товаров.
#
# Считывает файл конфигурации cfgHomeFile.
# Последовательно открывает файлы из директории uXcfPath и
# и экспортирует содержимое в четыре размера с белым фоном
# в соответствующие директории. Удаляет обработанные файлы из
# директории uXcfPath

from gimpfu import *
import os

import ConfigParser
import sys
import datetime
import shutil

err = open(os.path.expanduser("~/sumkamnet/gimp-plug-ins-logs/gimp-plug-ins.error.log"), "a+")
log = open(os.path.expanduser("~/sumkamnet/gimp-plug-ins.log"), "a+")
sys.stderr = err
#sys.stdout = log

def plugin_func(cfgHomeFile):

  print cfgHomeFile
  config = ConfigParser.ConfigParser()
  config.read(os.path.expanduser(cfgHomeFile))

  logPath = config.get("Paths","logPath")
  now = datetime.datetime.now()
  logFile = open(logPath+now.strftime("%Y-%m-%d")+".to_jpg.log","a+")

  uXcfPath = config.get("Paths","uXcfPath")
  xcfPath = config.get("Paths","xcfPath")
  xcfExtension = config.get("Extension","xcfExtension")
  
  jpgPath = config.get("Paths","jpgPath")
  jpgLpath = config.get("Paths","jpgLpath")
  jpgMpath = config.get("Paths","jpgMpath")
  jpgSpath = config.get("Paths","jpgSpath")
  jpgXsPath = config.get("Paths","jpgXsPath")

  heightL = config.getint("Heights","l")
  heightM = config.getint("Heights","m")
  heightS = config.getint("Heights","s")
  heightXs = config.getint("Heights","xs")

  jpegCompress = config.getfloat("JpegParams","compress")
  jpegSaturation = config.getfloat("JpegParams","saturation")
  jpegSharpen = config.getfloat("JpegParams","sharpen")
  jpegSmoothing = config.getfloat("JpegParams","smoothing")


  uFiles = []

  for root, dirs, files in os.walk(uXcfPath):
    for name in files:
      if name.endswith(xcfExtension):
        image = pdb.gimp_xcf_load(0, uXcfPath + name, name)

        layer = image.layers[0]
        pdb.gimp_layer_resize_to_image_size(layer)
        
        nameJpg = name[0:-4]+".jpg"

        layer = pdb.gimp_layer_new(image, 10, 10, 1, "s", 1, 0)
        pdb.gimp_image_insert_layer(image, layer, None, 2)
        pdb.gimp_layer_resize_to_image_size(layer)
        
        pdb.gimp_drawable_fill(layer, 2)

        layer = pdb.gimp_image_merge_visible_layers(image, 0)

        pdb.gimp_hue_saturation(layer, 0, 0, 0, jpegSaturation)

        imageD = pdb.gimp_image_duplicate(image)
        layerD = imageD.layers[0]

        pdb.plug_in_sharpen(imageD, layerD, jpegSharpen)
        pdb.file_jpeg_save(imageD,layerD,jpgPath+nameJpg,nameJpg,jpegCompress,jpegSmoothing,1,1,"",0,0,0,1)

        pdb.gimp_image_delete(imageD)
        imageD = pdb.gimp_image_duplicate(image)
        layerD = imageD.layers[0]

        pdb.gimp_image_scale_full(imageD, heightL*0.75, heightL,1)
        pdb.plug_in_sharpen(imageD, layerD, jpegSharpen) 
        pdb.file_jpeg_save(imageD,layerD,jpgLpath+nameJpg,nameJpg,jpegCompress,jpegSmoothing,1,1,"",0,0,0,0)

        pdb.gimp_image_delete(imageD)
        imageD = pdb.gimp_image_duplicate(image)
        layerD = imageD.layers[0]

        pdb.gimp_image_scale_full(imageD, heightM*0.75, heightM,1)
        pdb.plug_in_sharpen(imageD, layerD, jpegSharpen)
        pdb.file_jpeg_save(imageD,layerD,jpgMpath+nameJpg,nameJpg,jpegCompress,jpegSmoothing,1,1,"",0,0,0,0)

        pdb.gimp_image_delete(imageD)
        imageD = pdb.gimp_image_duplicate(image)
        layerD = imageD.layers[0]

        pdb.gimp_image_scale_full(imageD, heightS*0.75, heightS,1)
        pdb.plug_in_sharpen(imageD, layerD, jpegSharpen)
        pdb.file_jpeg_save(imageD,layerD,jpgSpath+nameJpg,nameJpg,jpegCompress,jpegSmoothing,1,1,"",0,0,0,0)

        pdb.gimp_image_delete(imageD)
        imageD = pdb.gimp_image_duplicate(image)
        layerD = imageD.layers[0]

        pdb.gimp_image_scale_full(imageD, heightXs*0.75, heightXs,1)
        pdb.plug_in_sharpen(imageD, layerD, jpegSharpen)
        pdb.file_jpeg_save(imageD,layerD,jpgXsPath+nameJpg, nameJpg,jpegCompress,jpegSmoothing,1,1,"",0,0,0,0)

        pdb.gimp_image_delete(imageD)
        
        pdb.gimp_image_delete(image)

        logFile.write(now.strftime("%H:%M:%S")+";"+xcfPath+";"+name+"\n")
        uFiles.append(name)

        print name + "\n"

  for uFile in uFiles:
    try:
      shutil.move( uXcfPath + uFile, xcfPath)
    except:
      a = 1

  os.system(" exiftool -all= " + jpgPath + "/*.jpg")
  os.system("rm " + jpgPath + "/*.jpg_original")

  os.system(" exiftool -all= " + jpgLpath + "/*.jpg")
  os.system("rm " + jpgLpath + "/*.jpg_original")

  os.system(" exiftool -all= " + jpgMpath + "/*.jpg")
  os.system("rm " + jpgMpath + "/*.jpg_original")

  os.system(" exiftool -all= " + jpgSpath + "/*.jpg")
  os.system("rm " + jpgSpath + "/*.jpg_original")

  os.system(" exiftool -all= " + jpgXsPath + "/*.jpg")
  os.system("rm " + jpgXsPath + "/*.jpg_original")

  return

register(
          "python-fu-sumkamnet-to-jpg-bath", # Имя регистрируемой функции
          "sumkam.net. Save xcf into jpg with preconfigured sizes", # Информация о дополнении
          "Save xcf into jpg with preconfigured sizes", # Короткое описание выполняемых скриптом действий
          "Eugene Polyakov", # Информация об авторе
          "Eugene Polyakov (foxen@foxen.ru)", # Информация о копирайте
          "30.12.2013", # Дата изготовления
          "to jpg batch", # Название пункта меню, с помощью которого дополнение будет запускаться
          "", # Типы изображений, с которыми может работать дополнение
          [
          (PF_STRING,"cfgHomeFile", "path to config", ~/sumkamnet/gimp-plug-ins-config/gimp-plug-ins.cfg)
          ],# Параметры, которые будут переданы дополнению
          [],# Список переменных, которые вернет дополнение
          plugin_func, 
          menu="<Image>/SUMKAMNET/")# Имя исходной функции и меню, в которое будет помещён пункт, запускающий дополнение

main()