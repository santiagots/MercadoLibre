from datetime import datetime
from typing import List
from MercadoLibreApi import MercadoLibreApi
from SQL import getProductSold
from Utility import getConfiguration, SetConfiguration, LogInfo, LogError
from Class.Sale import Sale


LogInfo("INICIO DE ACTUALIZACION DE VARIACIONES")
lastUpdate = getConfiguration("Run","lastupdate")

LogInfo("buscando productos vendidos desde {}".format(lastUpdate))
sales:List[Sale] = getProductSold(lastUpdate)
LogInfo("se han encuentrado {} productos vendidos".format(len(sales)))

for sale in sales:
    mercadoLibreApi = MercadoLibreApi()
    
    LogInfo("SKU {} buscando variaciones".format(sale.Sku))
    publicationsId, variationId, price, availableQuantity = mercadoLibreApi.getVariationBySKU(sale.Sku)
    if(publicationsId == 0):
        LogInfo("SKU {} Producto no publicado".format(sale.Sku, sale.Quantity, availableQuantity))
        continue

    if(variationId != 0):
        availableQuantity -= sale.Quantity
        LogInfo("SKU {} Actualizando VENTAS {} CANTIDAD DISP. {}".format(sale.Sku, sale.Quantity, availableQuantity))
        variation = mercadoLibreApi.updateVariationQuantity(publicationsId, variationId, availableQuantity)
    else:
        LogError("SKU {} No se pudo actualizar la cantidad de la publicacion con ID {} SKU {} ya se tiene SKUs repetidos. VENTAS {} actualizar a mano".format(publicationsId, sale.Sku, sale.Quantity))

SetConfiguration("Run", "lastUpdate", datetime.now().strftime(getConfiguration("App", "dateFormat")))
LogInfo("FIN DE ACTUALIZACION DE VARIACIONES")