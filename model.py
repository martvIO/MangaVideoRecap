from transformers import AutoModel, AutoConfig
from Logger import get_logger

logger = get_logger(name="Manga")

def load_model():
    model_name = "ragavsachdeva/magiv2" # this model is used to extract the text and the character's names from a manga panel

    try:
        # loading the model from cache folder
        logger.info(f"trying to load the model {model_name} from the cache folder")
        model = AutoModel.from_pretrained(f"cache/model/{model_name}", device_map = 'cuda' , trust_remote_code=True, force_download=True)
    except: 
        logger.error(f"Failed to load the model {model_name} from the cache folder")
        # downloading the model from the huggingface model hub
        model = AutoModel.from_pretrained(model_name, trust_remote_code=True, force_download=True)
        # saving the model in the cache/model folder
        model.save_pretrained(f"cache/model/{model_name}")
        logger.info(f"Model {model_name} saved to the cache folder")

    logger.debug(f"load the model {model_name}")
    return model