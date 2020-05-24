FROM mmdnn/mmdnn:0.2.5-py35-ubuntu16.04
RUN pip3 install -U pip \
 && pip3 uninstall -y torch torchvision \
 && pip3 install torch==1.5.0+cu101 torchvision==0.6.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html
CMD ["/bin/bash"]
