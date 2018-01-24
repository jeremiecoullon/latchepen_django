from django.db import models
from django.utils import timezone
import os
from calendar import Calendar


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
    jamboree = models.BooleanField(default=False, help_text="Tick this box and the gig with automatically be set to Jamboree recurring every 3rd Sunday of the month")

    def __str__(self):
        return self.name

    def coming_up(self):
        "Check whether the gig is in the future"
        return self.gig_date >= timezone.now()

    def get_third_sunday_of_month(self, year, month):
        """
        Finds the third Sunday of a given month in a year

        Parameters
        ----------
        year, month: Datetime.year, Datetime.month

        Returns
        -------
        third_sunday: Datetime.date
        """
        iter_dates = Calendar().itermonthdates(year, month)
        list_days = [c for c in iter_dates if c.month==month]
        third_sunday = [day for day in list_days if day.strftime("%A")=="Sunday"][2]
        return third_sunday

    def get_next_third_sunday(self):
        """
        Finds the next third Sunday

        Returns
        -------
        get_next_third_sunday: Datetime.date
        """
        third_sunday_current_month = self.get_third_sunday_of_month(year=timezone.now().year, month=timezone.now().month)
        if third_sunday_current_month >= timezone.now().date():
            return third_sunday_current_month
        else:
            le_year = timezone.now().year
            next_month = timezone.now().month+1
            if next_month == 13:
                le_year, next_month = timezone.now().year+1, 1
            return self.get_third_sunday_of_month(year=le_year, month=next_month)

    def format_date(self, le_date):
        """
        Format date to display in gig list

        Parameters
        ----------
        le_date: Datetime.date

        Returns
        formatted_date: str
        """
        date_num = le_date.strftime("%d")
        if date_num[0]=='0':
            date_num=date_num[1]
        return le_date.strftime("%A ")+date_num + le_date.strftime(" %B %Y")


    def display_gig_date(self):
        """
        Returns the gig date to display in the template
        """
        if self.jamboree:
            return self.format_date(le_date=self.get_next_third_sunday())
        elif self.preview_date_admin:
            return self.preview_date_admin
        else:
            return self.preview_date_hidden

    def save(self, *args, **kwargs):
        self.preview_date_hidden = self.format_date(le_date=self.gig_date)
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
