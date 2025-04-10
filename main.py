
import pydicom as dcm
import os
import shutil
from pathlib import Path
from logging_config import configure_module_logging
import logging

if __name__ == "__main__":
    logger = logging.getLogger('main')
else:
    logger = logging.getLogger(__name__)


def set_root_folder():
    """set the root folder to search for RDSR files"""
    
    logger.info('Setting the root folder')
    root = input('Enter the root folder: ')
    root = Path(root)
    if not root.exists():
        logger.error(f'The path {root} does not exist.')
        return None
    if not root.is_dir():
        logger.error(f'The path {root} is not a directory.')
        return None
    logger.info(f'Root folder is {root}')
    return root

def set_dest_folder():
    """set the destination folder to save the RDSR files"""
    # Input destination folder. Press enter to use "RDSR" in current working directory.
    logger.info('Setting the root folder')
    dest = input('Enter the destination folder ("Enter" to use "RDSR" in current dir): ')
    if dest == '':
        dest = Path.cwd() / 'RDSR'
    else:
        dest = Path(dest)
    
    if not dest.exists():
        logger.error(f'The path {dest} does not exist.')
        try:
            dest.mkdir(parents=True)
            logger.info(f'Created the directory {dest}.')
        except Exception as e:
            logger.error(f'Failed to create the directory {dest}. Error: {e}')
            return None
        
    if not dest.is_dir():
        logger.error(f'The path {dest} is not a directory.')
        return None
    
    logger.info(f'Destination folder is {dest}.')
    return dest

def _read_metadata(fp: str) -> dcm.Dataset:
    # Attempt tp read the DICOM file and return the dataset
    try:
        ds = dcm.dcmread(fp, stop_before_pixels=True)
        return ds
    except Exception as e:
        logger.warning(f"Non DICOM file excluded: {fp}, error using dcmread: {str(e)}")
        return None

def _is_rdsr(ds: dcm.Dataset, path: str) -> bool:
    # Check for Radiation Dose Structured Report (RDSR):
    if hasattr(ds, "SOPClassUID") and (ds.SOPClassUID == "1.2.840.10008.5.1.4.1.1.88.67"):
        logger.info(f"RDSR file found: {path}")
        return True
    else:
        return False

def find_rdsr_files(root, dest):
    """find RDSR files in the root folder and save them to the destination folder"""
    logger.info('Finding RDSR files')
    for root, _, files in os.walk(root):
        for file in files:
            # try dicomread (stop before pixels)
            # if the sop class is not RDSR, skip
            # if the sop class is RDSR, save it to the destination folder
            path = os.path.join(root, file)
            metadata = _read_metadata(path)
            if metadata is None:
                continue
            if _is_rdsr(metadata, path):
                # read the study date and time and copy the file to the destination
                # with the filename study date and time (only hrs) - RDSR.dcm
                study_date = metadata.StudyDate
                study_time = metadata.StudyTime
                study_date_time = f"{study_date}_{study_time[:2]}_RDSR.dcm"
                dest_path = os.path.join(dest, study_date_time)
                try:
                    shutil.copy2(path, dest_path)
                    logger.info(f"Copying {path} to {dest_path}")
                except Exception as e:
                    logger.error(f"Failed to copy {path} to {dest_path}: {str(e)}")

def copy_rdsr_files():
    """the main function to run the script"""
    logger.info('Starting the main function')

    root = set_root_folder()
    if root is None:
        logger.error('Root folder is not set. Exiting.')
        return
    dest = set_dest_folder()
    if dest is None:
        logger.error('Destination folder is not set. Exiting.')
        return
    
    find_rdsr_files(root, dest)



    return

if __name__ == '__main__':
    configure_module_logging({
        'main': {'file': 'main.log', 'level': logging.DEBUG, 'console': True}})
    logger.info('Finished setup of logger for main module.')
    #copy_rdsr_files()
    filename = "/run/media/bhosteras/PRIVATE_USB/Huddoser/RDSR/20250409_10_RDSR.dcm"
    ds = dcm.dcmread(filename)
    logger.info(f"RDSR file found: {filename}")
    # calculate skindose in pyskindose:
    



