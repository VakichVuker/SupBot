import random


class PictureStorage:
    TYPE_PHOTO = 'photo'
    TYPE_DOCUMENT = 'document'

    def __init__(self, root_path):
        self.root_path = root_path
        self.picture_dict = {
            1: {
                'path': root_path + '/files/img.png',
                'type': self.TYPE_PHOTO
            },
            2: {
                'path': root_path + '/files/img_1.png',
                'type': self.TYPE_PHOTO
            },
            3: {
                'path': root_path + '/files/img_2.png',
                'type': self.TYPE_PHOTO
            },
            4: {
                'path': root_path + '/files/img_3.png',
                'type': self.TYPE_PHOTO
            },
            5: {
                'path': root_path + '/files/charlotte-traffic.mp4',
                'type': self.TYPE_DOCUMENT
            },
            6: {
                'path': root_path + '/files/shrek-gingerbread-man.mp4',
                'type': self.TYPE_DOCUMENT
            },
            7: {
                'path': root_path + '/files/wink-gingerbread-man.mp4',
                'type': self.TYPE_DOCUMENT
            },
        }

    def get_random_pic(self):
        random_num = random.randint(1, 7)
        return self.picture_dict[random_num]
