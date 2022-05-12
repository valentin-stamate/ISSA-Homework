import cv2
import numpy as np


def main():
    video_path = 'Lane Detection Test Video 01.mp4'
    cam = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cam.read()
        old_shape = frame.shape

        ratio = old_shape[0] / old_shape[1]

        # Exercise 2
        width = 420
        frame = cv2.resize(frame, (int(width), int(width * ratio)))

        # Exercise 3
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height = frame.shape[0]
        width = frame.shape[1]

        # Exercise 4
        upper_left = (int(width * 0.33), int(height * 0.75))
        upper_right = (int(width * 0.6), int(height * 0.75))
        lower_left = (int(0), int(height - 1))
        lower_right = (int(width - 1), int(height - 1))

        trapezoid_points = np.array([upper_left, upper_right, lower_right, lower_left], dtype='int32')

        trapezoid_frame = np.zeros((height, width), dtype='uint8')
        cv2.fillConvexPoly(trapezoid_frame, points=trapezoid_points, color=1)
        trapezoid_frame = trapezoid_frame * frame
        # Exercise 5
        screen_points = np.array([(0, 0), (width - 1, 0), (width - 1, height - 1), (0, height - 1)], dtype='float32')
        magical_matrix = cv2.getPerspectiveTransform(np.float32(trapezoid_points), screen_points)

        stretched_trapezoid_frame = cv2.warpPerspective(trapezoid_frame, magical_matrix, (width, height))

        # Exercise 6
        frame = cv2.blur(stretched_trapezoid_frame, ksize=(3, 3))

        # Exercise 7
        sobel_vertical = np.float32([
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ])

        sobel_horizontal = np.transpose(sobel_vertical)

        frame_f = np.float32(frame)

        frame_1 = cv2.filter2D(frame_f, -1, sobel_vertical)
        frame_2 = cv2.filter2D(frame_f, -1, sobel_horizontal)

        # frame_int = cv2.convertScaleAbs(frame_2)
        combined = np.sqrt(frame_1 * frame_1 + frame_2 * frame_2)

        frame = cv2.convertScaleAbs(combined)

        # Exercise 8
        threshold = int(150)

        frame = np.array(frame > threshold, dtype='uint8')
        frame = frame * 255

        # Exercise 9
        copy_frame = frame.copy()
        nr = int(width * 0.2)
        copy_frame[0:width, 0:nr] = 0
        copy_frame[0:width, (width - nr): width] = 0

        left_xs = []
        left_ys = []
        right_xs = []
        right_ys = []

        half = int(width / 2)
        first_half = copy_frame[0:width, 0:half]
        second_half = copy_frame[0:width, half:width]

        left_points = np.argwhere(first_half > 1)
        right_points = np.argwhere(second_half > 1)

        for i in range(left_points.shape[0]):
            for j in range(left_points.shape[1]):
                left_xs.append(j)
                left_ys.append(i)

        for i in range(right_points.shape[0]):
            for j in range(right_points.shape[1]):
                right_xs.append(j)
                right_ys.append(i)

        frame = copy_frame

        # Exercise 10
        b_left, a_left = np.polynomial.polynomial.polyfit(left_xs, left_ys, deg=1)
        b_right, a_right = np.polynomial.polynomial.polyfit(right_xs, right_ys, deg=1)

        left_top_y = int(0)
        left_top_x = int((left_top_y - b_left) / a_left)
        left_top = (int(left_top_x), int(left_top_y))

        left_bottom_y = int(height - 1)
        left_bottom_x = int((left_bottom_y - b_left) / a_left)
        left_bottom = (int(left_bottom_x), int(left_bottom_y))

        right_top_y = int(0)
        right_top_x = int((right_top_y - b_right) / a_right)
        right_top = (int(right_top_x), int(right_top_y))

        right_bottom_y = int(height - 1)
        right_bottom_x = int((right_top_y - b_right) / a_right)
        right_bottom = (int(right_bottom_x), int(right_bottom_y))

        # Not working for some reason
        if np.abs(left_top[0]) < 10 ** 8:
            cv2.line(frame, left_top, left_bottom, (200, 0, 0), width)

        if np.abs(right_top[0]) < 10 ** 8:
            cv2.line(frame, right_top, right_bottom, (100, 0, 0), width)

        if ret is False:
            break

        # Exercise 11
        # second_frame = np.array((height, width), dtype='uint8')
        #
        # if np.abs(left_top[0]) < 10 ** 8:
        #     cv2.line(second_frame, left_top, left_bottom, (200, 0, 0), width)
        #
        # if np.abs(right_top[0]) < 10 ** 8:
        #     cv2.line(second_frame, right_top, right_bottom, (100, 0, 0), width)

        # Exercise 12
        # it runs in real time

        cv2.imshow('Original', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
