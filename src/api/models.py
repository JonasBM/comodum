from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


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
    Trade Model
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

    quantidade_acumulada = models.PositiveIntegerField(blank=True, null=True)
    preco_medio = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        blank=True,
        null=True
    )
    lucro = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        blank=True,
        null=True
    )

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
