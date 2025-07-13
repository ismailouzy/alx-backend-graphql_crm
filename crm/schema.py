import graphene
from crm.models import Product

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        dummy = graphene.Boolean()

    updated = graphene.List(graphene.String)
    message = graphene.String()

    def mutate(self, info, dummy=False):
        low_stock = Product.objects.filter(stock__lt=10)
        names = []
        for p in low_stock:
            p.stock += 10
            p.save()
            names.append(p.name)
        return UpdateLowStockProducts(updated=names, message="Restocked products successfully")

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
