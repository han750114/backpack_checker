import cv2
import numpy as np

# 載入圖片
image_path = r"/home/serena/backpack_checker/static/uploaded/8883.jpg"  # 更換為你的圖片路徑
img = cv2.imread(image_path)
if img is None:
    print("圖片讀取失敗，請檢查路徑")
    exit()

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

# cv2.imshow("Bakon", gray)

# 高斯模糊 + 邊緣偵測
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
# cv2.imshow("Backlllon", blurred)

edges = cv2.Canny(blurred, 86, 150)

# cv2.imshow("Backon", edges)

# 膨脹 + 侵蝕讓邊緣更連續
kernel = np.ones((5, 5), np.uint8)
edges = cv2.dilate(edges, kernel, iterations=3)
edges = cv2.erode(edges, kernel, iterations=2)

# cv2.imshow("ohmydamn", edges)

# 找輪廓
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# cv2.imshow("ohmydamn", edges)

# 找最大輪廓
max_area = 0
backpack_contour = None
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > max_area:
        max_area = area
        backpack_contour = cnt

# 畫出輪廓
if backpack_contour is not None:
    epsilon = 0.035 * cv2.arcLength(backpack_contour, True)
    approx = cv2.approxPolyDP(backpack_contour, epsilon, True)
    box = cv2.boundingRect(approx)
    x, y, w, h = box
    cv2.rectangle(img_rgb, (x, y), (x + w, y + h), (0, 0, 255), 3)
    # cv2.imshow("ohmydamn", img_rgb)
    # STEP 1: 擷取背包區域 ROI
    cropped_items = img[y:y+h, x:x+w]
    roi_gray = gray[y:y+h, x:x+w]
    # cv2.imshow("oh51amn", cropped_items)
    # cv2.imshow("amn", roi_gray)

# 顯示結果
# cv2.imshow("Backpack Detection", img_rgb)
# cv2.imshow("Backon", cropped_items)
#  ----------------------------------------------------------------------------------------------------------
# 轉為灰階 + 增強對比度
gay0 = cv2.cvtColor(cropped_items, cv2.COLOR_BGR2GRAY)
gray1 = cv2.equalizeHist(gay0)

# cv2.imshow("Ba", gay0 )

# 高斯模糊 + 邊緣偵測 wallet unbrella
blukkkkkk = cv2.GaussianBlur(gray1, (5, 5), 0)
edges1 = cv2.Canny(blukkkkkk, 40, 180)

# cv2.imshow("Basesgsg", edges1 )


# 膨脹 + 侵蝕讓邊緣更連續
kernel1 = np.ones((3, 3), np.uint8)
# edges1 = cv2.erode(edges1, kernel, iterations=10)
edges1 = cv2.dilate(edges1, kernel1, iterations=9)
# cv2.imshow("Basewgwgwgggsgsg", edges1 )
kernel = np.ones((7, 7), np.uint8)
edges1 = cv2.erode(edges1, kernel, iterations=2)
# cv2.imshow("Basewgwgwgggsgsg", edges1 )


# 膨脹 + 侵蝕讓邊緣更連續
kernel1 = np.ones((5, 5), np.uint8)
# edges1 = cv2.erode(edges1, kernel, iterations=10)
edges1 = cv2.dilate(edges1, kernel1, iterations=13)
# cv2.imshow("Basewgwgwgggsgsg", edges1 )
kernel = np.ones((7, 7), np.uint8)
edges1 = cv2.erode(edges1, kernel, iterations=12)
# cv2.imshow("Basewgwgwgggsgsg", edges1 )
# 找輪廓
contours, _ = cv2.findContours(edges1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 找最大輪廓（背包）
max_area = 0
backpack_contour = None
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > max_area:
        max_area = area
        backpack_contour = cnt

# cv2.imshow("Ba", edges1 )


# 在彩圖上畫出最大輪廓
if backpack_contour is not None:
    cv2.drawContours(cropped_items, [backpack_contour], -1, (0, 0, 0), 3)  # 綠色輪廓線，線寬為3

# 建立與原圖大小相同的黑色遮罩
maskll = np.zeros_like(gay0)

# 在遮罩上填滿最大輪廓區域
cv2.drawContours(maskll, [backpack_contour], -1, 255, thickness=cv2.FILLED)

# 把遮罩應用到原圖，保留輪廓內部的圖像
backpack_only = cv2.bitwise_and(cropped_items, cropped_items, mask=maskll)

# 擷取邊界矩形並裁剪出 ROI（可選）
x, y, w, h = cv2.boundingRect(backpack_contour)
cropped_ddddd = backpack_only[y:y+h, x:x+w]



# --------------------------------------------------------------------------------------------------------------------------------
# cv2.imshow("wallet unberrla", cropped_ddddd)
# cv2.imshow("cropppng", cropped_backpack)


x, y, w, h = cv2.boundingRect(backpack_contour)
cv2.rectangle(cropped_ddddd, (x, y), (x + w, y + h), (0, 0, 0), 3)  # 矩形
# 再裁切綠色輪廓區域的最小長方形（直接用彩色版本）
x, y, w, h = cv2.boundingRect(backpack_contour)
cropped_rectangle = cropped_ddddd[y:y+h, x:x+w]

# 顯示裁切後的長方形區域
# cv2.imshow("rectangle", cropped_rectangle)
# -------------------------------------------------------------------------------------------------

# 對 cropped_rectangle 做處理：轉灰階並找邊緣
gray_final = cv2.cvtColor(cropped_rectangle, cv2.COLOR_BGR2GRAY)
blurred_final = cv2.GaussianBlur(gray_final, (5, 5), 0)
edges_final = cv2.Canny(blurred_final, 50, 190)


# 膨脹 + 侵蝕
kernel_final = np.ones((3, 3), np.uint8)
edges_final = cv2.dilate(edges_final, kernel_final, iterations=40)
edges_final = cv2.erode(edges_final, kernel_final, iterations=25)

# 找出輪廓
contours_final, _ = cv2.findContours(edges_final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 尋找最大輪廓
max_area = 0
max_contour = None
for cnt in contours_final:
    area = cv2.contourArea(cnt)
    if area > max_area:
        max_area = area
        max_contour = cnt

# 若有找到最大輪廓，就畫出並裁切
if max_contour is not None:
    # 畫出輪廓（確認用）
    cv2.drawContours(cropped_rectangle, [max_contour], -1, (255, 0, 0), 2)

    # 建立遮罩並保留最大輪廓區域
    mask_final = np.zeros_like(gray_final)
    cv2.drawContours(mask_final, [max_contour], -1, 255, thickness=cv2.FILLED)
    final_object = cv2.bitwise_and(cropped_rectangle, cropped_rectangle, mask=mask_final)

    # 裁切最小外接矩形
    x, y, w, h = cv2.boundingRect(max_contour)
    final_crop = final_object[y:y+h, x:x+w]

    # 顯示最終裁切結果
    cv2.imshow("Final Cropped Item", final_crop)

cv2.waitKey(0)
cv2.destroyAllWindows()