from moviepy import VideoFileClip
from moviepy.video.fx.Crop import Crop
import os

def split_and_create_short(input_video):
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
        
        # Get the video size and calculate the cropping to fit 9:16 aspect ratio
        width, height = clip.size
        new_height = int(width * 16 / 9)  # Calculate new height for 9:16 aspect ratio
        start_y = (height - new_height) // 2  # Calculate the starting Y position for cropping
        
        # Crop the video to fit the vertical frame (9:16)
        cropped_clip = Crop(width=1080,height=1920, x_center=clip.w / 2, y_center=clip.h / 2).apply(clip)
        cropped_clip = cropped_clip.resized((1080,1920))
        # Resize the cropped clip to 1080x1920 (portrait mode for YouTube Shorts)        
        # Output file path
        output_filename = os.path.join(output_folder, f"{base_name}_part{clip_number}.mp4")
        cropped_clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")
        
        print(f"Saved: {output_filename}")
        start_time += 60  # Move to the next minute
        clip_number += 1
    
    video.close()
    print("Video splitting and conversion to Shorts complete!")

if __name__ == '__main__':
    input_video = r"C:\Users\martv\Videos\Seraph of the end\Chapter 1\0202 (1).mp4"  # Replace with your input video path
    split_and_create_short(input_video)
