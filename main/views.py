from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.forms import SignUpForm, CollectionForm, CardForm
from main.models import Collection, Card


class HomeView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['collections'] = Collection.objects.filter(user=self.request.user).prefetch_related('cards')
        return context


class SignUpAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({"ok": True})
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)


class LoginAjaxView(View):
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"ok": True})
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)


class CreateCollectionAjaxView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.user = request.user
            collection.save()
            return JsonResponse({"ok": True, "id": collection.id, "name": collection.name})
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)


class DeleteCollectionAjaxView(LoginRequiredMixin, View):
    def post(self, request, collection_id, *args, **kwargs):
        try:
            collection = Collection.objects.get(id=collection_id, user=request.user)
            collection.delete()
            return JsonResponse({"ok": True})
        except Collection.DoesNotExist:
            return JsonResponse({"ok": False, "errors": "Collection not found"}, status=404)


class UpdateCollectionAjaxView(LoginRequiredMixin, View):
    def post(self, request, collection_id, *args, **kwargs):
        try:
            collection = Collection.objects.get(id=collection_id, user=request.user)
            form = CollectionForm(request.POST, instance=collection)
            if form.is_valid():
                form.save()
                return JsonResponse({"ok": True})
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)
        except Collection.DoesNotExist:
            return JsonResponse({"ok": False, "errors": "Collection not found"}, status=404)


class CreateCardAjaxView(LoginRequiredMixin, View):
    def post(self, request, collection_id, *args, **kwargs):
        try:
            collection = Collection.objects.get(id=collection_id, user=request.user)
            form = CardForm(request.POST, request.FILES)
            if form.is_valid():
                card = form.save(commit=False)
                card.collection = collection
                card.save()
                return JsonResponse({"ok": True, "id": card.id})
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)
        except Collection.DoesNotExist:
            return JsonResponse({"ok": False, "errors": "Collection not found"}, status=404)


class UpdateCardAjaxView(LoginRequiredMixin, View):
    def post(self, request, card_id, *args, **kwargs):
        try:
            card = Card.objects.get(id=card_id, collection__user=request.user)
            form = CardForm(request.POST, request.FILES, instance=card)
            if form.is_valid():
                form.save()
                return JsonResponse({"ok": True})
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)
        except Card.DoesNotExist:
            return JsonResponse({"ok": False, "errors": "Card not found"}, status=404)


class DeleteCardAjaxView(LoginRequiredMixin, View):
    def post(self, request, card_id, *args, **kwargs):
        try:
            card = Card.objects.get(id=card_id, collection__user=request.user)
            card.delete()
            return JsonResponse({"ok": True})
        except Card.DoesNotExist:
            return JsonResponse({"ok": False, "errors": "Card not found"}, status=404)


