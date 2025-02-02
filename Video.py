from moviepy import ImageClip, AudioFileClip, concatenate_audioclips, VideoFileClip, concatenate_videoclips
import os
import glob

def create_video(img_path: str, audio_clips_dir: str, output_video: str) -> None:    
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
        threads=4,  # Set number of threads for encoding (optional)
        preset="fast",  # Encoding speed (optional)
        ffmpeg_params=["-c:v", "h264_nvenc"]  # Enable GPU-based encoding (NVIDIA NVENC)
    )

def combine_videos(main_directory, output_file="output.mp4", fps=24):
    all_videos = []
    
    # Loop through all subdirectories inside the main directory
    for subdir in sorted(os.listdir(main_directory)):
        subdir_path = os.path.join(main_directory, subdir)
        if os.path.isdir(subdir_path):  # Ensure it's a directory
            video_files = sorted(glob.glob(os.path.join(subdir_path, "*.mp4")))  # Find all MP4 files
            
            for video_file in video_files:
                try:
                    clip = VideoFileClip(video_file)
                    all_videos.append(clip)
                except Exception as e:
                    print(f"Error loading {video_file}: {e}")
    
    if not all_videos:
        print("No videos found to combine.")
        return
    
    # Concatenate all video clips
    final_video = concatenate_videoclips(all_videos, method="compose")
    final_video.write_videofile(
        output_file, 
        codec="libx264",  # You can use 'h264_nvenc' for NVIDIA GPUs
        fps=fps,
        threads=4,  # Set number of threads for encoding (optional)
        preset="fast",  # Encoding speed (optional)
        ffmpeg_params=["-c:v", "h264_nvenc"]  # Enable GPU-based encoding (NVIDIA NVENC)
    )    
