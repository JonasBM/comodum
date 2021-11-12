from rest_framework import generics, permissions

from api.authentication import APIKeyAuthentication
from api.models import Portifolio
from api.serializers import PortifolioSerializer


class PortifolioView(generics.CreateAPIView):
    """
    PortfolioView view
    Get the trades via post, and process the data
    returning a portfolio serialized model
    """
    model = Portifolio
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PortifolioSerializer

    def post(self, request, *args, **kwargs):
        Portifolio.objects.all().delete()
        return self.create(request, *args, **kwargs)
