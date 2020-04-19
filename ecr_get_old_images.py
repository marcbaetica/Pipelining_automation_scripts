import boto3, pprint;
from operator import itemgetter;

ecrClient = boto3.client('ecr');
pp = pprint.PrettyPrinter(indent=4);

#set aws credentials for API calls

def getRegistryName():
	regs = ecrClient.describe_repositories()['repositories'];
	registries = [x['repositoryName'] for x in regs];
	name = [x for x in registries if 'syslog' in x and 'test' in x][0];
	print(f'Registry name: {name}');
	return name;

def getImagesDescriptionsSortedByCreationTime(registry):
	imagesDescriptions = ecrClient.describe_images(repositoryName = registry)['imageDetails'];
	for x in imagesDescriptions:
		del x['imageSizeInBytes'];
		del x['repositoryName'];
		del x['registryId'];
	return sorted(imagesDescriptions, key=itemgetter('imagePushedAt'), reverse=True);


#get list excluding the 5 most recent images
def getShaListOfOldImages(list, amountToRetain):
	totalShaList = [x['imageDigest'] for x in sortedImagesDescriptions];
	print(f'\nThe total amount of SHAs before selection is {len(totalShaList)}. Skipping the first {amountToRetain}.');
	return [totalShaList[x].split(':')[1] for x in range(5, len(totalShaList))];

def getLitOfOldImagesSha(imagesList):
	print('\nSHAs of docker images to account for:')
	pp.pprint(imagesList);



registryName = getRegistryName();
sortedImagesDescriptions = getImagesDescriptionsSortedByCreationTime(registryName);

print('The list of docker images (together with their respective descriptions) sorted from the newest to the oldest:');
pp.pprint(sortedImagesDescriptions);

#from the images list description get SHAs of old images (ignoring the first 5)
filteredLimages = getShaListOfOldImages(sortedImagesDescriptions, 5);

getLitOfOldImagesSha(filteredLimages);