from moviepy.editor import VideoFileClip

name = "scratch-telenger-0020-walking"
clip = VideoFileClip("../zenn-assets/videos/" + name + ".mov").crop(x1=300,y1=60,x2=1620,y2=1050)
clip = clip.resize(width=480).subclip(0, 9)
clip.write_gif("images/scratch-telenger-0020/" + name + ".gif", fps=24)
