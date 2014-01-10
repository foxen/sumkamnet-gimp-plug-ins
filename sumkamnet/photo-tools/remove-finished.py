#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SUMKAM.NET
#
# Вспомогательный скрипт.
# 


import os
import ConfigParser

cfgHomeFile = "~/sumkamnet/gimp-plug-ins-config/gimp-plug-ins.cfg"

config = ConfigParser.ConfigParser()
config.read(os.path.expanduser(cfgHomeFile))

basePath = config.get("Paths","base")