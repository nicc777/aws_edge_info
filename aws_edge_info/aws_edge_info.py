import urllib.request
import json
import traceback

class Prefix:
    def __init__(self, ip_prefix: str, region: str, service: str):
        self.ip_prefix = ip_prefix
        self.region = region
        self.service = service


class Prefixes:
    def __init__(self):
        self.prefixes = list()

    def add_prefix(self, prefix: Prefix):
        if prefix is not None:
            if isinstance(prefix, Prefix):
                self.prefixes.append(prefix)

    def get_service_prefixes(self, service_name: str, region_filter: list=list()):
        result = Prefixes()
        for prefix in self.prefixes:
            if prefix.service == service_name:
                if len(region_filter) > 0:
                    if prefix.region in region_filter:
                        result.add_prefix(prefix=prefix)
                else:
                    result.add_prefix(prefix=prefix)
        return result

    def get_service_names(self, region_filter: list=list()):
        result = list()
        for prefix in self.prefixes:
            if len(region_filter) > 0:
                if prefix.region in region_filter:
                    if prefix.service not in result:                
                        result.append(prefix.service)  
            else:
                if prefix.service not in result:                
                    result.append(prefix.service)     
        return result

    def get_region_names(self):
        result = list()
        for prefix in self.prefixes:
            result.append(prefix.region)
        return result

    def get_ip_prefix(self, region_filter: list=['us-east-1'], service_filter: list=['CLOUDFRONT']):
        result = list()
        if region_filter is None:
            region_filter = self.get_region_names()
        if len(region_filter) < 1:
            region_filter = self.get_region_names()
        if service_filter is None:
            service_filter = self.get_service_names(region_filter=region_filter)
        for prefix in self.prefixes:
            if prefix.region in region_filter:
                if prefix.service in service_filter:
                    result.append(prefix.ip_prefix)
        return result


def get_remote_data()->dict:
    data = None
    try:
        with urllib.request.urlopen('https://ip-ranges.amazonaws.com/ip-ranges.json') as f:
            data = f.read()
        return json.loads(data)
    except:
        print('* Failed to retrieve data\n{}'.format(traceback.format_exc()))
    return data


def parse_data(data: dict)->Prefixes:
    prefixes = Prefixes()
    try:
        if 'prefixes' in data:
            data_prefixes = data['prefixes']
            if isinstance(data_prefixes, list):
                for data_prefix in data_prefixes:
                    if 'ip_prefix' in data_prefix and 'region' in data_prefix and 'service' in data_prefix:
                        prefixes.add_prefix(
                            prefix=Prefix(
                                ip_prefix=data_prefix['ip_prefix'],
                                region=data_prefix['region'],
                                service=data_prefix['service'])
                        )
    except:
        print('* Failed to parse data\n{}'.format(traceback.format_exc()))
    return prefixes


if __name__ == '__main__':
    data = get_remote_data()
    if data is not None:
        print('Retrieved {} bytes in JSON data.'.format(len(data)))
    else:
        print('No data retrieved')

# EOF
