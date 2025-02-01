from moviepy import ImageClip, AudioFileClip, concatenate_audioclips
import os
import glob

def create_video(img_path: str, audio_clips_dir: str, output_video: str) -> None:
    # loading all the audio files from the audio clips directory
    files = glob.glob(f"{audio_clips_dir}/*.mp3")
    
    # Load all audio files
    audio_clips = [AudioFileClip(audio) for audio in files]

    # Merge the audio clips into one track
    final_audio = concatenate_audioclips(audio_clips)

    # Create a video from the image (same duration as final audio)
    video = ImageClip(img_path, duration=final_audio.duration)

    # Attach the merged audio to the video
    video = video.with_audio(final_audio)
    video = video.with_fps(24)  # Set frame rate

    # Export the video
    video.write_videofile(f"{output_video}", codec="libx264", fps=24)