from config_classes.config import Config
from pin_management.list_manager import *
import hydra


@hydra.main(config_path="configs", config_name="config.yaml", version_base=None)
def main(cfg: Config):

    return
        
     

if __name__ == "__main__":
    main()