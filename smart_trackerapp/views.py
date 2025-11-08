from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import smart
from .forms import smartform


# Create your views here.

def dashboard(request):
    expenses = smart.objects.all().order_by("-date")
    total = sum(s.amount for s in expenses)
    return render(request, "dashboard.html", {"expenses": expenses, "total": total})


def add_expense(request):
    if request.method == "POST":
        form = smartform(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = smartform()
    return render(request, "expenses_form.html", {"form": form})


def edit_expense(request, expense_id):
    expense = get_object_or_404(smart, id=expense_id)
    if request.method == "POST":
        form = smartform(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = smartform(instance=expense)
    return render(request, "expenses_form.html", {"form": form})


def delete_expense(request, expense_id):
    expense = get_object_or_404(smart, id=expense_id)
    if request.method == "POST":
        expense.delete()
        return redirect("dashboard")
    return render(request, "delete_confirm.html", {"expense": expense})


@csrf_exempt
def ai_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            # Analyze message content for engaging responses
            user_lower = user_message.lower()

            # Expense-related queries (keep existing logic)
            if 'total' in user_lower or 'spent' in user_lower:
                expenses = smart.objects.all()
                total = sum(exp.amount for exp in expenses)
                response = f"Your total expenses are ${total:.2f}. Keep up the great tracking! What category are you spending most on lately?"
            elif 'category' in user_lower:
                categories = smart.objects.values_list('category', flat=True).distinct()
                if categories:
                    response = f"Expense categories: {', '.join(categories)}. Which one interests you most? Maybe we can analyze your spending there!"
                else:
                    response = "No categories yet! Start adding expenses to see them here. What kind of expenses do you usually track?"
            elif 'highest' in user_lower or 'most expensive' in user_lower:
                expense = smart.objects.order_by('-amount').first()
                if expense:
                    response = f"Your highest expense is '{expense.title}' for ${expense.amount:.2f}. Wow, that was a big one! What made you spend that much?"
                else:
                    response = "No expenses recorded yet. Let's get some data in here! What's your first expense going to be?"
            elif 'recent' in user_lower or 'latest' in user_lower:
                expense = smart.objects.order_by('-date').first()
                if expense:
                    response = f"Your latest expense is '{expense.title}' on {expense.date} for ${expense.amount:.2f}. Fresh off the press! How did that purchase make you feel?"
                else:
                    response = "No expenses recorded yet. Time to add your first one? I'm excited to see what you'll track!"
            elif 'help' in user_lower or 'what can you do' in user_lower:
                response = "I can help with your expenses! Ask about total spent, categories, highest expense, or recent expenses. Or just chat about anything – I'm here for fun too! What would you like to know first?"
            # Casual/funny/off-topic responses - make them more engaging and curious
            elif any(word in user_lower for word in ['hello', 'hi', 'hey']):
                response = "Hey there! How's your day going? Ready to chat about expenses or something else? I'm all ears!"
            elif any(word in user_lower for word in ['joke', 'funny', 'laugh']):
                response = "Why did the expense tracker go to therapy? It had too many unresolved issues! 😂 What about you, got any jokes? Or tell me something funny that happened to you today!"
            elif any(word in user_lower for word in ['weather', 'day', 'how are you']):
                response = "I'm doing great, thanks for asking! As an AI, I'm always sunny. How about you? What's the weather like where you are? Does it affect your spending habits?"
            elif any(word in user_lower for word in ['bored', 'nothing']):
                response = "Bored? Let's spice things up! Tell me about your favorite hobby or ask me about your expenses. I'm all ears! What's something you're passionate about?"
            elif any(word in user_lower for word in ['thanks', 'thank you']):
                response = "You're welcome! Happy to help anytime. 😊 What's next on your mind? More expense questions or something else?"
            elif any(word in user_lower for word in ['bye', 'goodbye', 'see you']):
                response = "See you later! Don't forget to track those expenses. 👋 Come back soon - I enjoy our chats!"
            elif any(word in user_lower for word in ['love', 'like']):
                response = "Aww, that's sweet! I love chatting with you too. What's on your mind? Tell me more about what you love!"
            elif any(word in user_lower for word in ['hate', 'dislike']):
                response = "Oh no, sorry to hear that! What can I do to make it better? Or let's talk about something fun. What's something you absolutely love instead?"
            elif '?' in user_message:
                response = "That's a great question! While I'm focused on expenses, I can try to answer or we can pivot to something lighter. What's up? I'm curious!"
            else:
                # Fallback: Engage based on message length/tone - make more curious and interactive
                if len(user_message) < 10:
                    response = f"'{user_message}' – short and sweet! Tell me more about that, or ask about your expenses. I'm genuinely interested!"
                elif any(word in user_lower for word in ['!', 'wow', 'amazing', 'great']):
                    response = "Sounds exciting! I'm glad you're feeling that way. What's making you so pumped? Tell me the story behind it!"
                else:
                    response = f"Thanks for sharing that! '{user_message}' – interesting. Want to dive deeper into that topic or switch to expense talk? I'm here for whatever you want to chat about!"

            return JsonResponse({'response': response})
        except Exception as e:
            return JsonResponse({'response': 'Oops, something went wrong on my end. Try again?'}, status=400)
    return JsonResponse({'response': 'Hmm, that didn\'t work. Let\'s try a proper chat!'}, status=405)
        