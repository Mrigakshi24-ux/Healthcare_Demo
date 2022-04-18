
FROM ubuntu
# Add labels to docker such as maintainer, version etc.
# LABEL maintainer="vk001716@gmail.com"
# LABEL version="0.1"


# ENV instruction adds env variable
# ENV TEST="hello"

# RUN echo $TEST

# MUST RUN THIS TWO LINE 
# set timezone according to your region
ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Run instruction runs a command
RUN apt update
RUN apt install python3 python3-pip build-essential cmake make -y

# Install dlib package

# Install flask package





# RUN pip3 install dlib flask
RUN pip3 install torch==1.8.2+cpu torchvision==0.9.2+cpu torchaudio==0.8.2 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html
RUN apt-get install libsndfile1 -y
ADD ./ /docker-app
RUN pip3 install -r /docker-app/requirements.txt
#RUN cat /docker-app/requirements.txt | xargs -n 1 pip3 install
# RUN pip3 install torch==1.8.2+cu111 torchvision==0.9.2+cu111 torchaudio==0.8.2 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html
# Lets copy contents of current folder to /docker-app folder in image



# What is the difference between CMD and ENTRYPOINT? You cannot override the ENTRYPOINT instruction by adding command-line parameters to the docker run command. By opting for this instruction, you imply that the container is specifically built for such use.

# Lets expose the image port to connect to flask applicaiton

EXPOSE 5000

# Entry point for docker image file
WORKDIR /docker-app
ENTRYPOINT  /usr/bin/python3 /docker-app/newHC_API.py