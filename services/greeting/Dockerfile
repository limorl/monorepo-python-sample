FROM public.ecr.aws/lambda/python:3.12

# Copy lambda folder and local packages
COPY ./services/greeting/greeting ${LAMBDA_TASK_ROOT}/greeting
COPY ./services/greeting/config ${LAMBDA_TASK_ROOT}/config
RUN mkdir ${LAMBDA_TASK_ROOT}/local_packages
COPY ./packages/. ${LAMBDA_TASK_ROOT}/local_packages
COPY ./services/greeting/requirements.txt ${LAMBDA_TASK_ROOT}

WORKDIR ${LAMBDA_TASK_ROOT}

# Replace local package paths to container paths
RUN sed -i "s|file://.*/packages|file://$LAMBDA_TASK_ROOT/local_packages|g" requirements.txt

# Install required packages
RUN pip install -r requirements.txt

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "greeting.lambda_handler.handler" ]
