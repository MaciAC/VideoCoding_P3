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

        self.video_formats = []
        self.audio_formats = []
        self.broadcasts = []
        self.broadcast_dictionary = {
            "DVB": {
                "Video": ["mpeg2","h264"],
                "Audio": ["aac", "ac3", "mp3", "mp2", "mp1"]
            },
            "ATSC": {
                "Video": ["mpeg2","h264"],
                "Audio": ["aac"]
            },
            "ISDB": {
                "Video": ["mpeg2","h264"],
                "Audio": ["ac3"]
            },
            "DTMB": {
                "Video": ["mpeg2","h264","avs","avs+"],
                "Audio": ["dra", "aac", "ac3", "mp1", "mp2", "mp3"]
            }
        }

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

    def get_stream_formats(self):
        os.system("ffmpeg -i {} > aux.txt 2>&1".format(self.filename))
        with open("aux.txt",'r') as file:
            line = file.readline()
            # read the file line by line checking if contains certain info
            while line:
                if "Stream" in line:
                    if "Audio" in line:
                        self.audio_formats.append(line.split(':', 2)[-1].split(" ")[2])
                    elif "Video" in line:
                        self.video_formats.append(line.split(':', 2)[-1].split(" ")[2])

                line = file.readline()

    def check_broadcast_compatibility(self):
        if not self.audio_formats and not self.video_formats:
            self.get_stream_formats()

        for broadcast_std in self.broadcast_dictionary.keys():
            vid_flag = False
            aud_flag = False
            for vid in self.video_formats:
                if vid in self.broadcast_dictionary[broadcast_std]["Video"]:
                    vid_flag = True

            for aud in self.audio_formats:
                if aud in self.broadcast_dictionary[broadcast_std]["Audio"]:
                    aud_flag = True

            if aud_flag and vid_flag:
                self.broadcasts.append(broadcast_std)
