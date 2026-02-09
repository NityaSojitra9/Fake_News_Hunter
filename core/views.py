from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponse
from .forms import ArticleURLForm, UserRegistrationForm, UserProfileForm
from .models import ArticleAnalysis, UserProfile
from .scraper import extract_article_info, clean_text
from .nlp_analysis import analyze_article
from django.urls import reverse
import PyPDF2
import time

def is_news_content(text):
    """
    Simple heuristic to check if text is news-related.
    Returns True if news-related keywords are found, else False.
    """
    if not text or len(text) < 100:
        return False
    news_keywords = [
        'news', 'report', 'journalist', 'government', 'study', 'published',
        'breaking', 'update', 'headline', 'official', 'analysis', 'research',
        'article', 'press', 'media', 'interview', 'statement', 'source', 'agency',
        'editor', 'coverage', 'broadcast', 'investigation', 'announcement', 'conference'
    ]
    text_lower = text.lower()
    found = sum(1 for word in news_keywords if word in text_lower)
    return found >= 2  # Require at least 2 news-related keywords

# Create your views here.

def landing(request):
    """Landing page - shows landing page for all users"""
    return render(request, 'landing.html')

@login_required
def home(request):
    if request.method == 'POST':
        form = ArticleURLForm(request.POST, request.FILES)
        if form.is_valid():
            url = form.cleaned_data.get('url')
            uploaded_file = form.cleaned_data.get('file')
            if uploaded_file:
                filename = uploaded_file.name
                ext = filename.split('.')[-1].lower()
                file_text = ""
                if ext == 'txt':
                    try:
                        file_text = uploaded_file.read().decode('utf-8', errors='ignore')
                    except Exception:
                        form.add_error('file', 'Could not read the .txt file.')
                        return render(request, 'home.html', {'form': form})
                elif ext == 'pdf':
                    try:
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        for page in pdf_reader.pages:
                            text = page.extract_text()
                            if text:
                                file_text += text
                    except Exception:
                        form.add_error('file', 'Could not read the .pdf file.')
                        return render(request, 'home.html', {'form': form})
                else:
                    form.add_error('file', 'Unsupported file type. Please upload a .txt or .pdf file.')
                    return render(request, 'home.html', {'form': form})

                if not file_text.strip():
                    form.add_error('file', 'The uploaded file is empty or could not be read.')
                    return render(request, 'home.html', {'form': form})

                # News content check
                if not is_news_content(file_text):
                    form.add_error('file', 'This file is not a news article. Please upload files that contain news content.')
                    return render(request, 'home.html', {'form': form})

                cleaned_content = clean_text(file_text)
                nlp_results = analyze_article(cleaned_content)
                # Generate a unique URL value for file uploads
                unique_url = f"uploaded-file-{int(time.time())}-{filename}"
                analysis = ArticleAnalysis.objects.create(
                    url=unique_url,
                    title=filename,
                    content=file_text[:1000],
                    publication_date=None,
                    author='Unknown',
                    source_domain='Uploaded File',
                    prediction=nlp_results['prediction'],
                    confidence=nlp_results['confidence'],
                    sentiment=nlp_results['sentiment'],
                    sentiment_score=nlp_results['sentiment_score'],
                    entities=", ".join([f"{e[0]} ({e[1]})" for e in nlp_results['entities']]),
                    trust_score=nlp_results['trust_score'],
                    user=request.user,
                )
                messages.success(request, 'File analyzed successfully!')
                return redirect('result', pk=analysis.pk)
            elif url:
                try:
                    analysis = ArticleAnalysis.objects.get(url=url)
                    return redirect('result', pk=analysis.pk)
                except ArticleAnalysis.DoesNotExist:
                    pass
                article_info = extract_article_info(url)
                cleaned_content = clean_text(article_info['content'])
                nlp_results = analyze_article(cleaned_content, url)
                analysis = ArticleAnalysis.objects.create(
                    url=url,
                    title=article_info['title'],
                    content=article_info['content'][:1000],
                    publication_date=article_info['publication_date'],
                    author=article_info['author'],
                    source_domain=article_info['source_domain'],
                    prediction=nlp_results['prediction'],
                    confidence=nlp_results['confidence'],
                    sentiment=nlp_results['sentiment'],
                    sentiment_score=nlp_results['sentiment_score'],
                    entities=", ".join([f"{e[0]} ({e[1]})" for e in nlp_results['entities']]),
                    trust_score=nlp_results['trust_score'],
                    user=request.user,
                )
                messages.success(request, 'URL analyzed successfully!')
                return redirect('result', pk=analysis.pk)
    else:
        form = ArticleURLForm()
    return render(request, 'home.html', {'form': form})

@login_required
def result(request, pk):
    analysis = get_object_or_404(ArticleAnalysis, pk=pk)
    return render(request, 'result.html', {'analysis': analysis})

@login_required
def history(request):
    filter_val = request.GET.get('filter')
    
    # Admin users can see all analyses, regular users only see their own
    if request.user.is_staff or request.user.is_superuser:
        qs = ArticleAnalysis.objects.all().order_by('-created_at')
    else:
        qs = ArticleAnalysis.objects.filter(user=request.user).order_by('-created_at')
    
    if filter_val in ('Real', 'Fake'):
        analyses = qs.filter(prediction=filter_val)
    else:
        analyses = qs
    stats = {
        'total': qs.count(),
        'real': qs.filter(prediction='Real').count(),
        'fake': qs.filter(prediction='Fake').count(),
    }
    return render(request, 'history.html', {'analyses': analyses, 'stats': stats})





@login_required
def contact(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Send email
        try:
            from django.core.mail import send_mail
            from django.conf import settings
            
            subject = 'Fake News Hunter'
            email_message = f"""Name: {name}
Email: {email}

Message:
{message}"""
            
            send_mail(
                subject=subject,
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['nsextra9@gmail.com'],
                fail_silently=False,
            )
            
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        except Exception as e:
            messages.error(request, f'Sorry, there was an error sending your message: {str(e)}')
        
        return render(request, 'contact.html', {'submitted': True})
    return render(request, 'contact.html', {'submitted': False})

@login_required
def delete_analysis(request, pk):
    analysis = get_object_or_404(ArticleAnalysis, pk=pk, user=request.user)
    analysis.delete()
    messages.success(request, 'Analysis deleted successfully.')
    return redirect('history')

@login_required
def clear_my_history(request):
    ArticleAnalysis.objects.filter(user=request.user).delete()
    messages.success(request, 'Your analysis history cleared successfully.')
    return redirect('history')

@login_required
def delete_analysis(request, pk):
    analysis = get_object_or_404(ArticleAnalysis, pk=pk)
    analysis.delete()
    messages.success(request, 'Analysis deleted successfully.')
    return redirect('history')

@login_required
def clear_history(request):
    # Admin users can clear all analyses, regular users only clear their own
    if request.user.is_staff or request.user.is_superuser:
        ArticleAnalysis.objects.all().delete()
        messages.success(request, 'All history cleared successfully.')
    else:
        ArticleAnalysis.objects.filter(user=request.user).delete()
        messages.success(request, 'Your analysis history cleared successfully.')
    return redirect('history')

@login_required
def download_result(request, pk):
    analysis = get_object_or_404(ArticleAnalysis, pk=pk)
    content = f"Title: {analysis.title}\nURL: {analysis.url}\nSource: {analysis.source_domain}\nPrediction: {analysis.prediction}\nConfidence: {analysis.confidence:.2f}\nSentiment: {analysis.sentiment}\nSentiment Score: {analysis.sentiment_score:.2f}\nEntities: {analysis.entities}\nTrust Score: {analysis.trust_score}\n\nContent:\n{analysis.content}"
    response = HttpResponse(content.encode('utf-8'), content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="analysis_{pk}.txt"'
    return response

# Authentication views
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Set admin privileges based on role selection
            role = form.cleaned_data.get('role')
            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True
                user.save()
                messages.success(request, 'Admin account created successfully! Welcome to FakeNewsHunter.')
            else:
                messages.success(request, 'Account created successfully! Welcome to FakeNewsHunter.')
            
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'registration/profile.html', {'form': form})

def custom_logout(request):
    """Custom logout view that directly redirects to landing page without showing logout page"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('landing')
