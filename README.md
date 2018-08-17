# aws_edge_info
Query the AWS edge data provided by https://ip-ranges.amazonaws.com/ip-ranges.json (as per https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/LocationsOfEdgeServers.html)

## Example Usage

To get all the edge service names:

    >>> from aws_edge_info.aws_edge_info import *
    >>> data = get_remote_data()
    >>> parsed_data = parse_data(data=data)
    >>> parsed_data.get_service_names()
    ['AMAZON', 'ROUTE53_HEALTHCHECKS', 'S3', 'EC2', 'ROUTE53', 'CLOUDFRONT', 'CODEBUILD', 'AMAZON_CONNECT', 'CLOUD9']

The same as above, but only for the region `sa-east-1`:

    >>> parsed_data.get_service_names(region_filter=['sa-east-1'])
    ['AMAZON', 'ROUTE53_HEALTHCHECKS', 'S3', 'EC2', 'CLOUDFRONT', 'CODEBUILD']

Getting the IP prefixes:

    >>> parsed_data.get_ip_prefix(result_as_prefixes=False)
    ['34.226.14.0/24', '34.195.252.0/24', '34.232.163.208/29']
    >>> parsed_data.get_ip_prefix(region_filter=['us-east-1', 'us-east-2'], result_as_prefixes=False)
    ['34.226.14.0/24', '52.15.127.128/26', '18.216.170.128/25', '13.59.250.0/26', '34.195.252.0/24', '34.232.163.208/29']
    >>> parsed_data.get_ip_prefix(region_filter=['us-east-1', 'us-east-2'], service_filter=['CLOUDFRONT', 'S3'], result_as_prefixes=False)
    ['54.231.0.0/17', '52.219.96.0/20', '52.92.16.0/20', '52.219.80.0/20', '52.92.76.0/22', '52.216.0.0/15', '34.226.14.0/24', '52.15.127.128/26', '18.216.170.128/25', '13.59.250.0/26', '34.195.252.0/24', '34.232.163.208/29']

Note: The first run without any arguments sets the region filter to `us-east-1` and the service to `CLOUDFRONT`.

Example to get a random IP address:

    >>> parsed_data.get_random_prefix().get_random_ip_address()
    '34.237.149.129'
    >>> parsed_data.get_random_prefix().get_random_ip_address()
    '18.185.40.162'