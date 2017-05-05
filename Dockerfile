FROM continuumio/anaconda3
ADD requirements.txt /root/workspace/
WORKDIR /root/workspace
RUN /opt/conda/bin/conda install jupyter -y --quiet \ 
  && pip install -q -r requirements.txt
CMD ["jupyter", "notebook", "--notebook-dir=/root/workspace/notebooks", "--ip='*'", "--port=8888", "--no-browser"]