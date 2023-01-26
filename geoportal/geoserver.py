from geo.Geoserver import Geoserver
from .settings import GEOSERVER, DATABASES
from geo.Geoserver import GeoserverException

def get_geoserver():
    return Geoserver(f"http://{GEOSERVER['HOST']}:{GEOSERVER['PORT']}/geoserver", 
                     username=GEOSERVER["USER"], password=GEOSERVER["PASSWORD"])

def install_module(geo_server: Geoserver, module_name: str, models):

    try:
        geo_server.create_workspace(workspace=module_name)

        geo_server.create_featurestore(workspace=module_name,
                                   store_name=f"{module_name}_store",  
                                   db=DATABASES['default']['NAME'], 
                                   host=DATABASES['default']['HOST'], 
                                   pg_user=DATABASES['default']['USER'], 
                                   pg_password=DATABASES['default']['PASSWORD'])

        for model in models:
            meta = model.objects.model._meta
            if hasattr(meta, 'gis_model') and meta.gis_model == True:
                geo_server.publish_featurestore(workspace=module_name,
                                                store_name=f"{module_name}_store", 
                                                pg_table=meta.db_table, 
                                                title=meta.layer_name)

    except Exception as geo_e:
        # уже существует, отмена дальнейшей установки
        #print(f"EXCEPTIOON STATUS: {geo_e.status}")
        # if geo_e.status == 409 or geo_e.status == 500:
        #     print("NOTICE: module init was runned several times")
        #     return
        # else:
        #     raise geo_e
        raise geo_e

    

    




