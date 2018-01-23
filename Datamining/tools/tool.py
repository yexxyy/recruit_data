#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by yetongxue<yeli.studio@qq.com> on 2018/1/23 17:50

from sqlalchemy import create_engine

def get_connnect():
	engine = create_engine('mysql://root:123456@localhost:3306/zhilian?charset=utf8', echo=False)
	connnect = engine.connect()
	return connnect

