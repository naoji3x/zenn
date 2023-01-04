from moviepy.editor import VideoFileClip, concatenate_videoclips

name = "scratch-telenger-0070-1-fighting"
clip = VideoFileClip("../zenn-assets/videos/" + name + ".mov").crop(x1=300,y1=60,x2=1620,y2=1050)
clip = clip.resize(width=480)
clip1 = clip.subclip(1, 3)
clip2 = clip.subclip(18.8, 21)
clip = concatenate_videoclips([clip1, clip2])
clip.write_gif("images/scratch-telenger-0070/" + name + ".gif", fps=15)

name = "scratch-telenger-0070-2-fighting"
clip = VideoFileClip("../zenn-assets/videos/" + name + ".mov").crop(x1=300,y1=60,x2=1620,y2=1050)
clip = clip.resize(width=480).subclip(7, 11)
clip.write_gif("images/scratch-telenger-0070/" + name + ".gif", fps=15)
