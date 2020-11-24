import os

class Container_manager:

    def __init__(self, filename):
        self.filename = filename
        temp = self.filename.split('.')[0]
        self.mono_filename = temp + "mono_audio.mp4"
        self.lowrate_filename = temp + "lowrate_audio.mp4"
        self.video_filename = temp + "video.mp4"
        self.subtitle_filename = temp + "_subtitles.srt"
        self.output_name = temp + "_output.mp4"


    def export_audio_mono(self):
        os.system("ffmpeg -i {} -ss 00:00:00 -t 00:01:00 -map 0:a:0 -ac 1 {}".format(self.filename, self.mono_filename))

    def export_audio_lowrate(self):
        os.system("ffmpeg -i {} -ss 00:00:00 -t 00:01:00 -map 0:a:0 -b:a 24k {}".format(self.filename, self.lowrate_filename))

    def export_video(self):
        os.system("ffmpeg -i {} -ss 00:00:00 -t 00:01:00 -map 0:v:0 -c:v copy {}".format(self.filename, self.video_filename))

    def create_new_container(self):
        self.export_audio_mono()
        self.export_audio_lowrate()
        self.export_video()
        os.system("ffmpeg -i {} -i {} -i {} -i {} -ss 00:00:00 -t 00:01:00 -map 0:a:0 -map 1:a:0 -map 2:v:0 -c:v copy -map 3:s:0 -c:s mov_text {}".format(self.mono_filename,self.lowrate_filename,self.filename, self.subtitle_filename, self.output_name))
