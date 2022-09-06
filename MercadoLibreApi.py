import requests
import json
from Utility import getConfiguration

class MercadoLibreApi():
    urlGetPublicationsIDBySKU       = "https://api.mercadolibre.com/users/{UserId}/items/search?seller_sku={Sku}"
    urlGetVariaciones               = "https://api.mercadolibre.com/items/{PublicationId}?attributes=variations"
    urlAddPublication               = "https://api.mercadolibre.com/items"
    urlUpdatePublication            = "https://api.mercadolibre.com/items/{PublicationId}"
    urlAddPublicationDescription    = "https://api.mercadolibre.com/items/{PublicationId}/description"
    urlTokenRefresh                 = "https://api.mercadolibre.com/oauth/token"
   
    def __init__(self):
        self.userId = getConfiguration("MercadoLibre","userId")
        self.clientId = getConfiguration("MercadoLibre","clientId")
        self.clientSecret = getConfiguration("MercadoLibre","clientSecret")
        self.refreshToken = getConfiguration("MercadoLibre","refreshToken")
        self.authToken = self.getAuthToken()
  
    def getAuthHeader(self):
        return {
        'Authorization': 'Bearer ' + self.authToken,
        'Content-Type': 'application/json'
        }
    
    def getAuthToken(self):

        headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded'
        }

        data='grant_type=refresh_token&client_id={clientId}&client_secret={clientSecret}&refresh_token={refreshToken}'.format(clientId = self.clientId, clientSecret = self.clientSecret, refreshToken = self.refreshToken)

        response = requests.request("POST", self.urlTokenRefresh, headers=headers, data=data)
        if (response.status_code == 200):
            responseData = json.loads(response.text)
            return responseData["access_token"]

    def getPublicationsIDBySKU(self, skus):
        url = self.urlGetPublicationsIDBySKU.format(UserId = self.userId, Sku = ','.join(skus))
        response = requests.request("GET", url, headers=self.getAuthHeader())
        print(response.text)
        if (response.status_code == 200):
            responseData = json.loads(response.text)
            if(len(responseData["results"]) > 0):
                return responseData["results"]
            else:
                return {}

    def addPublication(self, data):
        print(data)
        response = requests.request("POST", self.urlAddPublication, headers=self.getAuthHeader(), data=data)
        print(response.text)
        if response.status_code == 201:
            responseData = json.loads(response.text)
            return responseData["id"]

    def addDescription(self, publicationId, description):
        url = self.urlAddPublicationDescription.format(PublicationId = publicationId)
        response = requests.request("POST", url, headers=self.getAuthHeader(), data=description)
        print(response.text)

    def getVariationBySKU(self, sku):
        variationId = 0
        variationPrice = 0
        variationQuantity = 0
        variationWithSKULen = 0
        
        publicationsId = self.getPublicationsIDBySKU([sku])
        if len(publicationsId) == 0:
            return 0, 0, 0, 0

        publicationsId = publicationsId[0]
        url =  self.urlGetVariaciones.format(PublicationId = publicationsId)
        response = requests.request("GET", url, headers=self.getAuthHeader())

        if response.status_code == 200:
            responseData = json.loads(response.text)
            for variation in responseData["variations"]:
                if sku == variation["seller_custom_field"]:
                    variationId = variation["id"]
                    variationPrice = variation["price"]
                    variationQuantity = variation["available_quantity"]
                    variationWithSKULen += 1
        
        
        if(variationWithSKULen == 1):
            return publicationsId, variationId, variationPrice, variationQuantity
        else:
            return publicationsId, 0, 0, 0

    def updateVariationQuantity(self, publicationsId, variationId, quantity):

        url = self.urlUpdatePublication.format(PublicationId = publicationsId)
        data = {
                "variations": [{
                    "id": variationId,
                    "available_quantity": quantity
                    }]
                }
        response = requests.request("PUT", url, headers=self.getAuthHeader(), data=json.dumps(data))
        print(response.text)