from django.contrib import admin
from django.urls import reverse
# Register your models here.

from .models import Ata, Item, Pedido, Resumo, Geral, Municipio
from produtos.models import Produto
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from django.utils.html import format_html

admin.site.site_header = "Nutri C"

class ItemInline(admin.StackedInline):
    model = Item
  
    extra = 1
class PedidoInline(admin.StackedInline):
    model = Pedido
    extra = 1

class PedidoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('ata',)

class AtaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    
    inlines = (ItemInline,PedidoInline, )
    list_display = ('municipio','data','valor_total_ata','valor_total_pedidos', 'valor_restante')
    search_fields = ('municipio',)


class AtaInline(admin.TabularInline):
    model = Ata
    extra = 1



class MunicipioAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('nome', 'view_atas')  # Include the custom method in list display
    inlines = [AtaInline]

    def view_atas(self, obj):
       
        atas = Ata.objects.filter(municipio=obj)
        links = []
        for ata in atas:
            url = reverse('admin:sistema_ata_change', args=[ata.id])
            link = format_html('<a href="{}">{}</a>', url, ata)
            links.append(link)
        return format_html('<br>'.join(links))

    view_atas.short_description = 'Atas'

class ProdutoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass

admin.site.register(Municipio, MunicipioAdmin)


admin.site.register(Ata, AtaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Resumo)
admin.site.register(Geral)
