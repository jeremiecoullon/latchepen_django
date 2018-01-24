from django.shortcuts import render
from .models import BandImage, Gig, Video

def index(request):
    gallery = BandImage.objects.all()
    gigs = Gig.objects.all()
    gigs = sorted(gigs, key=lambda x: x.gig_date_filter())
    videos = Video.objects.order_by('-pub_date')
    return render(request, 'band/index.html', {'gallery': gallery, 'gigs':gigs, 'videos':videos})
