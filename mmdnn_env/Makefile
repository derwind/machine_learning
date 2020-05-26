TARGET = pretrained.pt
INTERMEDIATE = VGG_ILSVRC_19.pt
CAFFEMODEL = VGG_ILSVRC_19_layers.caffemodel
PROTOTXT = VGG_ILSVRC_19_layers_deploy.prototxt

.PHONY: build_image clean $(CAFFEMODEL) $(PROTOTXT)

all: $(TARGET)

$(TARGET): build_image $(INTERMEDIATE)
	python convert.py $(INTERMEDIATE) $@

build_image:
	docker image ls | grep local/mmdnn > /dev/null || docker image build . -t local/mmdnn:0.2.5

$(INTERMEDIATE): $(CAFFEMODEL) $(PROTOTXT)
	docker run -it --rm -v $(PWD):/mnt local/mmdnn:0.2.5 bash -c 'cd /mnt && mmconvert -sf caffe -iw $(CAFFEMODEL) -in $(PROTOTXT) -df pytorch -om $@'

$(CAFFEMODEL):
	curl http://www.robots.ox.ac.uk/~vgg/software/very_deep/caffe/VGG_ILSVRC_19_layers.caffemodel -o $@

$(PROTOTXT):
	curl https://gist.githubusercontent.com/ksimonyan/3785162f95cd2d5fee77/raw/f02f8769e64494bcd3d7e97d5d747ac275825721/VGG_ILSVRC_19_layers_deploy.prototxt -o $@

clean:
	rm -rf $(TARGET) $(INTERMEDIATE) VGG_ILSVRC_19.py $(CAFFEMODEL) $(PROTOTXT)
