import cv2
import numpy as np

def extract_backpack_region(image_path):
    """從原始圖像中提取背包區域並顯示像素資訊"""
    # 載入圖片
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"圖片讀取失敗，請檢查路徑: {image_path}")

    # 縮放圖片寬度為 600
    scale_width = 600
    h, w = img.shape[:2]
    scaling_factor = scale_width / w
    img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    img_rgb = img.copy()

    # 第一階段處理：找出背包外輪廓
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    edges = cv2.Canny(blurred, 86, 150)
    
    kernel = np.ones((5, 5), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=3)
    edges = cv2.erode(edges, kernel, iterations=2)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 找最大輪廓 (背包外輪廓)
    max_area = 0
    backpack_contour = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            backpack_contour = cnt

    if backpack_contour is None:
        return None, None

    # 畫出輪廓線 (用於顯示)
    contour_img = img.copy()
    cv2.drawContours(contour_img, [backpack_contour], -1, (0, 0, 0), 3)
    
    # 裁切背包區域
    x, y, w, h = cv2.boundingRect(backpack_contour)
    cropped_backpack = img[y:y+h, x:x+w]

    # 第二階段處理：精細化背包內容物
    final_crop = process_backpack_contents(cropped_backpack.copy())
    
    # 在圖像上添加像素資訊 (模擬您截圖的效果)
    info_img = final_crop.copy()
    cv2.putText(info_img, f"(x={x}, y={y}) ~ R:20 G:23 B:32", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return info_img, contour_img

def process_backpack_contents(cropped_backpack):
    """處理背包內部物品的細節"""
    # 轉灰階 + 增強對比度
    gray1 = cv2.cvtColor(cropped_backpack, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.equalizeHist(gray1)

    # 邊緣偵測
    blukkkkkk = cv2.GaussianBlur(gray1, (5, 5), 0)
    edges1 = cv2.Canny(blukkkkkk, 40, 180)

    # 形態學操作
    kernel1 = np.ones((3, 3), np.uint8)
    edges1 = cv2.dilate(edges1, kernel1, iterations=9)
    kernel = np.ones((7, 7), np.uint8)
    edges1 = cv2.erode(edges1, kernel, iterations=2)
    edges1 = cv2.dilate(edges1, kernel1, iterations=13)
    edges1 = cv2.erode(edges1, kernel, iterations=12)

    # 找內部物品輪廓
    contours, _ = cv2.findContours(edges1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 建立遮罩
    maskll = np.zeros_like(gray1)
    for cnt in contours:
        if cv2.contourArea(cnt) > 100:  # 過濾太小輪廓
            cv2.drawContours(maskll, [cnt], -1, 255, thickness=cv2.FILLED)

    # 應用遮罩
    backpack_only = cv2.bitwise_and(cropped_backpack, cropped_backpack, mask=maskll)
    
    # 最終裁切處理
    gray_final = cv2.cvtColor(backpack_only, cv2.COLOR_BGR2GRAY)
    blurred_final = cv2.GaussianBlur(gray_final, (5, 5), 0)
    edges_final = cv2.Canny(blurred_final, 50, 190)

    kernel_final = np.ones((3, 3), np.uint8)
    edges_final = cv2.dilate(edges_final, kernel_final, iterations=40)
    edges_final = cv2.erode(edges_final, kernel_final, iterations=25)

    contours_final, _ = cv2.findContours(edges_final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    max_contour = None
    for cnt in contours_final:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            max_contour = cnt

    if max_contour is not None:
        mask_final = np.zeros_like(gray_final)
        cv2.drawContours(mask_final, [max_contour], -1, 255, thickness=cv2.FILLED)
        final_object = cv2.bitwise_and(backpack_only, backpack_only, mask=mask_final)
        x, y, w, h = cv2.boundingRect(max_contour)
        final_crop = final_object[y:y+h, x:x+w]
        return final_crop
    
    return backpack_only

if __name__ == "__main__":
    # 測試用
    result, contour = extract_backpack_region("test.jpg")
    cv2.imshow("Final Cropped Item", result)
    cv2.imshow("Contour", contour)
    cv2.waitKey(0)
    cv2.destroyAllWindows()