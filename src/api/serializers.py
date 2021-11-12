from django.db import transaction
from django.db.models import F, Sum
from rest_framework import serializers

from api.models import COMPRA, VENDA, Portifolio, Trade


def quantidade_acumulada(instance):
    buys = Trade.objects.filter(
        data__lte=instance.data, ativo=instance.ativo, operacao=COMPRA).aggregate(
        quantity=Sum(F('quantidade')))['quantity'] or 0
    sells = Trade.objects.filter(
        data__lte=instance.data, ativo=instance.ativo, operacao=VENDA).aggregate(
        quantity=Sum(F('quantidade')))['quantity'] or 0
    return (buys - sells)


def preco_medio(instance):
    quantidade_acumulada = instance.quantidade_acumulada
    if quantidade_acumulada == 0:
        return None

    buys = Trade.objects.filter(
        data__lte=instance.data, ativo=instance.ativo, operacao=COMPRA).aggregate(
        cost=Sum((F('preco')*F('quantidade'))+F('custos')))['cost'] or 0
    sells = Trade.objects.filter(
        data__lte=instance.data, ativo=instance.ativo, operacao=VENDA).aggregate(
        cost=Sum((F('preco')*F('quantidade'))-F('custos')))['cost'] or 0

    return (buys - sells)/quantidade_acumulada


def lucro(instance):

    if instance.operacao == COMPRA:
        return None

    buys = Trade.objects.exclude(pk=instance.pk).filter(
        data__lte=instance.data, ativo=instance.ativo, operacao=COMPRA)

    sells = Trade.objects.exclude(pk=instance.pk).filter(
        data__lte=instance.data, ativo=instance.ativo, operacao=VENDA)

    last_buys_quantity = buys.aggregate(
        quantity=Sum((F('quantidade'))))['quantity'] or 0
    last_buys_cost = buys.aggregate(
        cost=Sum((F('preco')*F('quantidade'))+F('custos')))['cost'] or 0
    last_sells_quantity = sells.aggregate(
        quantity=Sum((F('quantidade'))))['quantity'] or 0
    last_sells_cost = sells.aggregate(
        cost=Sum((F('preco')*F('quantidade'))+F('custos')))['cost'] or 0

    last_average_price = (last_buys_cost - last_sells_cost) / \
        (last_buys_quantity - last_sells_quantity)

    return ((instance.preco - last_average_price)*instance.quantidade) - instance.custos


class TradeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Trade
        fields = ['id', 'ativo', 'operacao', 'data', 'quantidade', 'preco',
                  'custos', 'daytrade', 'preco_medio', 'quantidade_acumulada', 'lucro']


class PortifolioSerializer(serializers.ModelSerializer):
    trades = TradeSerializer(many=True)

    class Meta:
        model = Portifolio
        fields = ['trades', ]

    @transaction.atomic
    def create(self, validated_data):
        if "trades" in validated_data.keys():
            trades_data = validated_data.pop("trades")
        else:
            trades_data = []

        portifolio = Portifolio.objects.create(**validated_data)
        for trade_data in trades_data:

            Trade.objects.create(portifolio=portifolio, **trade_data)
        return portifolio
