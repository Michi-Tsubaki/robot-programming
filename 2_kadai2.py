#!/usr/bin/env python
# -*- coding: utf-8 -*-

##「フロー駆動形」のプログラム
##大域変数に指令値を保存し、ループの中でその指令を送る

import rospy
from opencv_apps.msg import RotatedRectStamped

from geometry_msgs.msg import Twist

rect = RotatedRectStamped() ##指令値を大域変数として持つ

def callback(msg):
    global rect ##大域変数としてrectを使用することを宣言する
    area = msg.rect.size.width *msg.rect.size.height
    rospy.loginfo("area = {}, center = ({} {})".format(area, msg.rect.center.x, msg.rect.center.y))
    if area > 100:
        rect = msg ##認識結果の面積が100のときだけrectの結果に保存

if __name__ == '__main__': #メイン文
    try:
        rospy.init_node('client')
        rospy.Subscriber('/camshift/track_box', RotatedRectStamped, callback)
        pub = rospy.Publisher('/cmd_vel', Twist)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown(): #ROSが起動しているとき
            cmd_vel = Twist() #pubするcmd_velのインスタンスを生成している
            rect_arrived = rospy.Time.now() - rect.header.stamp #最大1秒前の結果しか利用しない。古すぎるのは使わない
            if rect_arrived.to_sec() < 1.0:
                if rect.rect.center.x < 320:
                    cmd_vel.angular.z = 0.1
                else:
                    cmd_vel.angular.z = -0.1
            else: #もし対象物が1秒以上観測されないときは，旋回する．
                cmd_vel.angular.z = 1.0 ##課題1のときから，ここを変更した！！

            rospy.loginfo("\t\t\t\t\t\tpublish {}".format(cmd_vel.angular.x)) #roslogに残す
            pub.publish(cmd_vel) #pubは↑で起動しているpublisher。publishが関数
            rate.sleep()
            
    except rospy.ROSInterruptException: pass #エラーハンドリング
