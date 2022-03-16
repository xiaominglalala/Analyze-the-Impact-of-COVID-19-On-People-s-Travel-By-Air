---
title: Project_4
tags: []
categories: ""
mathjax: false
date: 2021-11-21 13:12:00
---

# 1 Introduction

Travel has been severely restricted since the COVID-19 outbreak began in late 2019, but is this the result of government restrictions, or people simply choosing not to go out because of scary of unknown COVID-19. So we wanted to use the data from Twitter, the number of COVID-19 diagnoses and new cases per day, as well as flights over the last three years, to find out how does the COVID-19 affects people's travel and their mood. Based on this original intention, the project completed the following tasks:

-   Data Collecting
-   Data Pre-Processing
-   Data Analysis
-   Data Conclusion
-   Future Work

# 2 Data Collecting

> 这部分基本可以直接用 project 1 的内容。
>
> 预计在网页上占一个 tab，首先是 overview 介绍这三个数据集的：
>
> -   采集来源：给个 reference 的 url
> -   采集方式：爬取/api/下载
> -   数据格式：每一列的含义、解释
> -   数据目的：这个数据集有什么用(简单做个铺垫啥的)
>
> project1 做过数据集的 cleanliness/data issue，把这部分也加上
>
> 最后每个数据集用 plotly 等工具展示一个数据样本

## 2.1 Covid-19 Cases and Death Dataset

### 2.1.1 Overview

We use CDC api to collect [Covid-19 Cases and Death](https://data.cdc.gov/Case-Surveillance/United-States-COVID-19-Cases-and-Deaths-by-State-o/9mfq-cb36) dataset. We need a APP TOKEN to request their api.

Requested data are in the form of json array. I transform them into CSV data with some adjustments (to make data more easy to look at). Their api has a paging limitation so I can't just get my data in a simple request. I made a loop to request 5000 records per request, and save them into CSV files.

### 2.1.2 Data Sample and Definition

| Column Name     | Description                                                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------------------- |
| submission_date | Date of counts                                                                                                |
| state           | Jurisdiction                                                                                                  |
| tot_cases       | Total number of cases                                                                                         |
| conf_cases      | Total confirmed cases                                                                                         |
| prob_cases      | Total probable cases                                                                                          |
| new_case        | Number of new cases                                                                                           |
| pnew_case       | Number of new probable cases                                                                                  |
| tot_death       | Total number of deaths                                                                                        |
| conf_death      | Total number of confirmed deaths                                                                              |
| prob_death      | Total number of probable deaths                                                                               |
| new_death       | Number of new deaths                                                                                          |
| pnew_death      | Number of new probable deaths                                                                                 |
| created_at      | Date and time record was created                                                                              |
| consent_cases   | If Agree, then confirmed and probable cases are included. If Not Agree, then only total cases are included.   |
| consent_deaths  | If Agree, then confirmed and probable deaths are included. If Not Agree, then only total deaths are included. |

Please click [here](sample_cdc.html) to view some data sample of this dataset.

### 2.1.3 Data Issues

-   Different data types such as float and string may appear in the same column.
-   There are a lot of missing values.
    -   For example, we have the value of "tot_case" for a certain city on a certain day, and this value represents the total number of cases. This value should be equal to the sum of the value of "conf_cases" and the value of "prob_cases". But the last two values in the data set are often blank, even if they should not be 0.
        Some data may have a noise value. For example, the value of the number of new infections is -1.

### 2.1.4 Data Cleanliness

For the CDC data set, we mainly made the following assessments：

-   Calculate the fraction of missing values for each attribute.
-   Calculate the fraction of noise values.

The percentage of missing values for each attribute:

![Missing Value](https://user-images.githubusercontent.com/35549544/143917182-01b4fa0e-b19f-4cbc-8846-009da273236f.PNG)

The fraction of noise values:

![Noise Value](https://user-images.githubusercontent.com/35549544/143917244-3216d4da-e829-47ad-92b2-b94c91c5252e.PNG)

## 2.2 Opensky Airline dataset

### 2.2.1 Overview

We use python crawler to scrape data from [OpenSky](https://opensky-network.org/) for this dataset. Find a website that contain the data we need, pass the url to the method, then the method will iterate all the href in the html text, add it into the waiting list only if it is the csv file that we need by using 'endswith()'. Then use 'requests' to scrape filee, and add a downloading percentage bar by using tqdm. Since all scv files are compressed as gz file, we also need to import gzip to decompress the file one by one by script.

In total, the whole dataset contains **15 different columns** and **71645420 records**.

Since it is too large to upload (13.3 GB), we choose to provide a download link for the whole data set.

### 2.2.2 Data Sample and Definition

| Column Name  | Description                                                                                                                                                      |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| callsign     | the identifier of the flight displayed on ATC screens (usually the first three letters are reserved for an airline: AFR for Air France, DLH for Lufthansa, etc.) |
| number       | the commercial number of the flight, when available (the matching with the callsign comes from public open API)                                                  |
| icao24       | the transponder unique identification number;                                                                                                                    |
| registration | the aircraft tail number (when available);                                                                                                                       |
| typecode     | the aircraft model type (when available);                                                                                                                        |
| origin       | a four letter code for the origin airport of the flight (when available);                                                                                        |
| destination  | a four letter code for the destination airport of the flight (when available);                                                                                   |
| firstseen    | the UTC timestamp of the first message received by the OpenSky Network;                                                                                          |
| lastseen     | the UTC timestamp of the last message received by the OpenSky Network;                                                                                           |
| day          | the UTC day of the last message received by the OpenSky Network.                                                                                                 |

Please click [here](sample_opensky.html) to view some data sample of this dataset.

### 2.2.3 Data Issues

-   There is no noise value in this dataset, only missing value
-   Missing value for Fields **origin** and **destination**
    Origin and destination airports are computed online based on the ADS-B trajectories on approach/takeoff: no crosschecking with external sources of data has been conducted. These two fields are empty when no airport could be found
-   Missing value for Fields **typecode** and **registration**
    Aircraft information come from the OpenSky aircraft database. Fields are empty when the aircraft is not present in the database.
-   Missing value for Fields **number**
    The commercial number of the flight, are empty when unavailable

### 2.2.4 Data Cleanliness

-   The evaluation of the cleaniness is (valid records that we need/ all records that we need), as long as there is a missing value in the record, this record is invalid.
-   Cleaniness of Sample(First 4000 records of each file) => 91.8156%
-   Cleaniness of whole Dataset(the whole dataset is too big to upload - 13.3GB) => 98.1030%

## 2.3 Scraped Tweets related to 'Covid' and 'flight'

### 2.3.1 Overview

This is a dataset of tweets that is scraped from twitter. We scraped for more than 20 hours to get over 450K tweets in English that contains keywords `covid` and `flight` since `01-01-2019` (It's an early date but we just want to make sure the data is fully covered. Interesting fact is that the earliest tweet that contains those two words is on `02-19-2019`, unrelated to covid-19 though).

There are a lot of columns such as datetime, user_id, username, name, tweet, language, mentions, urls, photos, replies_count, retweets_count, likes_count, hashtags, cashtags, link, retweet, quote_url, video, thumbnail, near, geo, etc.

### 2.3.2 Data Sample and Definition

| Column Name     | Description                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------ |
| id              | id of this original tweet                                                                                    |
| conversation_id | id of the conversation that includes this tweet(if applied). Otherwise appears the id of this original tweet |
| created_at      | the date and time when this tweet is created (with time zone)                                                |
| date            | the date when this tweet is created                                                                          |
| time            | the time when this tweet is created                                                                          |
| timezone        | the timezone of date and time above                                                                          |
| user_id         | id of the user who creates this tweet                                                                        |
| username        | username of the user who creates this tweet                                                                  |
| name            | the nickname of user who creates this tweet                                                                  |
| tweet           | the plain text of tweet                                                                                      |
| language        | the language this tweet uses                                                                                 |
| mentions        | twitter users that are mentioned in this tweet                                                               |
| urls            | the urls that appears in this tweet                                                                          |
| photos          | the photos that appears in this tweet                                                                        |
| replies_count   | the number of replies to this tweet                                                                          |
| retweets_count  | the number of retweets of this tweet                                                                         |
| likes_count     | the number of likes of this tweet                                                                            |
| hashtags        | the hashtags that appears in this tweet                                                                      |
| link            | the original link to this tweet                                                                              |
| video           | the number of videos that appear in this tweet                                                               |
| thumbnail       | the thumbnail of user that creates this tweet                                                                |
| reply_to        | the people and their id that this tweet replies to(if applied)                                               |

Please click [here](sample_twitter.html) to view some data sample of this dataset.

### 2.3.3 Data Issues

-   Missing values in many fields.

    -   For example, 'username', 'mentions', 'retweets'. However, we mainly focus on the tweet column because that is where text data exists.

-   Noise value in 'tweet' colunmn. For example, there are lots of emojis and punctuation which are useless for following analysis.

### 2.3.4 Data Cleanliness

cleaningText.py: # cleaning text

-   using regular expression to filter all the emojis and punctuation
-   using stopwords to filter all the useless words

```
the percentage of valid content: 19.478%
the percentage of useful words: 78.476%
```

# 3 Pre-Processing of Data

We extract **_8_** columns from COVID-19 dataset and **_3_** columns from flight dataset.

## 3.1 Covid-19 Cases and Death Dataset

-   Handling null values
    -   For null values, we decided to fill them with mean values. Because we need to make sure there is a relation about the columns, such as tot_cases = conf_cases + prob_cases.

```python
# handle null value of each column
data[col].fillna(mean, inplace = True)
```

-   Checking the duplicates

```python
# check duplicate
print(df[df.duplicated()])
```

## 3.2 Opensky Airline dataset

-   Since we only need the origin, destination, icao24 and date of flights for the current project, delete any records that contain nan values or empty values in above four columns.
-   Also, for this project, we only need flights that take place in the United States, so we use python crawler to get the aiports and their corresponding states from wiki, so we can identify and delete records that containing airports that are not in the United States.

## 3.3 Scraped Tweets related to 'Covid' and 'flight'

In this part, we need to decide what content of a tweet is not clean. This decision should also made under the consideration of what we need to do with those tweets. After our discussion, we decided to do Sentiment analysis with all these tweets (will be further described in that section).

After reading quite a few scraped tweets, we found out that these 4 kinds of noise should be cleaned.

-   Stopwords
-   URLs (https://xxx.dd.com/dasdfa)
-   Hashtags (#sometag)
-   Mentioned tags (@somebody)

The reason for removing stopwords is quite clear, there's no need analyze the sentiment of stopwords(which usually don't have emotional meaning afterall). This reason also applies for URLs and Mentioned tag. Whether to remove hashtags is discussed more. We decided to remove it simply because, yes it do have meaning sometimes, but most of the time they only represent some certain objective things(it's a noun mostly) which don't tend to have emotional meaning.

We used `nltk` package to tokenize tweets. We also used it as our stopwords list. In terms of urls and hash tags and mentioned tags, we came up with two regular expressions to find and replace them.

Every tweet is read from csv file named `result_covid_flight.csv` and then rewrite into a new csv file named `result_covid_flight_cleaning.csv`. As we collected 470K records and there's no way to upload it on github, we created a share link on google drive for you to use.

```
https://drive.google.com/file/d/1OA1kkjQ9V0ZXQ-s8MqbLsOXATgK4k-IW/view
```

# 4 Analysis

## 4.1 Basic Statistical Analysis

### 4.1.1 Mean, Mode, Median

#### 4.1.1.1 Opensky Airline dataset

The three columns data we got here are origin airports, destination airports and the date of flight. Where the mean and standard divation of those three variables is meaningless, so we choose to calculate the median and mode (Actually the median is also meaningless).
Average flights per day => 10491
Here is the hitogram for flights per day:

[**plotly 链接**](https://github.com/singh-classes/project-4-segmentfault/blob/lyt/figures/opensky_histogram.html)

#### 4.1.1.2 CDC dataset

Here are mean, median, std values of variables in COVID-19 dataset.

[\*\*plotly link](www.google.com)

### 4.1.2 Anomalies Detection

#### 4.1.2.1 Opensky Airline dataset

As for the anomalies detection. Since this data could be considered as kind of time series, we choose to calculate the anomalies point by using S-H-ESD method. We constructed a variable named flights, which is used for represent the number of flights that launched that day, which is also used for anomalies detection. For those points, we choose to keep them since they are part of our data, which is the real data, could got some unexpected situation, and that's what we are going to dig.

[**plotly 链接**](https://github.com/singh-classes/project-4-segmentfault/blob/lyt/figures/opensky_ourliers.html)

#### 4.1.2.2 CDC dataset

Using **_lof_** to detect anomlies on CDC dataset

the inliers in the output are the new variables that do not contain the outliers.
First compute the local density deviation of a given data point with respect to its neighbors. It considers as outliers the samples that have a substantially lower density than their neighbors.
Use method as a threshold value for distinguishing outliers and common points.

Here are three different values of K to detect anomlies

K = 5:

![](figures/lofk=5.png)

K = 10:

![](figures/lofk=10.png)

K = 15

![](figures/lofk=15.png)

##### 4.1.2.2.1 How S-H-ESD Work

![](figures/S-H-ESD.png)

## 4.2 Bin the data

### 4.2.1 Covid-19 Cases and Death Dataset

Here is the overvew of the **binned** data.

We chose to bin the data that combined by two columns - 'origin' and 'destination'. Which is actually the number of flights per day after the processing. As for the binning strategy we used in this part, is Equal-width binning, which is pretty good for those kind of data. Since the number of flights would be pretty stable if there is no influence.

[**plotly 链接**](https://github.com/singh-classes/project-4-segmentfault/blob/lyt/figures/opensky_bin.html)

From this chart we can know that average flights per day is within 6906 to 10358, and the overall trend is toward higher frequencies. In fact, from here we can come up with a more superficial hypothesis that people's travel and their attitudes towards the new cap and the spread of the disease have no direct relationship

### 4.2.2 Covid-19 Cases and Death Dataset

-   The tot_cases is the key data in the CDC data, reflecting the number of patients in a certain state on a certain day. Through the binning operation, we can get the distribution of the number of patients, we can **eliminate some abnormal data**, **realize the discretization of the data**, **improve the robustness of the data**, and will not collapse due to the input of some extreme size data. In addition, if we further subdivide into each state, we can get the peak date of the epidemic in each state.
-   For the tot_cases, we divide it into intervals with **same width** .
-   We can find that the first bin concludes half of the cases.

[binning.html](https://github.com/singh-classes/project-4-segmentfault/blob/ym/binning.html)

## 4.3 Histograms and Correlations

### 4.3.1 Histograms

-   For CDC dataset, we made histograms of tot_cases, conf_cases and prob_cases.
-   The abscissa represents the interval of the data box, and the ordinate represents the number of people.
-   We can see that the histogram shapes of tot_cases and conf_cases are very similar. And the frequency range also crystallizes. Since tot_cases is obtained by adding conf_cases and prob_cases, we can conclude that the size of tot_cases is mainly determined by the size of conf_cases.

#### 1. historgram for tot_cases

![](https://user-images.githubusercontent.com/35549544/138144242-7733ef2d-60c1-4770-9425-7f0306fa780d.png)

#### 2. historgram for conf_cases

![image](https://user-images.githubusercontent.com/35549544/138144262-943465aa-cde7-4158-86c9-876b4159d84b.png)

#### 3. historgram for prob_cases

![image](https://user-images.githubusercontent.com/35549544/138144276-1c0628ee-67e0-4963-b909-4ef6607c9b45.png)

### 4.3.2 Correlations

#### 4.3.2.1 correlation between tot_cases and tot_death

-   In this picture, We can see that the scattered points formed by tot_cases and tot_death present **multiple curves shapes**. And by observing these shapes, we can conclude that the overall relationship between these two data is **proportional**.
-   In addition, if we observe the scatter plot in the figure, we can find that the scatter points are not completely concentrated together to form a sphere, but form multiple curves, starting from (0, 0). Such a result may reflect the relationship between the total number of diagnoses and the total number of deaths in different **states**, or it may be the influence of the **season**, which makes the image present such characteristics.

[图片 1](https://github.com/singh-classes/project-4-segmentfault/blob/ym/corrleation%20totcases%26totdeath.html)

#### 4.3.2.2 correlation between tot_cases and prob_death

-   In this picture we can see that the scattered points also form many curves that are close to straight lines, instead of clustering into a cluster. The analysis of this situation is the same as the analysis in the first picture.
-   What is worth noting is the scattered point set of **two approximate horizontal lines** in the figure. The following one reflects the situation that prob_death is 0 but tot_cases is not 0 happens many times. The above item reflects that when prob_death occurs with a high frequency between 0 and 1000, this situation is caused by filling the blank part of prob_death with the average value.
-   The resaon for this method is： If we do not fill in, we will lose nearly **half of the data** , because it is time series data, if the data loses a long period of time, it will be difficult to compare the data characteristics of different time periods. For example, the influence of the season on the epidemic situation in a certain state.

[图片 2](https://github.com/singh-classes/project-4-segmentfault/blob/ym/corrleation%20prob%20death%20%26%20tot%20cases.html)

#### 4.3.2.3 correlation between tot_death and prob death

-   In this picture, we can find that the relationship diagram between pro_death and tot_death is very close to the relationship diagram between pro_death and tot_cases. Since tot_death and tot_cases are close to a linear relationship, such a result can also be inferred.

[图片 3](https://github.com/singh-classes/project-4-segmentfault/blob/ym/corrleation%20prob%20death%20%26%20tot%20death.html)

## 4.4 Cluster Analysis

-   For each dataset, we only display one figures, for more, please refer to [Project2](https://github.com/singh-classes/project-2-segmentfault/tree/main/pics/)

### 4.4.1 opensky

We have conducted all four cluster analyses on the opensky dataset. However, since all numeric dataset we got are time series, it can't do cluster by above 4 method. So we do combine several columns into two new columns named 'flights per day' and 'flights happened in Mode airports per day'. But nothing changed, even though we have made out four of them, they seems like meaningless. The only only thing we can tell form the figures is that the 'flights per day' and 'flights happened in Mode airports per day' do key the same correlation at the most the time.

-   ![](figures/opensky_cluster_kmean.png)

### 4.4.2 CDC

We have conducted all four cluster analyses on the opensky dataset. However, since all numeric dataset we got are time series, it can't do cluster by above 4 method. So we do combine several columns into two new columns named 'new death per day' and 'new cases per day'. But nothing changed, even though we have made out four of them, they seems like meaningless. The only only thing we can tell form the figures is that the 'new deatch per day' and 'new cases per day' do key the same correlation at the most the time.

-   ![](figures/CDC_cluster_kmean.png)

## 4.5 Sentiment Analysis

Sentiment Analysis via Scraped Tweets.

We chose Sentiment Analysis because of two reasons.

1. Tweets are too short to use topic modeling. In Professor Lisa's lecture, we saw how bad it cloud become, there won't be any good result of topics to show. More importantly, we don't want the topic of it! These data are collected because they are related to `covid-19` and `flight`. That's already our topics!
2. We do want to analyze how people feel about `covid-19` when `travel through air`. Perhaps sentiment analysis won't tell exactly how but that's the way on it.

To be more specific, why we want to find sentiment of tweets? First, we want to know how people feel when they are traveling by plane under the pandemic of Covid-19, that is, does people feel positive more or negative more under such circumstances. Second, we want to know the sentiment through out the timelines. When does people feel negative more?

### 4.5.1 Sentiment Grading

We use `vaderSentiment` package to do grading. This is a great package based on lexicon method. It does not only contains emotional vocabulary, but also has a lot `emoji` and `emoticon`. We use it to calculate the sentiment for each tweet.

The result for this part is also too large to upload. It extract the content in `result_covid_flight_cleaning.csv` (which is also generated in `Tweets cleaning` section) and generate results in a new csv file named `result_covid_flight_cleaning_sentiment.csv`.

For more details please check it in our code file `TweetsSentiment.py`

### 4.5.2 Sentiment Labeling and Accuracy

For this part we manually add tags by determining the sentiment for a tweets. It included 2 parts here.

First we need to sample a few tweets. Here we extracted 50 tweets randomly from `result_covid_flight_cleaning.csv`. And we manually labeled each of these 50 tweets. Sometimes it's really hard to determine it is positive, negative or neutral even for human beings like us. We wrote a small script named `TweetsTagging.py` for this task and it will generate a tagged file named `result_covid_flight_cleaning_tag.csv` (and it is uploaded on github). **Please don't run it** unless you want to overwrite our tagging result and re-tag it again.

Second we want to compare it to the sentiment grading done by `vaderSentiment`. In the code `TweetsSentimentAccuracy.py`, we calculated the sentiment of each tweet and compared it with our manually labels. It will generate the result in a file named `TweetsSentimentAccuracyResult.txt`.

```
Positive tweets accuracy: 4/4
Negative tweets accuracy: 10/27
Neutral tweets accuracy: 8/19
Total tweets accuracy: 22/50 = 0.44
```

### 4.5.3 Sentiment Analysis

For this part we want to analyze some result by grading sentiment for each tweets. We summarized the total amount of tweets in each month by their sentiment. The result (`TweetsSentimentAnalysisResult.txt`) is generated by code file named `TweetsSentimentAnalysis.py`and it looks like this:

```
month       pos   neg   neu
2021-08    [7759, 8106, 3996]
2021-07    [6802, 6988, 2922]
2021-06    [6785, 6070, 3391]
2021-05    [7937, 8557, 3939]
2021-04    [9452, 11601, 5548]
2021-03    [6045, 6331, 2726]
2021-02    [6452, 6457, 3136]
2021-01    [10841, 12724, 5194]
2020-12    [12646, 19225, 6153]
2020-11    [9028, 7321, 4133]
2020-10    [9842, 10077, 3912]
2020-09    [8888, 8893, 4255]
2020-08    [10677, 9769, 5160]
2020-07    [12560, 11426, 5593]
2020-06    [11901, 10048, 4416]
2020-05    [18170, 10801, 6237]
2020-04    [18425, 12129, 5403]
2020-03    [16272, 17767, 7922]
2020-02    [1040, 1138, 537]
2020-01    [1, 0, 0]
2019-06    [0, 0, 1]
```

```
month       pos     neg     neu
2021-08    [39.07%, 40.81%, 20.12%]
2021-07    [40.70%, 41.81%, 17.48%]
2021-06    [41.76%, 37.36%, 20.87%]
2021-05    [38.84%, 41.88%, 19.28%]
2021-04    [35.53%, 43.61%, 20.86%]
2021-03    [40.03%, 41.92%, 18.05%]
2021-02    [40.21%, 40.24%, 19.55%]
2021-01    [37.70%, 44.24%, 18.06%]
2020-12    [33.26%, 50.56%, 16.18%]
2020-11    [44.08%, 35.74%, 20.18%]
2020-10    [41.30%, 42.29%, 16.42%]
2020-09    [40.33%, 40.36%, 19.31%]
2020-08    [41.70%, 38.15%, 20.15%]
2020-07    [42.46%, 38.63%, 18.91%]
2020-06    [45.14%, 38.11%, 16.75%]
2020-05    [51.61%, 30.68%, 17.71%]
2020-04    [51.24%, 33.73%, 15.03%]
2020-03    [38.78%, 42.34%, 18.88%]
2020-02    [38.31%, 41.92%, 19.78%]
2020-01    [100.00%, 0.00%, 0.00%]
2019-06    [0.00%, 0.00%, 100.00%]
```

Judging by the result we may conclude that:

-   Positive tweets are apparently more than negative tweets in the beginning months that COVID-19 pandemic just started. People using English on twitter are significantly confident overall. We guess that most of them at that time believes that it will all be gone soon.
-   As time went by, tweets from people tends to be balanced between positive sentiment and negative sentiments. There are some months that negative sentiments are significantly more than positive sentiments.
-   People talked it more when COVID-19 just began. The tendency of which tends to be lower as time goes by.

## 4.6 Hypothesis

> 我也没想清楚这个到底是放在 analysis 里还是单独拿出来讲，我感觉好像都可以，单独拿出来那就是一个独立的 tab 了，直接照搬 project3 的内容

### 4.6.1 Hypothesis1 (Decision Tree)

_Although the number of flights per day is generally on the rise. But people's willingness to travel is still affected by the number of new cases and deaths each day._

We used decision tree to test since we want to prove that there is a relationship between the daily new cases and deaths and people's willingness to take plane. The hypothesis assumes that the daily new cases and new deaths would influence people's willingness, but we don't know how it works, so we choose to use decision tree classifier here.
(With both opensky and CDC data set).

We preprocess the data by reducing the outliers, fill the missing value with the mean or median. And since both data set is time series, we have to make sure the data we used for this hypothesis test should in the same time range. So we choose the data based on the CDC data set. When there are both records for today and tomorrow in opensky data sets, choose this CDC records and store the group id.

As for how we divided those data into groups

-   When the flights number is decrease by tomorrow, mark it as '-1',
-   When flights number is increase by tomorrow, mark it as '1' (If remain the same, mark it as '0', which is impossible in our data set, so there are two groups in total.)

Here is the reports generated by the provided methods:

![](figures/opensky_CDC_decisionTree.png)

As we can see here, the sorce generated by those method tells us there do have a relation between people's mind about taking flights and daily new cases and deaths. However, those outputs also donate that the relation is so weak that only a small part of people would consider about the daily new cases and deaths when they are going to take plane.

So, our data do support this hypothesis, but the relationship between them is not completely assured.

### 4.6.2 Hypothesis 2 (T-Test)

As for t-test, we need to set a null hypothesis and set the significance standard alpha which will measure if the result meets the hypothesis or not.

Then we need to calculate the statistical values t(which measures if the average of a sample is quite different from the average of all) and we can get p_value by looking up in the table to compare p_value and the significance standard alpha

**_The average conf_cases in all states are 30,000._**

This hypothesis mainly focus on the difference of the number of confirmed COVID-19 cases between states in America, because people have to know if different states have different panic situation to make sure if it is safe to take flights.

here is the result (p_value < significance alpha)
![](figures/ttest.png)

### 4.6.3 Hypothesis 3 (Anova test)

As for anova test, we need to set a null hypothesis and set the significance standard alpha which will measure if the result meets the hypothesis or not.

Then we need to calculate the statistical values ssb(difference between groups) and ssw(difference within group) and we can get f_value by calling statistic function to compare f_value and the significance standard alpha

**_There is no significant difference between covid-19 cases(including conf_cases, prob_cases)._**

This hypothesis mainly focus on the difference between confirmed COVID-19 cases and probable COVID-19 cases in America.

here is the result (f_value < significance alpha)
![](figures/anova.png)

## 4.7 Classification

**There are some more information that wasn't shown directly on data. For example, death rate in CDC Covid-19 dataset. In this part we labeled death rate on CDC dataset and tried all 6 classifiers to classify data by death rate, in order to figure out how well they each did on this classification task.**

We evaluate their performances by `accuracy_score`, `classification report`(include `precision`, `f1-score`, `macro avg`, `weighted avg` for each class.)

We also plot `ROC curve` and `aur_score` for each classifier. As we know `sk-learn` only supports `ROC curve` for binary classifier. It's typical to draw a `ROC curve` by each class. So we will transform the result data into a binary one for each class, and then draw them on the plot by class. Check them down below.

### 4.7.1 How is data pre-processed and split

We first dealt with the missing and error in the data based on the analysis of Proj2. After that, we use tot_death and tot_cases in the processed data to divide and calculate the corresponding death_rate. This variable can be understood as the proportion of deaths in all cases.

Next, according to the value of death_rate, we perform labeling for later classification. Mark the top 25% part of death_rate in the data as type '2', which represents high mortality; mark the 25%~75% part of death_rate in the data as type '1', which represents medium mortality; mark death_rate in the data The last 25% of the part is marked as type '0', which represents low mortality.

The figure below shows the Data summary, including the 25% point and 75% of death rate:

![](figures/Data summary.png)

### 4.7.2 Logistical Regression

Here is the accuracy rate, confusion matrix and reports generated by Logistical Regression:

![](figures/LR result.png)

The ROC curve is:

![](figures/LR ROC.png)

### 4.7.3 Decision Tree

Here is the accuracy rate, confusion matrix and reports generated by Decision Tree:

![](figures/Decision Tree result.png)

The ROC curve is:

![](figures/DT ROC.png)

### 4.7.4 kNN

Here is the accuracy rate, confusion matrix and reports generated by kNN:

![](figures/KNN result.png)

The ROC curve is:

![](figures/kNN ROC.png)

### 4.7.5 Naive Bayes

Here is the accuracy rate, confusion matrix and reports generated by Naive Bayes:

![](figures/NB result.png)

The ROC curve is:

![](figures/NB ROC.png)

### 4.7.6 SVM

For the classification task done by SVM, well the result wasn't satisfied and it took more than the sum of all other 5 methods to finish. We used our training dataset to train this model and use validation dataset to test its performance. I tried all 3 SVM models, which are `svc`, `NuSVC` and `LinearSVC`. `SVC` did best so the result is performed by `svc` here.

We also used cross validation to train this model, still not so good.

![](figures/SVM result.png)

The ROC curve is:

![](figures/SVM ROC.png)

### 4.7.7 Random Forest

For the classification task done by random forest, it did really good. We used our training dataset to train this model and use validation dataset to test its performance.

![](figures/random forest result.png)

The `ROC curve` for random forest is also quite good-looking. It shows strong relation for each type.

![](figures/random forest ROC.png)

### 4.7.8 Overall comparison

Here is the comparison of all six algorithm:

![](figures/Algorithm Comparsion.png)

[可交互图表]https://github.com/singh-classes/project-4-segmentfault/blob/ym/alg%20accuray%20score.html

Note that our labels are formed by calculation of a few columns. So from all these 6 classification accuracy result we can learn that:

-   `Random Forest` and `Decision Tree` did best in our classification task
-   `Naive Bayes` did worst in our classification task
-   It implies that `Naive Bayes` might not detect much division relationship, while `Random Forest` and `Decision Tree` does.
-   `kNN` is in the upper middle.
-   `SVM` and `Logistical Regression` are not quite good as the best. But they did not too bad. However they cost most of the time.

# 4.8 Additional Cluster Analysis

## 4.8.1 opensky

We have conducted all four cluster analyses on the opensky dataset. However, since all numeric dataset we got are time series, it can't do cluster by above 4 method. So we do combine several columns into two new columns named 'flights per day' and 'flights happened in Mode airports per day'. But nothing changed, even though we have made out four of them, they seems like meaningless. The only only thing we can tell form the figures is that the 'flights per day' and 'flights happened in Mode airports per day' do key the same correlation at the most the time.
![](figures/opensky_cluster_dbscan.png)
![](figures/opensky_cluster_kmean.png)
![](figures/opensky_cluster_gmm.png)
![](figures/opensky_cluster_ward.png)

## 4.8.2 CDC

We have conducted all four cluster analyses on the opensky dataset. However, since all numeric dataset we got are time series, it can't do cluster by above 4 method. So we do combine several columns into two new columns named 'new death per day' and 'new cases per day'. But nothing changed, even though we have made out four of them, they seems like meaningless. The only only thing we can tell form the figures is that the 'new deatch per day' and 'new cases per day' do key the same correlation at the most the time.
![](figures/CDC_cluster_dbscan.png)
![](figures/CDC_cluster_kmean.png)
![](figures/CDC_cluster_gmm.png)
![](figures/CDC_cluster_ward.png)

# 5 Conclusion

There is no doubt that travels by air is affected by COVID-19.

## 5.1 People’s moods are affected by COVID-19

-   People are more positive in terms of travel by air at the beginning of this pandemic.
-   People become more negative as time went by.

Through sentiment analysis we know that sentiment of people are unstable. They tends to be more positive at first. They might be confident and thought COVID would all ends really soon. And then they become more negative cause it didn't end at all.

## 5.2 Only a part of travelers are finally stopped by COVID-19

-   Travelers are stopped most at the beginning of this pandemic.
-   Travelers made up their minds as time went by.

By combining flights dataset with CDC dataset we know that COVID-19 did stopped people traveling, but not significantly. They are mostly stopped at the beginning of this pandemic, and as time went by, people who decided to travel by air still travel.

# 6 Ethical considerations & Limitations & Future Work

A few ethical considerations and limitations in our project, and how can we do better in the future.

## 6.1 Bias

### 6.1.1 Only airlines data included

The first thing is bias. Apparently the fact that we only discussed about airlines made our bias.

We didn't take other forms of transportation into consideration mainly because they are hard to obtain.

But it's still a fact that our project can do better if we can compare airlines data with trains records or some other forms.

### 6.1.2 Only US regions are considered

Another bias in our project is that we only considered US regions.

If we can get flights data and covid-19 cases datasets all around the world, we can then do comparison to find out to what degree covid has affect each countries.

## 6.2 Tweets

### 6.2.1 Related to specific user

Another ethical consideration is about our dataset of tweets.

Even though it is scraped through publicly available, but it is related to specific twitter user. And this data will remains in our dataset even if that user deletes it.

### 6.2.2 Data remains

Tweet data will remains in our dataset even if that user deletes it.

## 6.3 Sentiment Analysis

### 6.3.1 Not accurate enough

As for sentiment analysis, we did come up with a few conclusions by that, but the sentiments within tweets are not accurate enough.

It is too unclear that we can't figure our their thought correctly, result in we cannot rely on those sentimental analysis. So what we are going to work on would be improving the accuracy of our sentimental analysis. Thus making our sentiment analysis more convincing.

## 6.4 Data Combinations

### 6.4.1 Text data should be somehow considered into analysis

Text data are solely analyzed. We didn't combine text data with other datasets when we are doing data analysis. We should definitely try to vectorize these text data and combine them with other forms of data and analyze them together.

### 6.4.2 Network graph isn’t combined with text data

We did draw the network graph for opensky dataset, which should generate many useful information about the correlations between pandemic and people's mind about it.

However, since we got few datasets to compare with, we didn't get any useful information, which shouldn't be. So the network analysis should also be a big part of our future work.

[可交互图表]https://github.com/singh-classes/project-4-segmentfault/blob/lyt/figures/opensky_network.html
