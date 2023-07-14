#!/bin/bash

PYSPARK_CODE=$1
JOB_NAME=$2
EXEC_DT=$3


python $PYSPARK_CODE


/home/jhy/spark/spark-3.2.4-bin-hadoop3.2/bin/spark-submit --master spark://BOOK-OCOA4D0UH1.:7077  \
--name "${JOB_NAME}_${EXEC_DT}" \
--executor-memory 512m \
--total-executor-cores 2 \
 $PYSPARK_CODE $EXEC_DT $SAMPLE_FRACTION

# CHECK
 ret_code=$?
if [ $ret_code -ne 0 ]; then 
    echo "SPARK JOB ERROR"
    exit $ret_code
fi
