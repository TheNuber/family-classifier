import sys
import os
import logging
import argparse
import re

im_re = re.compile(".*\.(jpeg|jpg|png)")

# Lista de rutas de imágenes o directorios con imágenes, junto con porcentaje de imagenes por directorio (se asume 100% para imágenes)
im_list = []

def process_directory(path:str):
    it = os.scandir(path)
    is_empty = True
    total_dir = True
    local_list = []
    for entry in it:
        is_empty = False
        if im_re.fullmatch(entry.name):
            local_list.append(entry.path)
        elif entry.is_dir():
            total_dir = process_directory(entry.path) and total_dir  
        else:
            total_dir = False

    if not is_empty:
        if total_dir:
            im_list.append(path)
        else:
            im_list.extend(local_list)
        
    return total_dir and not is_empty
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    logger = logging.getLogger()
    
    parser.add_argument('-r', '--root', help="Establece el directorio raíz del que extraer las imágenes", required=True)

    argv = parser.parse_args()
    
    logger.info("Current root directory: {}".format(argv.root))

    process_directory(argv.root)

    for e in im_list:
        print(e)
    
    
