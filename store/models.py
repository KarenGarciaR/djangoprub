from django.db import models
from django.contrib.auth.models import User

MEXICAN_STATES = [
    ('AGU', 'Aguascalientes'),
    ('BCN', 'Baja California'),
    ('BCS', 'Baja California Sur'),
    ('CAM', 'Campeche'),
    ('CHP', 'Chiapas'),
    ('CHH', 'Chihuahua'),
    ('COA', 'Coahuila'),
    ('COL', 'Colima'),
    ('DIF', 'Ciudad de México'),
    ('DUR', 'Durango'),
    ('GUA', 'Guanajuato'),
    ('GRO', 'Guerrero'),
    ('HGO', 'Hidalgo'),
    ('JAL', 'Jalisco'),
    ('MEX', 'Estado de México'),
    ('MIC', 'Michoacán'),
    ('MOR', 'Morelos'),
    ('NAY', 'Nayarit'),
    ('NLE', 'Nuevo León'),
    ('OAX', 'Oaxaca'),
    ('PUE', 'Puebla'),
    ('QRO', 'Querétaro'),
    ('QRO', 'Quintana Roo'),
    ('SLP', 'San Luis Potosí'),
    ('SIN', 'Sinaloa'),
    ('SON', 'Sonora'),
    ('TAB', 'Tabasco'),
    ('TAM', 'Tamaulipas'),
    ('TLX', 'Tlaxcala'),
    ('VER', 'Veracruz'),
    ('YUC', 'Yucatán'),
    ('ZAC', 'Zacatecas'),
]

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    referencias = models.CharField(max_length=250, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(
        max_length=3,
        choices=MEXICAN_STATES,
        blank=True,
        null=True
    )
    municipality = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else self.email

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Animales', 'Animales'),
        ('Arte Digital', 'Arte Digital'),
        ('Frases Motivadoras', 'Frases Motivadoras'),
    ]
    MATERIAL_CHOICES = [
        ('Vinil', 'Vinil'),
        ('Papel Adhesivo', 'Papel Adhesivo'),
        ('Transparente', 'Transparente'),
        ('Holográfico', 'Holográfico'),
        ('Otro', 'Otro'),
    ]
    FINISH_CHOICES = [
        ('Mate', 'Mate'),
        ('Brillante', 'Brillante'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, null=True, blank=True)
    price = models.FloatField()
    offer_price = models.FloatField(null=True, blank=True)
    offer = models.BooleanField(default=False)
    quantity = models.IntegerField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    height_cm = models.FloatField()
    width_cm = models.FloatField()
    material = models.CharField(max_length=50, choices=MATERIAL_CHOICES)
    finish = models.CharField(max_length=50, choices=FINISH_CHOICES)
    likes = models.ManyToManyField(User, related_name='liked_products', blank=True)
    date_of_delivery = models.DateField(null=True, blank=True)

    image = models.ImageField(null=True, blank=False)
    imageuno = models.ImageField(null=True, blank=False)
    imagedos = models.ImageField(null=True, blank=False)
    imagetres = models.ImageField(null=True, blank=False)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    @property
    def imageunoURL(self):
        try:
            url = self.imageuno.url
        except:
            url = ''
        return url
    
    @property
    def imagedosURL(self):
        try:
            url = self.imagedos.url
        except:
            url = ''
        return url
    
    @property
    def imagetresURL(self):
        try:
            url = self.imagetres.url
        except:
            url = ''
        return url

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Procesando', 'Procesando'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
        ('Cancelado', 'Cancelado'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendiente')
    estimated_delivery = models.DateField(null=True, blank=True)
    custom_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Orden #{self.id} - {self.customer}'

    @property
    def get_cart_items(self):
        return sum(item.quantity for item in self.orderitem_set.all())

    @property
    def get_cart_total(self):
        return sum(item.get_total for item in self.orderitem_set.all())

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return (self.product.offer_price if self.product.offer else self.product.price) * self.quantity

class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"Historial de {self.user.username}"

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Personalizacion(models.Model):
    STATUS_CHOICES = [
        ('PENDIENTE',    'Pendiente'),
        ('EN_PROGRESO',  'En progreso'),
        ('RESPONDIDA',   'Respondida'),
    ]

    cliente          = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    descripcion      = models.TextField()
    fecha_creacion   = models.DateTimeField(auto_now_add=True)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDIENTE')
    respuesta_admin  = models.TextField(null=True, blank=True)
    atendido_por     = models.ForeignKey(User, on_delete=models.SET_NULL,
                                        null=True, blank=True,
                                        related_name='personalizaciones_atendidas')

    def __str__(self):
        who = self.cliente.user.username if self.cliente and self.cliente.user else "Invitado"
        return f"#{self.pk} - {who}"

class Comment(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.message}"