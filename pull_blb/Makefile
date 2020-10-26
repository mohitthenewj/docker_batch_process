IMAGE='thenewj.azurecr.io/pullblob:v1'
CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=videobank;AccountKey=+7+BZaxs5zBHwyDAMJHnMEJS1mhzIN4AC6PS7wIbVgE1hd35eHEB9IAbc+E2PfV4GNP7dkFrWiLAVMZ8HgnFEw==;EndpointSuffix=core.windows.net"
MNT_DIR='/data1/code_base/mnt_data/MISC/OD_batch_docker/docker_pull/vids/'
CONTAINER='vbankold'


login-acr:
	sudo az acr login --name thenewj

build-image: ## Build docker image
	docker build -t ${IMAGE} .

tag-iamge:
	docker tag ${IMAGE}

pull-blobs:
	docker run -it --rm --ipc=host -v ${MNT_DIR}:/mnt/data ${IMAGE} python pull_mult_p.py --cont-cli ${CONTAINER} 

push-docker:
	sudo docker push ${IMAGE}