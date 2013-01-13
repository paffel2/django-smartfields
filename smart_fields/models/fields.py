from django.conf import settings
from django.db.models.fields.files import FileField, ImageField, FieldFile

from smart_fields.forms.widgets import PluploadVideoInput

__all__ = (
    "SmartFileField", "SmartImageField", "SmartAudioField", "SmartVideoField",
    "SmartPdfField",
)

KEEP_ORPHANS = getattr(settings, 'SMART_FIELDS_KEEP_ORPHANS', False)

VIDEO_FORM_TAG = getattr(settings, 'SMARTFIELDS_VIDEO_FORM_TAG', None)

VIDEO_DISPLAY_TAG = getattr(settings, 'SMARTFIELDS_VIDEO_DISPLAY_TAG', '<video id="video_%(name)s" class="video-js vjs-default-skin" controls="controls" preload="auto" width="640" height="480" data-setup="{}">%(sources)s</video>')


class SmartField(object):
    def smart_field_init(self, upload_url=None, keep_orphans=None):
        self.keep_orphans = KEEP_ORPHANS
        if not keep_orphans is None:
            self.keep_orphans = keep_orphans
        if upload_url and callable(upload_url):
            self.upload_url = upload_url

    def smart_field_save_form_data(self, instance, data):
        if not data and not data is None and not self.keep_orphans:
            instance.smart_fields_cleanup(instance, self.name)

    def upload_url(instance):
        raise NotImplementedError(
            "'upload_url' needs to be defined in order to use Plupload.")

        
class SmartFileField(FileField, SmartField):
    media_type = 'file'

    def __init__(self, upload_url=None, keep_orphans=None, *args, **kwargs):
        self.smart_field_init(upload_url=upload_url, keep_orphans=keep_orphans)
        super(SmartFileField, self).__init__(*args, **kwargs)

    def save_form_data(self, instance, data):
        self.smart_field_save_form_data(instance, data)
        super(SmartFileField, self).save_form_data(instance, data)


class SmartImageField(ImageField, SmartField):
    media_type = 'image'

    def __init__(self, upload_url=None, keep_orphans=None, *args, **kwargs):
        self.smart_field_init(upload_url=upload_url, keep_orphans=keep_orphans)
        super(SmartImageField, self).__init__(*args, **kwargs)

    def save_form_data(self, instance, data):
        self.smart_field_save_form_data(instance, data)
        super(SmartImageField, self).save_form_data(instance, data)
    

class SmartPdfField(SmartFileField):
    pass

class SmartAudioField(SmartFileField):
    media_type = 'audio'


class VideoFieldFile(FieldFile):
    @property
    def html5_tag(self):
        video_tag = VIDEO_DISPLAY_TAG or VIDEO_FORM_TAG
        return PluploadVideoInput().render_initial_content(self, video_tag=video_tag)

class SmartVideoField(SmartFileField):
    attr_class = VideoFieldFile
    media_type = 'video'
