from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.forms import SignUpForm, CollectionForm, CardForm, ProfileForm
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
        login_value = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''
        if not login_value or not password:
            return JsonResponse({"ok": False, "errors": {"__all__": ["Username/email and password required."]}}, status=400)
        if '@' in login_value:
            user_by_email = User.objects.filter(email__iexact=login_value).first()
            if not user_by_email:
                return JsonResponse({"ok": False, "errors": {"__all__": ["Invalid email or password."]}}, status=400)
            login_value = user_by_email.username
        user = authenticate(request, username=login_value, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"ok": True})
        return JsonResponse({"ok": False, "errors": {"__all__": ["Invalid username/email or password."]}}, status=400)


class UpdateProfileAjaxView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({"ok": True})
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)


class ChangePasswordAjaxView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        old_password = request.POST.get('old_password') or ''
        new_password1 = request.POST.get('new_password1') or ''
        new_password2 = request.POST.get('new_password2') or ''
        errors = {}
        if not request.user.check_password(old_password):
            errors['old_password'] = ['Current password is wrong.']
        if not new_password1:
            errors['new_password1'] = ['New password is required.']
        elif new_password1 != new_password2:
            errors['new_password2'] = ['Passwords do not match.']
        if errors:
            return JsonResponse({"ok": False, "errors": errors}, status=400)
        request.user.set_password(new_password1)
        request.user.save()
        return JsonResponse({"ok": True})


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
                if request.POST.get('clear_photo'):
                    old_photo = card.photo
                    card.photo = None
                    card.save(update_fields=['photo'])
                    if old_photo:
                        old_photo.delete(save=False)
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


