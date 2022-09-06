from datetime import datetime
import json
from MercadoLibreApi import MercadoLibreApi
from Class.Product import Product
from Utility import getDataFormExcelFile, getFilesNames, moveFiles, toJSON, tryParseFloat, tryParseInt, getConfiguration, SetConfiguration

def getAttributes(data, attributesPosition):
    attributes = {}
    for key in attributesPosition.keys():
        value = data[attributesPosition[key]]
        if tryParseInt(value) is not None:
            value = str(tryParseInt(value))
        elif tryParseFloat(value) is not None:
            value = str(tryParseFloat(value))
            
        attributes[key] = value

    return attributes

def getProductFormExcelFile(excelFilePath, productoParserPath):

    with open(productoParserPath) as json_file:
        productoParser = json.load(json_file)

    products = {}

    for data in getDataFormExcelFile(excelFilePath, productoParser["type"]):
        if data[productoParser["title"]] == "":
            break

        if(data[productoParser["title"]] in products.keys()):
            product = products[data[productoParser["title"]]]

            combination = getAttributes(data, productoParser["variations"]["combionation"])
            combionationAttributes = getAttributes(data, productoParser["variations"]["attributes"])

            product.AddVariations(data[productoParser["price"]],
                data[productoParser["available_quantity"]],
                data[productoParser["variations"]["attributes"]["SELLER_SKU"]],
                combination,
                combionationAttributes,
                data[productoParser["pictures"]].split(","))
        else:
            product = Product(data[productoParser["title"]],
                data[productoParser["price"]],
                data[productoParser["available_quantity"]],
                productoParser["categoryId"],
                data[productoParser["description"]],
                productoParser["accepts_mercadopago"])

            attributes = getAttributes(data, productoParser["attributes"])
            combination = getAttributes(data, productoParser["variations"]["combionation"])
            combionationAttributes = getAttributes(data, productoParser["variations"]["attributes"])

            product.AddAttributes(attributes)
            product.AddVariations(data[productoParser["price"]],
                data[productoParser["available_quantity"]],
                data[productoParser["variations"]["attributes"]["SELLER_SKU"]],
                combination,
                combionationAttributes,
                data[productoParser["pictures"]].split(","))

        products[data[productoParser["title"]]] = product
    return products 

def upLoadProduct(products):
    mercadoLibreApi = MercadoLibreApi()
    for key, product in products.items():

        skus = [variation.seller_custom_field for variation in product.variations]
        publicationsIds = mercadoLibreApi.getPublicationsIDBySKU(skus)
        
        if  len(publicationsIds) == 0:
            publicationId = mercadoLibreApi.addPublication(toJSON(product))
            mercadoLibreApi.addDescription(publicationId, toJSON(product.description))


productoParserFilesNames = getFilesNames(getConfiguration("Files","productTypeExcelDataParserPath"))
excelFileToProccess = getFilesNames(getConfiguration("Files","excelFilePathToProccess"))
excelFileProccessed = getConfiguration("Files","excelFilePathProccessed")
excelFilePathError = getConfiguration("Files","excelFilePathError")

for fileToProccess in excelFileToProccess:
    try:
        for productoParserFilesName in productoParserFilesNames:
            products = getProductFormExcelFile(fileToProccess, productoParserFilesName)
            if len(products) > 0:
                upLoadProduct(products)
        
        moveFiles(fileToProccess, excelFileProccessed)
    except Exception as e:
            print(e)
            moveFiles(fileToProccess, excelFilePathError)

SetConfiguration("Run", "lastUpload", datetime.now().strftime(getConfiguration("App", "dateFormat")))
