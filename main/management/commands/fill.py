from django.core.management import BaseCommand
from main.models import TeaProduct, TeaCategory


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        cat4 = TeaCategory.objects.get(id=4)

        items_list = [
            {"name": "Oolong Tea Tie Kuan Yin",
             "description": "One of the most appreciated Oolong teas in China, also known as Blue tea. Its sweet and toasted aroma and its digestive effect make it a delicacy to enjoy after meals. The theine content of Oolong tea is moderate and lower than that of other stimulating plants such as coffee. It is appreciated for its diuretic and digestive properties.",
             "ingredients": "Oolong tea from Fujian (China)",
             "flavour": "Sweet, Creamy",
             "aroma": "Sweet, Roasted",
             "preparation": "Infusion 85 ºC during 3 min",
             "preview": "",
             "price": "7.75",
             "category": cat4},
            {"name": "Milky Oolong Origin China",
             "description": "The dairy flavouring is added to the fresh leaves using a special technique at source, and then subjected to a short oxidation process. Its digestive properties make it perfect for all-day consumption. The theine content of Oolong tea is moderate and lower than that of other stimulating plants such as coffee. It is appreciated for its diuretic and digestive properties.",
             "ingredients": "Oolong tea from China, aroma",
             "flavour": "Sweet, Creamy",
             "aroma": "Sweet",
             "preparation": "Infusion 85 ºC during 3 min",
             "preview": "",
             "price": "8.50",
             "category": cat4},
            {"name": "Oolong Tea Spicy Strawberry",
             "description": "Captivating blend of Oolong tea with spices from Asia and the sweet touch of the strawberry. Oolong tea is also known as Blue tea and its digestive effect makes it ideal to enjoy after meals. The theine content of Oolong tea is moderate and lower than that of other stimulating plants such as coffee. It is appreciated for its diuretic and digestive properties.",
             "ingredients": "Oolong tea, green tea, carob, ginger, cinnamon, split star anise, pineapple, clove, strawberry, cornflower petals and aromas",
             "flavour": "Fruity, Spiced",
             "aroma": "Fruity, Spiced",
             "preparation": "Infusion 85 ºC during 3 min",
             "preview": "",
             "price": "8.95",
             "category": cat4},
            {"name": "Oolong Tea Azahar",
             "description": "Semioxidized Oolong tea that helps digestion and maintains vitality during the day. The orange blossom accompanies this Oolong tea very well for its sweet and floral aromatic notes. The theine content of Oolong is moderate and lower than that of other stimulating plants such as coffee. It is appreciated for its diuretic and digestive properties.",
             "ingredients": "Oolong tea, orange blossom, orange oil, orange aroma",
             "flavour": "Floral, Citrus",
             "aroma": "Sweet",
             "preparation": "Infusion 85 ºC during 3 min",
             "preview": "",
             "price": "7.25",
             "category": cat4}
        ]
        items_instances = [TeaProduct(**item) for item in items_list]

        TeaProduct.objects.bulk_create(items_instances)


