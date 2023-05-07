def create_overpass_query(query, overpass_host='https://maps.mail.ru/osm/tools/overpass'):
    """
     Создает запрос к заданному экземпляру Overpass API.

     query - запрос
    """
    full_query = f"""
        [out:json][timeout:25];
        {query}
        convert item ::=::, ::geom=geom(), _osm_type=type(), ::id=id();
        out geom;
    """
    return f"{overpass_host}/api/interpreter?data={full_query}"
