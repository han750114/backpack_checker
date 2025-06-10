import cv2
import numpy as np

# 載入圖片
image_path =r"/home/serena/backpack_checker/static/uploaded/IMG_8887.jpeg"  # 更換為你的圖片路徑
img = cv2.imread(image_path)

# 縮放圖片寬度為 600
scale_width = 600
h, w = img.shape[:2]
scaling_factor = scale_width / w
img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

# 備份彩圖
img_rgb = img.copy()

# 轉為灰階 + 增強對比度
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)

# 高斯模糊 + 邊緣偵測
blurred = cv2.GaussianBlur(gray, (9, 9), 0)
edges = cv2.Canny(blurred, 60, 150)

# 膨脹 + 侵蝕讓邊緣更連續
kernel = np.ones((5, 5), np.uint8)
edges = cv2.dilate(edges, kernel, iterations=16)
edges = cv2.erode(edges, kernel, iterations=10)

# 找輪廓
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 找最大輪廓（背包）
max_area = 0
backpack_contour = None
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > max_area:
        max_area = area
        backpack_contour = cnt

# cv2.imshow("Ba", edges )


# 在彩圖上畫出最大輪廓
if backpack_contour is not None:
    cv2.drawContours(img_rgb, [backpack_contour], -1, (0, 255, 0), 3)  # 綠色輪廓線，線寬為3

# 建立與原圖大小相同的黑色遮罩
mask = np.zeros_like(gray)

# 在遮罩上填滿最大輪廓區域
cv2.drawContours(mask, [backpack_contour], -1, 255, thickness=cv2.FILLED)

# 把遮罩應用到原圖，保留輪廓內部的圖像
backpack_only = cv2.bitwise_and(img_rgb, img_rgb, mask=mask)

# 擷取邊界矩形並裁剪出 ROI（可選）
x, y, w, h = cv2.boundingRect(backpack_contour)
cropped_backpack = backpack_only[y:y+h, x:x+w]

# 顯示和儲存結果
cv2.imshow("Backpack Cropped", cropped_backpack)
cv2.imwrite("cropped_backpack.png", cropped_backpack)
cv2.waitKey(0)
cv2.destroyAllWindows()



# # 顯示結果
# cv2.imshow("Backpack Detection", img_rgb)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
