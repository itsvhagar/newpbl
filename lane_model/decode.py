import numpy as np
import matplotlib.pyplot as plt
import cv2

# Giả sử biến `image_bytes` là đối tượng bytes nhận được từ client
# Decode đối tượng bytes thành mảng numpy
def De(image_bytes):
    # # print('1: ', type(image_bytes))
    # image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # # print('2: ', type(image_array))
    # # # Đọc ảnh từ mảng numpy
    # image_array = cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)
    # print('3: ', type(image_array))
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)

    # cv2.imshow('Decoded Image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # Hiển thị ảnh bằng matplotlib
    # plt.imshow(cv2.cvtColor(image_bytes, cv2.COLOR_BGR2RGB))
    # plt.axis('off')
    # plt.show()
    # plt.imshow(image_array)
    # plt.show()
    return image
