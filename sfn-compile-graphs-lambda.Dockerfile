FROM amazon/aws-lambda-python:3.8

COPY . /tmp/src
COPY bin/sfn_compile_graphs.py "${LAMBDA_TASK_ROOT}"

RUN rm -rf "${LAMBDA_RUNTIME_DIR}"/boto3* "${LAMBDA_RUNTIME_DIR}"/botocore*
RUN pip install -r /tmp/src/requirements.txt
RUN cd /tmp/src && python setup.py install && rm -rf /tmp/src

STOPSIGNAL SIGTERM

CMD ["sfn_compile_graphs.lambda_handler"]