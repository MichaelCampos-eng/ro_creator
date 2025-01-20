from config_classes.config import Config
from pin_management.list_manager import *
import hydra


@hydra.main(config_path="configs", config_name="config.yaml", version_base=None)
def main(cfg: Config):

    while True:
        """
        1) Create wire list
        2) Create unused pins list
        3) Map ground pins
        4) Produce test continuity 
        """

        if cfg.task == "Wire List":
            wire_list = WireList(file_path="testing")
            wire_list.begin_manual()
            break
        
        elif cfg.task == "Ground List":
            GroundList(file_path="testing") 
        
        elif cfg.task == "Unused Pins":
            unused_pins = IsolatedList(file_path="testing")
            unused_pins.begin_manual()
            break

        elif cfg.task == "Create RO":
            return
        
     

if __name__ == "__main__":
    main()