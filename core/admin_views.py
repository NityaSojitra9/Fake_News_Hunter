from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse
from .models import ArticleAnalysis, UserProfile, UserActivity, User
import json

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Main admin dashboard with overview statistics"""
    
    # Get date range for filtering
    days = request.GET.get('days', 30)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=int(days))
    
    # Basic statistics
    total_analyses = ArticleAnalysis.objects.count()
    total_users = User.objects.count()

    
    # Recent activity
    recent_analyses = ArticleAnalysis.objects.filter(created_at__gte=start_date).count()
    recent_users = User.objects.filter(date_joined__gte=start_date).count()
    
    # Analysis by prediction
    real_count = ArticleAnalysis.objects.filter(prediction='Real').count()
    fake_count = ArticleAnalysis.objects.filter(prediction='Fake').count()
    
    
    # Top users
    top_users = User.objects.annotate(
        analysis_count=Count('analyses')
    ).filter(analysis_count__gt=0).order_by('-analysis_count')[:10]
    
    # Daily analysis chart data
    daily_analyses = []
    for i in range(int(days)):
        date = end_date - timedelta(days=i)
        count = ArticleAnalysis.objects.filter(
            created_at__date=date.date()
        ).count()
        daily_analyses.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    context = {
        'total_analyses': total_analyses,
        'total_users': total_users,

        'recent_analyses': recent_analyses,
        'recent_users': recent_users,
        'real_count': real_count,
        'fake_count': fake_count,
        'top_users': top_users,
        'daily_analyses': json.dumps(list(reversed(daily_analyses))),
        'days': days,
    }
    
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_analyses(request):
    """Admin view of all article analyses with filtering"""
    
    analyses = ArticleAnalysis.objects.select_related('user').all()
    
    # Filtering
    prediction_filter = request.GET.get('prediction')
    sentiment_filter = request.GET.get('sentiment')
    user_filter = request.GET.get('user')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if prediction_filter:
        analyses = analyses.filter(prediction=prediction_filter)
    if sentiment_filter:
        analyses = analyses.filter(sentiment=sentiment_filter)
    if user_filter:
        analyses = analyses.filter(user__username__icontains=user_filter)
    if date_from:
        analyses = analyses.filter(created_at__date__gte=date_from)
    if date_to:
        analyses = analyses.filter(created_at__date__lte=date_to)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(analyses, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_count': analyses.count(),
        'prediction_filter': prediction_filter,
        'sentiment_filter': sentiment_filter,
        'user_filter': user_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    return render(request, 'admin/analyses.html', context)

@login_required


@login_required
@user_passes_test(is_admin)
def admin_users(request):
    """User activity and management"""
    
    users = User.objects.annotate(
        analysis_count=Count('analyses')
    ).all().order_by('-date_joined')
    
    # Filtering
    search = request.GET.get('search')
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(users, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
    }
    
    return render(request, 'admin/users.html', context)

@login_required
@user_passes_test(is_admin)
def admin_analytics(request):
    """Advanced analytics and charts"""
    
    # Get date range
    days = request.GET.get('days', 30)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=int(days))
    
    # Chart data
    daily_analyses = []
    daily_users = []
    prediction_data = []
    sentiment_data = []
    
    for i in range(int(days)):
        date = end_date - timedelta(days=i)
        analysis_count = ArticleAnalysis.objects.filter(
            created_at__date=date.date()
        ).count()
        user_count = User.objects.filter(
            date_joined__date=date.date()
        ).count()
        
        daily_analyses.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': analysis_count
        })
        daily_users.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': user_count
        })
    
    # Prediction distribution
    predictions = ArticleAnalysis.objects.values('prediction').annotate(
        count=Count('id')
    )
    for pred in predictions:
        prediction_data.append({
            'label': pred['prediction'],
            'value': pred['count']
        })
    
    # Sentiment distribution
    sentiments = ArticleAnalysis.objects.values('sentiment').annotate(
        count=Count('id')
    )
    for sent in sentiments:
        sentiment_data.append({
            'label': sent['sentiment'],
            'value': sent['count']
        })
    
    context = {
        'daily_analyses': json.dumps(list(reversed(daily_analyses))),
        'daily_users': json.dumps(list(reversed(daily_users))),
        'prediction_data': json.dumps(prediction_data),
        'sentiment_data': json.dumps(sentiment_data),
        'days': days,
    }
    
    return render(request, 'admin/analytics.html', context) 