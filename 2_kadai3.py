#!/usr/bin/env python
# -*- coding: utf-8 -*-
##「イベント・ドリブン型」のプログラムである
##subしたときにcallback関数を読んでpubする
import rospy
from opencv_apps.msg import FaceArrayStamped #Opencvの画像認識の型のインポート
from geometry_msgs.msg import Twist #ツイストの型のインポート

def callback(msg): #コールバック関数の登録
    cmd_vel = Twist() #cmd_velの型指定

    for face in msg.faces:
        x = face.face.x
    
    if x < 300.0: #顔が画面の右にあるとき
        cmd_vel.angular.z = 1 #右回転
    else: #顔が画面の左にあるとき
        cmd_vel.angular.z = -1 #左回転
    rospy.loginfo("\t\t\tpublish {}".format(cmd_vel.angular.z)) #rosのlogに指定値を残す
    pub.publish(cmd_vel) #パブリッシュする

if __name__ == '__main__': #メイン文
    try:
        rospy.init_node('client')
        rospy.Subscriber('/face_detection/faces', FaceArrayStamped, callback)
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1) #geometry.Twistの型
        rospy.spin() #待機状態に戻る

    except rospy.ROSInterruptException: pass #エラーハンドリング
        
