import multiprocessing                                                                                                                                            
from pathlib import Path                                                                                                                                          
from time import time                                                                                                                                             
from zipfile import ZipFile                                                                                                                                       
import logging
from typing import Union                                                                                                                                                    

DATA = Path("/data/DeepFakeData")                                                                                                    
logging.basicConfig(filename="extract.log", level=logging.INFO)
zipfiles = sorted(list(DATA.glob("**/*.zip")), key=lambda x: str(x.stem))
zipfiles = [str(x) for x in zipfiles]
def extract_zip(zipfile: Union[str, Path])->None:
    with ZipFile(zipfile) as zip_file:
        for file in zip_file.namelist():
            zip_file.extract(member=file, path="/data/DeepFakeData/")
    #logging.info('Finished extracting' + zipfile)


start = time()
with multiprocessing.Pool() as pool: # use all cores available
    pool.map(extract_zip, zipfiles)

