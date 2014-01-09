#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SUMKAM.NET
#
# Вспомогательный скрипт. 
# Считывает файл конфигурации.
# Cоздает структкру каталогов для обработки фотографий.

import os
import ConfigParser

cfgHomeFile = "~/sumkamnet/gimp-plug-ins-config/gimp-plug-ins.cfg"

config = ConfigParser.ConfigParser()
config.read(os.path.expanduser(cfgHomeFile))

basePath = config.get("Paths","base")
pathsList = config.items("Paths")
excludeList = ["base","logs"]
for pathList in pathsList:
    if pathList[0] not in excludeList:
        path = basePath + pathList[1]
        if not os.path.exists(path):
            os.makedirs(path)
