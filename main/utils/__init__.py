import os
import yaml
def yaml_loader(filepath):
   with open(os.path.join(os.getcwd(),filepath) , encoding='utf8') as file:
      config = yaml.load(file, Loader=yaml.FullLoader)
      return config
