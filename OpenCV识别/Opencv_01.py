# -*- coding:utf-8 -*-
import cv2.cv2 as cv2

# 读取图片

rawImage = cv2.imread("image.png")
# 高斯模糊，将图片平滑化，去掉干扰的噪声
image = cv2.GaussianBlur(rawImage, (3, 3), 0)
# 图片灰度化
image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
# Sobel算子（X方向）
Sobel_x = cv2.Sobel(image, cv2.CV_16S, 1, 0)
# Sobel_y = cv2.Sobel(image, cv2.CV_16S, 0, 1)
absX = cv2.convertScaleAbs(Sobel_x)  # 转回uint8
# absY = cv2.convertScaleAbs(Sobel_y)
# dst = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
image = absX
# 二值化：图像的二值化，就是将图像上的像素点的灰度值设置为0或255,图像呈现出明显的只有黑和白
ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)
# 闭操作：闭操作可以将目标区域连成一个整体，便于后续轮廓的提取。
kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 5))
image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernelX)
# 膨胀腐蚀(形态学处理)
kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
kernelY = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 19))
image = cv2.dilate(image, kernelX)
image = cv2.erode(image, kernelX)
image = cv2.erode(image, kernelY)
image = cv2.dilate(image, kernelY)
# 平滑处理，中值滤波
image = cv2.medianBlur(image, 15)
# 查找轮廓
contours, w1 = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for item in contours:
    rect = cv2.boundingRect(item)
    x = rect[0]
    y = rect[1]
    weight = rect[2]
    height = rect[3]
    if weight > (height * 2):
        # 裁剪区域图片
        chepai = rawImage[y:y + height, x:x + weight]
        cv2.imshow('chepai' + str(x), chepai)

# 改变车牌号大小
image = cv2.resize(chepai, (445, 150))
# cv2.imshow("1", image)
# 高斯模糊
blurerd = cv2.GaussianBlur(image, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
# cv2.imshow("213", blurerd)
# 图像转灰度
gray = cv2.cvtColor(blurerd, cv2.COLOR_BGR2GRAY)
# cv2.imshow("2", gray)

# 图像阀值化操作——获得二值化图
ret, image = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
cv2.imshow("3", image)

contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
words = []
words_images = []
# 对所有轮廓逐一操作
for item in contours:
    word = []
    rect = cv2.boundingRect(item)
    x = rect[0]
    y = rect[1]
    weight = rect[2]
    height = rect[3]
    word.append(x)
    word.append(y)
    word.append(weight)
    word.append(height)
    words.append(word)

# # 排序，车牌号有顺序。words是一个嵌套列表
print(word)
# # words    嵌套错误
words = sorted(word, key=lambda s: s[0], reverse=False)
i = 0
# # 排序，车牌号有顺序。words是一个嵌套列表
for word in words:
    #     # 筛选字符轮廓
    if (word[3] > (word[2] * 1.5)) and (word[3] < (word[2] * 3.5)) and (word[2] > 25):
        i = i + 1
        splite_image = image[word[1]:word[1] + word[3], word[0]:word[0] + word[2]]
        words_images.append(splite_image)
        print(i)
print(words)

# 绘制轮廓
image = cv2.drawContours(rawImage, contours, -1, (0, 0, 255), 3)
cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
