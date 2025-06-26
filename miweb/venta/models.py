from django.db import models


class Cliente(models.Model):
    id_cliente = models.CharField(
        max_length=8,
        primary_key=True,
        error_messages={'max_length': 'el texto debe tener 8 caracteres'},
    )
    ape_nombre = models.CharField(max_length=80)
    fec_registro = models.DateField()
    fec_sistema = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Nombres:{self.ape_nombre}, Dni:{self.id_cliente}"


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nom_prod = models.CharField(max_length=50)
    des_prod = models.TextField(max_length=500)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    estado = models.BooleanField(default=True)
    fec_vencimiento = models.DateField()
    fec_reg = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom_prod} - S/. {self.precio} (Stock: {self.cantidad})"
