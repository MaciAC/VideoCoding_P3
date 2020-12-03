import os

class Container_manager:

    def __init__(self, filename):
        self.filename = filename
        temp = filename.split('.')[0]
        self.mono_filename = temp + "mono_audio.mp4"
        self.aac_filename = temp + "aac_audio.mp4"
        self.mpg_filename = temp + ".mpg"
        self.lowrate_filename = temp + "lowrate_audio.mp4"
        self.video_filename = temp + "video.mp4"
        self.subtitle_filename = temp + "_subtitles.srt"
        self.epic_filename = temp + "_epic_container.mp4"

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

    def transcode2mpg(self):
        os.system("ffmpeg -i {} -ss 00:00:00 -t 00:00:10 {}".format(self.filename, self.mpg_filename))

    def transcode2aac(self):
        os.system("ffmpeg -i {} -ss 00:00:00 -t 00:01:00 -c:v copy -ac 1 -c:a aac {}".format(self.filename, self.aac_filename))


    def create_new_container(self):
        self.export_audio_mono()
        self.export_audio_lowrate()
        self.export_video()
        os.system("ffmpeg -i {} -i {} -i {} -i {} -ss 00:00:00 -t 00:01:00 -map 0:a:0 -map 1:a:0 -map 2:v:0 -c:v copy -map 3:s:0 -c:s mov_text {}".format(self.mono_filename,self.lowrate_filename,self.filename, self.subtitle_filename, self.epic_filename))



    def check_broadcast_compatibility(self, filename):

        compatible = []
        audio_formats = []
        video_formats = []

        os.system("ffmpeg -i {} > aux.txt 2>&1".format(filename))
        with open("aux.txt",'r') as file:
            line = file.readline()
            # read the file line by line checking if contains certain info
            while line:
                if "Stream" in line:
                    if "Audio" in line:
                        audio_formats.append(line.split(':', 2)[-1].split(" ")[2])
                    elif "Video" in line:
                        video_formats.append(line.split(':', 2)[-1].split(" ")[2])

                line = file.readline()


        for broadcast_std in self.broadcast_dictionary.keys():
            vid_flag = False
            aud_flag = False
            for vid in video_formats:
                if vid in self.broadcast_dictionary[broadcast_std]["Video"]:
                    vid_flag = True

            for aud in audio_formats:
                if aud in self.broadcast_dictionary[broadcast_std]["Audio"]:
                    aud_flag = True

            if aud_flag and vid_flag:
                compatible.append(broadcast_std)


        if not compatible:
            print("{} is not compatible with any broadcast standard! :(\n".format(filename))
        else:
            print("{} compatible with:\n".format(filename))
            for name in compatible:
                print(" .- {} \n".format(name))


def test_compatibility_check():
    Container_mngr = Container_manager("BBB_curt.mp4")
    Container_mngr.export_audio_mono()
    Container_mngr.export_audio_lowrate()
    Container_mngr.export_video()
    Container_mngr.transcode2aac()
    Container_mngr.transcode2mpg()
    Container_mngr.create_new_container()

    Container_mngr.check_broadcast_compatibility(Container_mngr.filename)
    Container_mngr.check_broadcast_compatibility(Container_mngr.aac_filename)
    Container_mngr.check_broadcast_compatibility(Container_mngr.mono_filename)
    Container_mngr.check_broadcast_compatibility(Container_mngr.mpg_filename)
    Container_mngr.check_broadcast_compatibility(Container_mngr.lowrate_filename)
    Container_mngr.check_broadcast_compatibility(Container_mngr.video_filename)
    Container_mngr.check_broadcast_compatibility(Container_mngr.epic_filename)



test_compatibility_check()
