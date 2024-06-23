from django.contrib import admin

# Register your models here.

from .models import Ata, Item, Pedido, Resumo, Geral
from produtos.models import Produto
from import_export.admin import ImportExportActionModelAdmin
from django.utils.html import format_html

admin.site.site_header = "Nutri C"

class ItemInline(admin.TabularInline):
    model = Item
    extra = 1
class PedidoInline(admin.TabularInline):
    model = Pedido
    extra = 1

class AtaAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    inlines = (ItemInline,PedidoInline, )
    list_display = ('municipio','data','valor_total_ata','valor_total_pedidos', 'valor_restante')
    search_fields = ('municipio',)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('ata', 'nota_fiscal', 'status', 'prazo_vencido')

    def prazo_colorido(self, obj):
        if obj.prazo_vencido():
            return format_html('<span style="color: red;">{}</span>', obj.prazo)
        return obj.prazo

    prazo_colorido.short_description = 'Prazo'   

admin.site.register(Ata, AtaAdmin)
admin.site.register(Produto)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Resumo)
admin.site.register(Geral)

