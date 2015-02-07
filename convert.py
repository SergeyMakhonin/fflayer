__author__ = 'sergey'

from converter import Converter

c = Converter()

info = c.probe('test1.ogg')

conv = c.convert('test1.ogg', '/tmp/output.mkv', {
    'format': 'mkv',
    'audio': {
        'codec': 'mp3',
        'samplerate': 11025,
        'channels': 2
    },
    'video': {
        'codec': 'h264',
        'width': 720,
        'height': 400,
        'fps': 15
    }})

for timecode in conv:
    print('Converting (%f) ...\r' % timecode)