class Product: 
	def __init__(self, title, price, available_quantity, category_id, description, accepts_mercadopago):
		self.currency_id= "ARS"
		self.buying_mode= "buy_it_now"
		self.listing_type_id= "gold_special"
		self.condition= "new"
		self.title= title
		self.price= price
		self.description= Description(description)
		self.available_quantity= available_quantity
		self.category_id= category_id
		self.pictures= []
		self.accepts_mercadopago: accepts_mercadopago
		self.sale_terms = []
		self.attributes = []
		self.variations = []

		self.sale_terms.append(SaleTerms())

	def AddPictures(self, sources):
		for source in sources:
			self.pictures.append(Picture(source))

	def AddAttributes(self, attributes):
		for key in attributes.keys():
			self.attributes.append(Attributes(key, attributes[key]))

	def AddVariations(self, price, available_quantity, sku, combionations, combionationAttributes, pictures):
		self.AddPictures(pictures)

		varation = Variation(price,available_quantity,sku)
		varation.AddCombinations(combionations)
		varation.AddAttributes(combionationAttributes)
		varation.AddPictures(pictures)

		self.variations.append(varation)

class SaleTermsValues:
	def __init__(self):
		self.id= "6150835"
		self.name= "Sin garantía"
		self.struct= None


class SaleTerms:
	def __init__(self):
		self.id= "WARRANTY_TYPE"
		self.name= "Tipo de garantía"
		self.value_id= "6150835"
		self.value_name= "Sin garantía"
		self.value_struct= None
		self.values= []
		self.values.append(SaleTermsValues())

class Picture:

    def __init__(self, source):
        self.source = source

class Attributes:

    def __init__(self, id, value_name):
        self.id = id
        self.value_name = value_name

class Variation:

	def __init__(self, price, available_quantity,seller_custom_field):
		self.attribute_combinations = []
		self.price = price
		self.available_quantity = available_quantity
		self.seller_custom_field = seller_custom_field
		self.attributes = []
		self.sold_quantity = 0
		self.picture_ids = []

	def AddCombinations(self, combinations):
		for key in combinations.keys():
			self.attribute_combinations.append(Attributes(key, combinations[key]))

	def AddAttributes(self, attributes):
		for key in attributes.keys():
			self.attributes.append(Attributes(key, attributes[key]))
	
	def AddPictures(self, sources):
		for source in sources:
			self.picture_ids.append(source)

class Description:
	def __init__(self, description):
		self.plain_text = description