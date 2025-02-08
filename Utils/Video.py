from moviepy import ImageClip, AudioFileClip, concatenate_audioclips
from Utils.Logger import get_logger
import os
# Set up the logger
logger = get_logger("Video")

def create_video(img_path: str, audio_clips_dir: str, output_video: str) -> None:
    try:
        os.makedirs("temp/temp_audiofile",exist_ok=True)
        if audio_clips_dir:
            logger.info(f"Starting video creation: {img_path} with audio from {audio_clips_dir}.")

            # Load all audio files
            logger.info(f"Loading audio clips from {audio_clips_dir}.")
            audio_clips = [AudioFileClip(audio) for audio in audio_clips_dir]
            logger.info(f"Loaded {len(audio_clips)} audio clips.")

            # Merge the audio clips into one track
            logger.info("Merging audio clips into one final audio track.")
            final_audio = concatenate_audioclips(audio_clips)
            logger.info(f"Final audio duration: {final_audio.duration} seconds.")

            # Create a video from the image (same duration as final audio)
            logger.info(f"Creating video from image: {img_path}.")
            video = ImageClip(img_path, duration=final_audio.duration)
            logger.info("Video created successfully from the image.")

            # Attach the merged audio to the video
            logger.info("Attaching the merged audio to the video.")
            video = video.with_audio(final_audio)
            video = video.with_fps(24)  # Set frame rate
            logger.info("Audio attached and frame rate set to 24 fps.")

            # Export the video
            logger.info(f"Exporting the video to {output_video}.")
            video.write_videofile(
                output_video, 
                codec="libx264",  # You can also use 'h264_nvenc' for NVIDIA GPUs
                fps=24,
                temp_audiofile=f"temp/temp_audiofile/audio.mp3"
            )
            logger.info(f"Video exported successfully to {output_video}.")
        else:
                        # Create a video from the image (same duration as final audio)
            logger.info(f"Creating video from image: {img_path}.")
            video = ImageClip(img_path, duration=4)
            logger.info("Video created successfully from the image.")
    
            # Attach the merged audio to the video
            logger.info("Attaching the merged audio to the video.")
            video = video.with_fps(24)  # Set frame rate
            logger.info("Audio attached and frame rate set to 24 fps.")
    
            # Export the video
            logger.info(f"Exporting the video to {output_video}.")
            video.write_videofile(
                output_video, 
                codec="libx264",  # You can also use 'h264_nvenc' for NVIDIA GPUs
                fps=24
                )
            logger.info(f"Video exported successfully to {output_video}.")
        
    except Exception as e:
        logger.error(f"An error occurred while creating the video: {e}")
        pass
