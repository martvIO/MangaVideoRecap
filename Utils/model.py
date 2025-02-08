from transformers import AutoModel
from Utils.Logger import get_logger

# Initialize the logger for tracking the model loading process
logger = get_logger(name="Manga")

def load_model():
    """
    This function loads the pre-trained model to extract text and character names from manga panels.
    
    The model is first attempted to be loaded from the local cache. If it is not found, 
    the model is downloaded from the HuggingFace model hub and then saved in the cache for future use.
    
    Returns:
    model: The loaded transformer model.
    """
    model_name = "ragavsachdeva/magiv2"  # The name of the model to extract text and character names from manga panels

    try:
        # Attempting to load the model from the cache folder
        logger.info(f"Trying to load the model '{model_name}' from the cache folder.")
        model = AutoModel.from_pretrained(f"cache/model/{model_name}", device_map='cuda', trust_remote_code=True, force_download=True)
        logger.info(f"Model '{model_name}' loaded successfully from the cache.")
    
    except Exception as e: 
        # If loading the model from the cache fails, log the error and proceed to download the model
        logger.error(f"Failed to load the model '{model_name}' from the cache folder: {e}")
        logger.info(f"Attempting to download the model '{model_name}' from the HuggingFace model hub.")
        
        try:
            # Download the model from the HuggingFace model hub
            model = AutoModel.from_pretrained(model_name, trust_remote_code=True, force_download=True)
            logger.info(f"Model '{model_name}' downloaded successfully from HuggingFace.")
            
            # Save the model to the cache for future use
            model.save_pretrained(f"cache/model/{model_name}")
            logger.info(f"Model '{model_name}' saved to the cache folder for future use.")
        
        except Exception as e:
            # Log an error if the model download fails
            logger.error(f"Failed to download and save the model '{model_name}': {e}")
            raise RuntimeError(f"Failed to download or save the model '{model_name}'")

    # Final debug message indicating that the model has been loaded successfully
    logger.debug(f"Model '{model_name}' loaded successfully.")
    return model
