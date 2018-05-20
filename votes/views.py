from rest_framework import generics
from rest_framework.renderers import (
    BrowsableAPIRenderer,
    JSONRenderer,
    TemplateHTMLRenderer,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.shortcuts import redirect
from .models import Vote
from .serializers import VoteSerializer


# class VoteList(generics.ListCreateAPIView):
#     renderer_classes = (
#         BrowsableAPIRenderer,
#         JSONRenderer,
#         TemplateHTMLRenderer,
#     )
#     template_name = "vote_list.html"
#     queryset = Vote.objects.all()
#     serializer_class = VoteSerializer
#
#     def create(self, request, *args, **kwargs):
#         response = super(VoteList, self).create(request, *args, **kwargs)
#
#         if request.accepted_renderer.format == 'html' and response.status_code == 201:
#             return redirect('/votes/')
#         return response


class VoteAPIMixin:
    render_classes = [JSONRenderer, TemplateHTMLRenderer]
    queryset = Vote.objects.all().order_by("vote_taken")
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_renderers(self):  # not working? anyone can still access API
        render_classes = self.render_classes
        if self.request.user.is_staff:
            render_classes += [BrowsableAPIRenderer]
        return [renderer() for renderer in render_classes]


class VoteList(VoteAPIMixin, generics.ListCreateAPIView):

    template_name = "vote_list.html"

    def create(self, request, *args, **kwargs):
        response = super(VoteList, self).create(request, *args, **kwargs)

        if request.accepted_renderer.format == "html" and response.status_code == 201:
            return redirect("/votes/")
        return response


# class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
#     renderer_classes = (
#         BrowsableAPIRenderer,
#         JSONRenderer,
#         TemplateHTMLRenderer,
#     )
#     template_name = "vote.html"
#     queryset = Vote.objects.all()
#     serializer_class = VoteSerializer


class VoteDetail(VoteAPIMixin, generics.RetrieveUpdateDestroyAPIView):
    template_name = "vote.html"
