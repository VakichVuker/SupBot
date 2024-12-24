import time
import os

class MemeStorage:

    def __init__(self, root_path):
        self.storage_root_path = root_path + '/storage'

    def get_meme_filepath(self, user_id):
        current_unix_timestamp = int(time.time())
        filename = str(current_unix_timestamp) + '.png'
        filepath = self.storage_root_path + '/' + str(user_id) + '/'
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        return filepath + filename
