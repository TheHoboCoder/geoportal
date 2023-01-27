from geo.Geoserver import Geoserver
from .settings import GEOSERVER, DATABASES
from geo.Geoserver import GeoserverException

def get_geoserver():
    return Geoserver(f"http://{GEOSERVER['HOST']}:{GEOSERVER['PORT']}/geoserver", 
                     username=GEOSERVER["USER"], password=GEOSERVER["PASSWORD"])

def install_module(geo_server: Geoserver, module_name: str, models):

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


def delete_module(geo_server: Geoserver, module_name: str):
    geo_server.delete_workspace(module_name)

    

    




