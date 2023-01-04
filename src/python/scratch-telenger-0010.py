from moviepy.editor import VideoFileClip

name = "scratch-telenger-0010-1-rough"
clip = VideoFileClip("../zenn-assets/videos/" + name + ".mp4")
clip = clip.resize(width=480)
clip.write_gif("images/scratch-telenger-0010/" + name + ".gif", fps=4)

name = "scratch-telenger-0010-2-walking"
clip = VideoFileClip("../zenn-assets/videos/" + name + ".mov").subclip(0, 5)
clip.write_gif("images/scratch-telenger-0010/" + name + ".gif", fps=24)
