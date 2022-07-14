from django.shortcuts import render
from .models import Session

# Create your views here.

today = datetime.now().strftime('%Y-%m-%d')

sessions_data = Sessions.objects.filter(active='a').filter(Q(date__gte=today)|Q(date=today)).order_by('date')

  