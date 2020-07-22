#!usr/bin/env python
# -*- coding:utf-8 -*-
#
# import cv2
# import os
# import imutils
# from skimage.metrics import structural_similarity
#
#
#
# class DealPic(object):
#     def __init__(self):
#         pass
#
#     def comparepic(self, im1, im2, y1=100, y2=1000, x1=0, x2=800):
#         """
#         :param im1: 图片1名称，resources_pic的图片，断言图片
#         :param im2: 图片2名称
#         图片比对有效区域为像素值范围「x1,y1-----x2,y2」
#         :param y1:
#         :param y2:
#         :param x1:
#         :param x2:
#         :return:
#         """
#         file_path1 = os.path.abspath(os.path.join(os.getcwd(), "../../.."))+"/resources_pic/"+im1
#         file_path2 = os.getcwd() + "/" + im2
#         file_path3 = os.getcwd() + "/Marked_differences.png"
#
#         # 加载两张图片并将他们转换为灰度：
#         imageA = cv2.imread(file_path1)
#         imageB = cv2.imread(file_path2)
#
#         grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
#         grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
#
#         grayAA = grayA[y1:y2, x1:x2]
#         grayBB = grayB[y1:y2, x1:x2]
#
#         # 计算两个灰度图像之间的结构相似度指数：
#         (score, diff) = structural_similarity(grayAA, grayBB, full=True)
#         print("SSIM:{}".format(score))
#         if score < 0.999:
#             (score, diff) = structural_similarity(grayA, grayB, full=True)
#             diff = (diff * 255).astype("uint8")
#             print("SSIM:{}".format(score))
#             # 找到不同点的轮廓以致于我们可以在被标识为“不同”的区域周围放置矩形：
#             thresh = cv2.threshold(
#                 diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
#             )[1]
#             cnts = cv2.findContours(
#                 thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
#             )
#             # cnts = cnts[0] if imutils.is_cv2() else cnts[1]
#             cnts = cnts[1] if imutils.is_cv3() else cnts[0]
#
#             # 找到一系列区域，在区域周围放置矩形：
#             # print cnts
#             for c in cnts:
#                 (x, y, w, h) = cv2.boundingRect(c)
#                 cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
#                 cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
#
#             # 用cv2.imshow 展现最终对比之后的图片， cv2.imwrite 保存最终的结果图片
#             # cv2.imshow("Modified", imageB)
#             cv2.imwrite(file_path3, imageA)
#             # cv2.waitKey(0)
#         return score