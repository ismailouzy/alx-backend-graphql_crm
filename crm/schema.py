import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.core.validators import RegexValidator
from django.utils import timezone
from crm.models import Customer, Product, Order
from crm.filters import CustomerFilter, ProductFilter, OrderFilter

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        filterset_class = ProductFilter

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilter

# ... Mutation classes stay the same ...

class Query(graphene.ObjectType):
    hello = graphene.String()
    all_customers = DjangoFilterConnectionField(CustomerType, order_by=graphene.List(of_type=graphene.String))
    all_products = DjangoFilterConnectionField(ProductType, order_by=graphene.List(of_type=graphene.String))
    all_orders = DjangoFilterConnectionField(OrderType, order_by=graphene.List(of_type=graphene.String))

    def resolve_hello(root, info):
        return "Hello, GraphQL!"

# graphql_crm/schema.py
import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation

class Query(CRMQuery, graphene.ObjectType):
    pass

class Mutation(CRMMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

