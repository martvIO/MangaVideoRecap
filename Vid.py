import os
import random
from moviepy import VideoFileClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip

def get_random_file(folder, extensions):
    """Returns a random file from a folder with the specified extensions."""
    files = [f for f in os.listdir(folder) if f.lower().endswith(extensions)]
    return os.path.join(folder, random.choice(files)) if files else None

def resize_and_center(clip, target_size=(1920, 1080)):
    """Resize the clip to fit within 1920x1080 while maintaining aspect ratio and center it."""
    clip = clip.resize(height=target_size[1]) if clip.w / clip.h > target_size[0] / target_size[1] else clip.resized(width=target_size[0])
    
    # Center the video on a black background
    return CompositeVideoClip([clip.with_position("center")], size=target_size)

def process_videos(videos_folder, bg_videos_folder, bg_music_folder, output_file):
    # Collect all video files
    video_files = [os.path.join(videos_folder, f) for f in os.listdir(videos_folder) if f.lower().endswith(('mp4', 'avi', 'mov', 'mkv'))]
    if not video_files:
        print("No videos found!")
        return

    print(f"Found {len(video_files)} videos. Processing...")

    # Load videos without resizing
    clips = [resize_and_center(VideoFileClip(f)) for f in video_files]
    
    # Concatenate all video clips
    final_video = concatenate_videoclips(clips, method='compose')

    # Select a random background video
    bg_video_path = get_random_file(bg_videos_folder, ('mp4', 'avi', 'mov', 'mkv'))
    if bg_video_path:
        bg_clip = VideoFileClip(bg_video_path).subclipped(0, min(final_video.duration, VideoFileClip(bg_video_path).duration))
        final_video = CompositeVideoClip([bg_clip.with_opacity(0.5), final_video])
    
    # Select a random background music file
    bg_music_path = get_random_file(bg_music_folder, ('mp3', 'wav', 'aac'))
    if bg_music_path:
        bg_music = AudioFileClip(bg_music_path).with_volume_scaled(0.5).with_duration(final_video.duration)
        final_video = final_video.with_audio(bg_music)
    
    # Export the final video
    final_video.write_videofile(output_file, codec='h264_nvenc',preset="superfast", fps=30)
    print("Video processing complete!")

if __name__ == "__main__":
    videos_folder = "t"
    bg_videos_folder = "background_vid"
    bg_music_folder = "background_mus"
    output_file = "output.mp4"
    
    process_videos(videos_folder, bg_videos_folder, bg_music_folder, output_file)
