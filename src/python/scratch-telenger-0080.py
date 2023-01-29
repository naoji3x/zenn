from moviepy.editor import VideoFileClip, concatenate_videoclips

name = "scratch-telenger-0080-fighting"
clip = VideoFileClip("../zenn-assets/videos/" + name + ".mov").crop(x1=300,y1=85,x2=1620,y2=1075)
clip = clip.resize(width=480).subclip(17.3, 21.5)
clip.write_gif("images/scratch-telenger-0080/" + name + ".gif", fps=15)
