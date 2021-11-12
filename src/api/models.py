from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Sum


class Portifolio(models.Model):
    """
    Portifolio Model
    Defines the attributes of a portifolio
    """
    class Meta:
        ordering = ["id", ]

    def __str__(self):
        return (str(self.id))


VENDA = "VENDA"
COMPRA = "COMPRA"
OPERATIONTYPE = [
    (VENDA, "VENDA"),
    (COMPRA, "COMPRA"),
]


class Trade(models.Model):
    """
    Ativo Model
    Defines the attributes of a trade
    """

    portifolio = models.ForeignKey(
        Portifolio, related_name="trades", on_delete=models.CASCADE,)

    ativo = models.CharField(max_length=255)
    operacao = models.CharField(
        max_length=10,
        choices=OPERATIONTYPE,
        default=COMPRA,
    )
    data = models.DateField()
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(
        max_digits=11, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    custos = models.DecimalField(
        max_digits=11, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        ordering = ["ativo", "data", "id"]

    def __str__(self):
        return (f'{str(self.id)} - {self.ativo}')

    @property
    def daytrade(self):
        """operações iniciadas e terminadas no mesmo dia com o mesmo ativo"""
        if self.operacao == COMPRA:
            conter_operation = VENDA
        else:
            conter_operation = COMPRA

        conter_trades = Trade.objects.exclude(pk=self.pk).filter(
            data=self.data, ativo=self.ativo, operacao=conter_operation)
        return len(conter_trades) > 0

    @property
    def quantidade_acumulada(self):
        buys = Trade.objects.filter(
            data__lte=self.data, ativo=self.ativo, operacao=COMPRA).aggregate(
            quantity=Sum(F('quantidade')))['quantity'] or 0
        sells = Trade.objects.filter(
            data__lte=self.data, ativo=self.ativo, operacao=VENDA).aggregate(
            quantity=Sum(F('quantidade')))['quantity'] or 0
        return (buys - sells)

    @property
    def preco_medio(self):
        quantidade_acumulada = self.quantidade_acumulada
        if quantidade_acumulada == 0:
            return None

        buys = Trade.objects.filter(
            data__lte=self.data, ativo=self.ativo, operacao=COMPRA).aggregate(
            cost=Sum((F('preco')*F('quantidade'))+F('custos')))['cost'] or 0
        sells = Trade.objects.filter(
            data__lte=self.data, ativo=self.ativo, operacao=VENDA).aggregate(
            cost=Sum((F('preco')*F('quantidade'))-F('custos')))['cost'] or 0

        return (buys - sells)/quantidade_acumulada

    @property
    def lucro(self):

        if self.operacao == COMPRA:
            return None

        buys = Trade.objects.exclude(pk=self.pk).filter(
            data__lte=self.data, ativo=self.ativo, operacao=COMPRA)

        sells = Trade.objects.exclude(pk=self.pk).filter(
            data__lte=self.data, ativo=self.ativo, operacao=VENDA)

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

        return ((self.preco - last_average_price)*self.quantidade) - self.custos
