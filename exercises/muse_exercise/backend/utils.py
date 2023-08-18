
def allowed_extension(extension):
    ALLOWED_EXTENSIONS = ['mp4', 'ogg', 'mov', 'mp3', 'avi', 'mpeg']
    return extension in ALLOWED_EXTENSIONS

def create_new_directory(path_directory):
    import pathlib
    pathlib.Path(path_directory).mkdir(parents=True, exist_ok=True)

def timestamp():
    import time
    return str(time.time()).split(".")[0]

def generate_output_file(filepath):
    splitted_filepath = filepath.rsplit('.',1)
    output_filepath = str(splitted_filepath[0])  + "_result." +  str(splitted_filepath[1])
    return output_filepath

def get_collection(host, port):
    from pymongo import MongoClient
    connection = MongoClient(host, port)
    db = connection['db_muse_videos_detect_silence']
    videos = db['videos']
    return videos

def load_config(filepath):
    from configparser import ConfigParser
    config = ConfigParser()
    config.read(filepath)
    loaded_config = {}
    loaded_config['HOST']=config['DEFAULT']['HOST']
    loaded_config['PORT']=int(config['DEFAULT']['PORT'])
    loaded_config['CELERY_BROKER_ADDRESS']=config['DEFAULT']['CELERY_BROKER_ADDRESS']
    loaded_config['MONGODB_HOST']=config['DEFAULT']['MONGODB_HOST']
    loaded_config['MONGODB_PORT']=int(config['DEFAULT']['MONGODB_PORT'])
    loaded_config['DIRECTORY_VIDEO']=config['DEFAULT']['DIRECTORY_VIDEO']
    loaded_config['ROOT_API']=config['DEFAULT']['ROOT_API']
    loaded_config['DEBUG']=(config['DEFAULT']['DEBUG'].lower() == 'true')
    return loaded_config


