from moviepy.editor import VideoFileClip, concatenate_videoclips

name = "scratch-telenger-0090-fighting"
clip = VideoFileClip("../zenn-assets/videos/" + name + ".mov").crop(x1=300,y1=60,x2=1620,y2=1050)
clip = clip.resize(width=480)
clip1 = clip.subclip(0.8, 4)
clip2 = clip.subclip(19, 22.5)
clip3 = clip.subclip(42, 46)
clip1.write_gif("images/scratch-telenger-0090/" + name + "-1.gif", fps=15)
clip2.write_gif("images/scratch-telenger-0090/" + name + "-2.gif", fps=15)
clip3.write_gif("images/scratch-telenger-0090/" + name + "-3.gif", fps=15)
