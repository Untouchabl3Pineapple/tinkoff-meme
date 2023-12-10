import cv2, subprocess, os
from moviepy.editor import VideoFileClip


class VideoProcessor:
    def __init__(self, video_path):
        self.video_capture = cv2.VideoCapture(video_path)
        self.frame_rate = self.video_capture.get(cv2.CAP_PROP_FPS)
        self.width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    def extract_audio(self):
        video_clip = VideoFileClip(video_path)
        self.audio_clip = video_clip.audio

    def overlay_images(self, images_info, output_path, audio_path=None):
        video_output = cv2.VideoWriter(
            output_path, self.fourcc, self.frame_rate, (self.width, self.height)
        )

        frame_count = 0

        while True:
            ret, frame = self.video_capture.read()

            if not ret:
                break

            for info in images_info:
                start_time, end_time, image_path = info
                if start_time <= frame_count / self.frame_rate <= end_time:
                    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
                    resized_image = cv2.resize(
                        image, (int(frame.shape[1] / 2), int(frame.shape[0] / 2))
                    )

                    x_offset = frame.shape[1] - resized_image.shape[1] - 20
                    y_offset = 20

                    for _ in range(0, 3):
                        frame[
                            y_offset : y_offset + resized_image.shape[0],
                            x_offset : x_offset + resized_image.shape[1],
                        ] = resized_image[:, :] * (resized_image[:, :] / 255.0) + frame[
                            y_offset : y_offset + resized_image.shape[0],
                            x_offset : x_offset + resized_image.shape[1],
                        ] * (
                            1.0 - resized_image[:, :] / 255.0
                        )

            video_output.write(frame)
            frame_count += 1

        self.video_capture.release()
        video_output.release()
        cv2.destroyAllWindows()

    def get_video_with_audio(self):
        self.audio_clip.write_audiofile("result.mp3", codec="mp3")
        cmd = "ffmpeg -i resultWithoutAudio.mp4 -i result.mp3 -c:v copy -c:a aac -strict experimental -shortest ../docs/videos/result.mp4"
        subprocess.call(cmd, shell=True)
        os.remove("resultWithoutAudio.mp4")
        os.remove("result.mp3")


# Путь к видеофайлу
video_path = "../docs/videos/tinkoff.mp4"

video_processor = VideoProcessor(video_path)
video_processor.extract_audio()

# Список информации о времени и пути для изображений
images_info = [
    (0, 5, "../docs/imgs/1.jpg"),
    (5, 8, "../docs/imgs/2.jpg"),
    (8, 11, "../docs/imgs/3.jpg"),
    (11, 14, "../docs/imgs/4.jpg"),
    (14, 17, "../docs/imgs/5.jpg"),
    (17, 21, "../docs/imgs/6.jpg"),
    (21, 23, "../docs/imgs/7.jpg"),
    (23, 27, "../docs/imgs/8.jpg"),
    (27, 30, "../docs/imgs/9.jpg"),
    (30, 32, "../docs/imgs/10.jpg"),
    (32, 34, "../docs/imgs/11.jpg"),
    (34, 38, "../docs/imgs/12.jpg"),
    (38, 39, "../docs/imgs/13.jpg"),
    (39, 41, "../docs/imgs/14.jpg"),
    (41, 44, "../docs/imgs/15.jpg"),
    (44, 46, "../docs/imgs/16.jpg"),
]

# Путь для сохранения результата
output_video_path = "resultWithoutAudio.mp4"

# Путь к аудиофайлу
audio_path = "../docs/videos/tinkoff.mp4"

video_processor.overlay_images(images_info, output_video_path, audio_path)
video_processor.get_video_with_audio()
