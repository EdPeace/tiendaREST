from django.db import models


class ProductManager(models.Manager):

    def productos_por_user(self, usuario):
        return self.filter(user_created=usuario, )

    def productos_con_stock(self):
        return self.filter(stok__gt=0, ).order_by('-num_sales')

    def productos_por_genero(self, genero):
        if genero == "m":
            masculino = True
            femenino = False
        elif genero == "f":
            masculino = False
            femenino = True
        else:
            masculino = True
            femenino = True
        return self.filter(woman=femenino, man=masculino).order_by('created')

    def filtrar_productos(self, **filtros):
        return self.filter(man=filtros['man'], woman=filtros['woman'], name__icontains=filtros['name'])
