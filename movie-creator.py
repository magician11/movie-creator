from sys import argv
from moviepy.editor import AudioFileClip, ImageClip, TextClip, CompositeVideoClip

# Load the audio file and image from command line arguments
audio_clip = AudioFileClip(argv[1])
img_clip = ImageClip(argv[2], duration=audio_clip.duration).set_audio(audio_clip)

magicNumber = 8

title_clip = (
    TextClip(
        argv[3].replace("\\n", "\n"),
        fontsize=magicNumber * magicNumber,
        color="white",
        size=img_clip.size,
    )
    .set_duration(magicNumber)
    .set_position("center")
)

credits_clip = (
    TextClip(
        "https://andrewgolightly.com",
        fontsize=magicNumber * 5,
        color="white",
        size=img_clip.size,
    )
    .set_duration(magicNumber)
    .set_position("center")
    .set_start(audio_clip.duration)
)

# Concatenate the title clip, the image clip with audio, and the credits clip
# Ensure the title clip appears for the full duration before transitioning
final_clip = CompositeVideoClip(
    [
        title_clip.set_start(0).crossfadeout(1),
        img_clip.set_start(title_clip.duration - 1)
        .crossfadein(1)
        .crossfadeout(1)
        .set_end(audio_clip.duration),
        credits_clip.set_start(audio_clip.duration).crossfadein(1).crossfadeout(1),
    ]
)

# Write the result to a file
final_clip.write_videofile(
    "output_with_silent_title.mp4", fps=24, codec="libx264", audio_codec="aac"
)
