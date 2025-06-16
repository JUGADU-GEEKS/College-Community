from model import Product

apron_c = Product.get_product_number_by_name('Apron')
drafter_c = Product.get_product_number_by_name('Drafter')
labcoat_c = Product.get_product_number_by_name('Labcoat')
calculator_c = Product.get_product_number_by_name('Calculator')
books_c = Product.get_product_number_by_name('Books')

print(apron_c, drafter_c, labcoat_c, calculator_c, books_c)