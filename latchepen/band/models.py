from django.db import models
from django.utils import timezone
from .date_utils import format_date, get_next_third_sunday
import os


class BandImage(models.Model):
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.image.url


class Gig(models.Model):
    name = models.CharField(max_length=200)
    gig_link = models.CharField(blank=True, max_length=200)
    gig_date = models.DateTimeField("Gig date")
    preview_date_admin = models.CharField(max_length=200, verbose_name="date",
        blank=True, null=True, help_text="This will override the date above when shown on the site. Otherwise leave blank")
    jamboree = models.BooleanField(default=False, help_text="Tick this box and the gig with automatically be set to Jamboree recurring every 3rd Sunday of the month")

    def __str__(self):
        return self.name

    def coming_up(self):
        "Check whether the gig is in the future"
        return self.gig_date >= timezone.now()

    def display_gig_date(self):
        """
        Returns the gig date to display in the template
        """
        if self.jamboree:
            return format_date(le_date=get_next_third_sunday())
        elif self.preview_date_admin:
            return self.preview_date_admin
        else:
            return format_date(le_date=self.gig_date)

    def gig_date_filter(self):
        "Publication date used to filter in views: also includes jamboree date"
        if self.jamboree:
            return get_next_third_sunday()
        else:
            return self.gig_date.date()

    def save(self, *args, **kwargs):
        if self.jamboree:
            self.gig_link = "http://www.jamboreevenue.co.uk/"
            self.name = "Jamboree"
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
