from django.db import models
from django.utils import timezone
import os


class BandImage(models.Model):
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.image.url

class Gig(models.Model):
    name = models.CharField(max_length=200)
    gig_link = models.CharField(blank=True, max_length=200)
    gig_date = models.DateTimeField("Gig date")
    preview_date_hidden = models.CharField(max_length=200)
    preview_date_admin = models.CharField(max_length=200, verbose_name="date",
        blank=True, null=True, help_text="This will override the date above when shown on the site. Otherwise leave blank")

    def __str__(self):
        return self.name

    def coming_up(self):
        "Check whether the gig is in the future"
        return self.gig_date >= timezone.now()

    def save(self, *args, **kwargs):
        date_num = self.gig_date.strftime("%d")
        if date_num[0]=='0':
            date_num=date_num[1]
        self.preview_date_hidden = self.gig_date.strftime("%A ")+date_num + self.gig_date.strftime(" %B %Y")
        super(Gig, self).save(*args, **kwargs)


class Video(models.Model):
    name = models.CharField(max_length=100)
    thumbnail = models.ImageField(blank=True, help_text="Thumbnail for the youtube video")
    youtube_link = models.CharField(default='', max_length=300, blank=True, verbose_name="Youtube URL")
    pub_date = models.DateTimeField(null=True, default=timezone.now, help_text="Use this to re-order the videos. This doesn't actually reflect the date of publication of the youtube video")

    def __str__(self):
        return self.name

    def create_youtube_embed(self, url):
        """
        Parses URL to youtube video and returns the embeded link.
        """
        if 'www.youtube.com' not in url:
            return ""
        if 'youtube.com/embed' in url:
            if "?" in url:
                url = url.split("?")[0]
            url = url.split('embed/')[-1]
            # return url
        if 'watch' in url:
            url = url.split("=")[1]
        if "&" in url:
            url = url.split("&")[0]
        return os.path.join('https://www.youtube.com','embed',url+'?autoplay=1')

    def save(self, *args, **kwargs):
        self.youtube_link = self.create_youtube_embed(url=self.youtube_link)
        super(Video, self).save(*args, **kwargs)
