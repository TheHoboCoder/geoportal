import numpy as np

def create_overpass_query(query, 
                          overpass_host='https://maps.mail.ru/osm/tools/overpass'):
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

class RangeConverter:
    """Преобразует значение из одного диапазона в другой.
       Может использоваться для создания цветовых шкал.
    """
    def __init__(self, ranges, min_value=None, max_value=None):
        """
        Args:
            ranges (tuple|list): список кортежей:
                ( (минИсходногоДиапазона, максИсходногоДиапазона), 
                  (минЦелевогоДиапазона, максЦелевогоДиапазона) )
            Значения границ исходного диапазона должны быть числом.
            При этом мин < макс
            Значения границ целевого диапазона могут быть как числом, так и вектором.
            min_value (number|tuple) - значение, которое будет возвращено, если
                значение меньше минимума первого диапазона. Если не указано, то будет
                использовано значение минимума целевого диапазона.
            max_value (number|tuple) - аналогично.

        """
        self.ranges = sorted(ranges, key=lambda r: r[0][0])
        self.min_value = min_value
        self.max_value = max_value
        if self.min_value is None:
            self.min_value = self.ranges[0][1][0]
        if self.max_value is None:
            self.max_value = self.ranges[-1][1][1]
    
    def find_range(self, value):
        for r in self.ranges:
            (minS, maxS), _ = r
            if value >= minS and value <= maxS:
                return r
        return None

    def convert(self, value):
        found_range = self.find_range(value)
        if found_range is None:
            if value < self.ranges[0][0][0]:
                return self.min_value
            return self.max_value
        (minS, maxS), (minD, maxD) = self.find_range(value)
        startD = np.array(minD)
        distVector = (np.array(maxD) - startD) / (maxS - minS)
        return startD + distVector * (value - minS)

