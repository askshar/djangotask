from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=155)
    order = models.IntegerField(default=0, null=True, blank=True)
    parent_id = models.ForeignKey(
            "self",
            on_delete=models.CASCADE,
            related_name="subcategories",
            null=True, blank=True
        )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=155, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    categories = models.ManyToManyField(Category, related_name="product_category")

    def __str__(self):
        return self.name