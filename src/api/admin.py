from django.contrib import admin

from api.models import Portifolio, Trade


admin.site.register(Portifolio)


# admin.site.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    search_fields = ['inscricao_imobiliaria', 'codigo', ]

    fields = ('ativo', 'operacao', 'data', 'quantidade', 'preco', 'custos',
              'daytrade', 'preco_medio', 'quantidade_acumulada', 'lucro')

    readonly_fields = ('daytrade', 'preco_medio',
                       'quantidade_acumulada', 'lucro',)


admin.site.register(Trade, TradeAdmin)
