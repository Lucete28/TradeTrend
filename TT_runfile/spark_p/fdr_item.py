from pyspark.sql import SparkSession
from pyspark.sql.functions import min, max, col
from pyspark.sql.window import Window
import FinanceDataReader as fdr
import pandas as pd
from airflow.models import Variable

# SparkSession 생성
spark = SparkSession.builder.getOrCreate()

# Target_list 변수 가져오기
Target_list = Variable.get("Target_list")

# Target_list 파싱 및 정리
values = [tuple(item.strip("()").split(",")) for item in Target_list.split("),")]
values = [(x[0].strip(), x[1].strip()) for x in values]

df1 = spark.createDataFrame(fdr.DataReader('USD/KRW', '2020').reset_index())
df2 = spark.createDataFrame(fdr.DataReader('ks11', '2020').reset_index())

# 공통 데이터 (USD/KRW, ks11) 머지 및 클린
df1.createOrReplaceTempView("df1_view")
df2.createOrReplaceTempView("df2_view")
common_df = spark.sql("""
    SELECT
        df1_view.Date AS df1_Date,
        df1_view.Open AS Open_df1,
        df1_view.High AS High_df1,
        df1_view.Low AS Low_df1,
        df1_view.Close AS Close_df1,
        df1_view.Volume AS Volume_df1,
        df1_view.`Adj Close` AS Adj_Close_df1,
        df2_view.Date AS df2_Date,
        df2_view.Open AS Open_df2,
        df2_view.High AS High_df2,
        df2_view.Low AS Low_df2,
        df2_view.Close AS Close_df2,
        df2_view.Volume AS Volume_df2,
        df2_view.`Adj Close` AS Adj_Close_df2
    FROM
        df1_view
    JOIN
        df2_view ON df1_view.Date = df2_view.Date
    WHERE
        df2_view.Date IS NOT NULL
""").na.drop()

# 공통 데이터 스케일링 (min-max scaling)
min_max_window = Window.partitionBy().orderBy("df1_Date")
scaled_common_df = common_df.withColumn("min_val", min(common_df['Open_df1']).over(min_max_window)) \
                            .withColumn("max_val", max(common_df['Open_df1']).over(min_max_window)) \
                            .withColumn("scaled_Open_df1", (col('Open_df1') - col('min_val')) / (col('max_val') - col('min_val'))) \
                            .drop("min_val", "max_val")

# 종목 데이터 처리
for val in values:
    # 뉴스 데이터 가져오기
    news_df = pd.read_csv(f'/home/jhy/code/TradeTrend/data/{val[0]}_news_raw2.csv', index_col=0)
    news_df.index = pd.to_datetime(news_df.index)
    news_df_spark = spark.createDataFrame(news_df.reset_index())
    news_df_spark = news_df_spark.withColumnRenamed('Date', 'News_Date')
    news_df_spark.createOrReplaceTempView("news_df_view")

    # 종목 데이터 가져오기
    target_df = spark.createDataFrame(fdr.DataReader(val[0], '2020').reset_index())
    target_df = target_df.withColumnRenamed('Date', 'Target_Date')
    target_df.createOrReplaceTempView("target_df_view")

    # 종목 데이터와 뉴스 데이터 머지 및 클린
    final_df = spark.sql(f"""
        SELECT target_df_view.Target_Date, target_df_view.Close AS Close_{val[0]}, *
        FROM target_df_view
        JOIN news_df_view ON target_df_view.Target_Date = news_df_view.News_Date
        WHERE news_df_view.News_Date IS NOT NULL
        AND target_df_view.Target_Date IS NOT NULL
    """).na.drop()

    # Rename 'Date' column from scaled_common_df to 'Common_Date' for consistency
    final_df = final_df.withColumnRenamed('df1_Date', 'Common_Date')
    final_df = final_df.drop('Target_Date')

    # 최종 DataFrame을 CSV로 저장
    final_df.select(final_df.columns).coalesce(1).write.mode('overwrite').option("header", "true").csv(f'file:///home/jhy/code/TradeTrend/data/spark_data/{val[0]}_temp')
    # final_df.select(scaled_raw_df.columns).coalesce(1).write.option("header", "true").csv(f'file:///home/jhy/tmp/test_save_csv1/')
    # final_df.coalesce(1).write.mode('overwrite').csv(f'file:///home/jhy/tmp/test_save_csv2/')
    

    # Raw 데이터 스케일링 (min-max scaling)
    min_max_window = Window.partitionBy().orderBy("Target_Date")
    scaled_raw_df = final_df.withColumn("min_val", min(final_df[f"Close_{val[0]}"]).over(min_max_window)) \
                            .withColumn("max_val", max(final_df[f"Close_{val[0]}"]).over(min_max_window)) \
                            .withColumn(f"scaled_Close_{val[0]}", (col(f"Close_{val[0]}") - col('min_val')) / (col('max_val') - col('min_val'))) \
                            .drop("min_val", "max_val")
    scaled_raw_df = scaled_raw_df.drop('Target_Date')

    # Raw 데이터를 CSV로 저장
    scaled_raw_df.select(scaled_raw_df.columns).coalesce(1).write.mode('overwrite').option("header", "true").csv(f'file:///home/jhy/code/TradeTrend/data/spark_data/{val[0]}_raw')
    # scaled_raw_df.select(scaled_raw_df.columns).coalesce(1).write.option("header", "true").csv(f'file:///home/jhy/tmp/test_save_csv2/')

spark.stop()
