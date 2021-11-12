from rest_framework import generics, permissions
from rest_framework.response import Response

from api.authentication import APIKeyAuthentication
from api.models import Portifolio, Trade
from api.serializers import PortifolioSerializer, TradeSerializer
from rest_framework import generics, permissions, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response


class PortifolioView(generics.CreateAPIView):
    """
    Password change view
    Only allow changing own password
    """
    model = Portifolio
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PortifolioSerializer

    def post(self, request, *args, **kwargs):
        Portifolio.objects.all().delete()

        # portifolio = Portifolio.objects.create()
        # trades_result = []

        # for trade in request.data['trades']:
        #     instance = Trade.objects.create(**trade, portifolio=portifolio)
        #     trades_result.append(TradeSerializer(instance).data)
        #     print(instance)

        # return Response({"trades": trades_result}, status=status.HTTP_200_OK)
        return self.create(request, *args, **kwargs)
