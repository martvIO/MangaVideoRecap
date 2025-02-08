from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def split_video(input_video):
    # Load the video file
    video = VideoFileClip(input_video)
    total_duration = int(video.duration)  # Get total duration in seconds
    base_name, ext = os.path.splitext(input_video)  # Extract name and extension
    output_folder = f"{base_name}_splits"  # Create an output folder
    os.makedirs(output_folder, exist_ok=True)
    
    # Iterate and create 1-minute clips
    start_time = 0
    clip_number = 1
    
    while start_time < total_duration:
        end_time = min(start_time + 60, total_duration)  # Ensure last clip is the remainder
        clip = video.subclipped(start_time, end_time)  # Extract subclip
        output_filename = os.path.join(output_folder, f"{base_name}_part{clip_number}.mp4")
        clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")
        
        print(f"Saved: {output_filename}")
        start_time += 60  # Move to the next minute
        clip_number += 1
    
    video.close()
    print("Video splitting complete!")

