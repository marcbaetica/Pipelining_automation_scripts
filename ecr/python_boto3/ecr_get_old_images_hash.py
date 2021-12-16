import boto3, pprint
from operator import itemgetter

ecrClient = boto3.client('ecr')
pp = pprint.PrettyPrinter(indent=4)

# Set aws credentials for API calls


def get_registry_name():
	regs = ecrClient.describe_repositories()['repositories']
	registries = [x['repositoryName'] for x in regs]
	name = [x for x in registries if 'syslog' in x and 'test' in x][0]
	print(f'Registry name: {name}')
	return name


def get_images_descriptions_sorted_by_creation_time(registry):
	images_descriptions = ecrClient.describe_images(repositoryName = registry)['imageDetails']
	for x in images_descriptions:
		del x['imageSizeInBytes']
		del x['repositoryName']
		del x['registryId']
	return sorted(images_descriptions, key=itemgetter('imagePushedAt'), reverse=True)


# Get list excluding the 5 most recent images.
def get_sha_list_of_old_images(descriptions, amount_to_retain):
	total_sha_list = [x['imageDigest'] for x in descriptions]
	print(f'\nThe total amount of SHAs before selection is {len(total_sha_list)}. Skipping the first {amount_to_retain}.')
	return [total_sha_list[x].split(':')[1] for x in range(5, len(total_sha_list))]


def get_list_of_old_images_sha(images_list):
	print('\nSHAs of docker images to account for:')
	pp.pprint(images_list)


registryName = get_registry_name()
sorted_images_descriptions = get_images_descriptions_sorted_by_creation_time(registryName)

print('The list of docker images (together with their respective descriptions) sorted from the newest to the oldest:')
pp.pprint(sorted_images_descriptions)

# From the images list description get SHAs of old images (ignoring the first 5).
filtered_images = get_sha_list_of_old_images(sorted_images_descriptions, 5)

get_list_of_old_images_sha(filtered_images)
