#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2018/9/19

from dueros.directive.AudioPlayer.PlayerInfo import PlayerInfo


class AudioPlayerInfo(PlayerInfo):

    def __init__(self, content, controls=[]):
        super(AudioPlayerInfo, self).__init__(content, controls)