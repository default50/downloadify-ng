#!/usr/bin/env python3

from gi.repository import Playerctl, GLib
import os, signal, time, sys, subprocess

player = Playerctl.Player()

pulse_src = subprocess.getoutput("pactl list | egrep -A2 '^(\*\*\* )?Source #'|grep 'Name: .*\.monitor$'| cut -d' ' -f2 | tail -n1")
print("src:" + pulse_src)
rec_pid = None
trackid = None

def rec_song(player, e = None):
        global rec_pid
        global trackid
        if rec_pid != None :
            os.killpg(rec_pid, signal.SIGQUIT)
        if trackid == None :
            trackid = player.props.metadata['mpris:trackid']
        elif trackid == player.props.metadata['mpris:trackid']
            print("Exit!")
            sys.exit()
        print('Now recording ' + trackid)
        location = '{trackNumber} - {artist} - {title}'.format(trackNumber=player.props.metadata['xesam:trackNumber'], artist=player.props.metadata['xesam:artist'][0], title=player.props.metadata['xesam:title'])
        #cmd = 'gst-launch-1.0 pulsesrc device={pulse_src} ! queue ! audio/x-raw,format=S16LE,rate=44100,channels=2 ! audioconvert ! lamemp3enc target=quality quality=2 ! filesink location="{location}.mp3"'.format(pulse_src=pulse_src, location=location)
        cmd = 'yes > /dev/null'
        rec_pid = subprocess.Popen(cmd, shell=True, preexec_fn=os.setpgrp).pid
        print("location:" + location)
        print("cmd:" + cmd)
        print("pid:" + repr(rec_pid))

player.on('metadata', rec_song)

if player.props.status == 'Paused':
    print('Pausado')
    #time.sleep(5)
    player.previous()
    rec_song(player)
    player.play()
elif player.props.status == 'Playing':
    print('Reproduciendo')
    player.pause()
    player.previous()
    rec_song(player)
    player.play()

GLib.MainLoop().run()

#subprocess.call("/usr/bin/playerctl" + " stop", shell=True)
#subprocess.call("/usr/bin/playerctl" + " previous", shell=True)

#print('Track Number:',player.props.metadata['xesam:trackNumber'])

