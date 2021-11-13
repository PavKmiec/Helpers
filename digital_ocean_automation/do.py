import time
import requests

url = 'https://api.digitalocean.com/v2/droplets'
api_key = '<your-api-key>'
headers = { 'Authorization': 'Bearer {}'.format(api_key) }



'''
# Check if droplet exists
'''
def check_droplet_exists(name, headers = headers):
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        for droplet in r.json()['droplets']:
            if droplet['name'] == name:
                return True
    return False


'''
# Create droplet
    name: Name of the droplet
    region: Region of the droplet
    size: Size of the droplet
    image: Image of the droplet
    user_data: User data to be passed to the droplet (useful for startup scripts)
'''
def create_droplet(name, region='lon1', size='s-1vcpu-1gb', image='ubuntu-20-04-x64', user_data=None, headers = headers):
    droplet_exists = check_droplet_exists(name, headers)
    if droplet_exists:
        print('Droplet {} already exists'.format(name))
        return False
    else:
        data = {
            'name': name,
            'region': region,
            'size': size,
            'image': image,
            'user_data': user_data
        }

        r = requests.post(url, headers=headers, data=data)
        if r.status_code == 202:
            print('Droplet created')
            print(r.json()['droplet']['id'])
            return r.json()['droplet']['id']
        else:
            print('Error creating droplet')

'''
# get droplet public IP
    droplet_id: ID of the droplet
    headers: Headers to be passed to the API
'''
def get_droplet_ip(droplet_id, headers = headers):
    r = requests.get(url + '/{}'.format(droplet_id), headers=headers)
    if r.status_code == 200:
        return r.json()['droplet']['networks']['v4'][0]['ip_address']
    else:
        print('Error getting droplet ip')


#create_droplet('test', region='lon1', size='s-1vcpu-1gb', image='ubuntu-20-04-x64', user_data=None)

