from moviepy import ImageClip, AudioFileClip, concatenate_audioclips, VideoFileClip, concatenate_videoclips
import os
import glob

def create_video(img_path: str, audio_clips_dir: str, output_video: str) -> None:    
    try:
        # Load all audio files
        audio_clips = [AudioFileClip(audio) for audio in audio_clips_dir]

        # Merge the audio clips into one track
        final_audio = concatenate_audioclips(audio_clips)

        # Create a video from the image (same duration as final audio)
        video = ImageClip(img_path, duration=final_audio.duration)

        # Attach the merged audio to the video
        video = video.with_audio(final_audio)
        video = video.with_fps(24)  # Set frame rate

        # Export the video
        # Export the video with GPU acceleration (e.g., using NVENC for NVIDIA GPUs)
        video.write_videofile(
            output_video, 
            codec="libx264",  # You can also use 'h264_nvenc' for NVIDIA GPUs
            fps=24,
            temp_audiofile="temp/temp_audiofile"
        )
    except:
        pass