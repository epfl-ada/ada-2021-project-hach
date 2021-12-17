# EPFL ADA 2021 - HACH Project Website

## Is the Greta effect fake news?
### An analysis of the public debate on climate change.
### Link to the website: https://hugocasa.github.io/hach-project/

### 1. Abstract:

Climate change has been a topic dominating the public debate in the media for a while now. Since 2018, the Friday for Future movement has taken to the streets in an attempt to be heard by policy makers. In our project on the Quotebank dataset we will analyze how the public debate on climate change has evolved over the recent years, while focusing on Greta Thunberg’s impact on it. We will explore who is quoted on climate change, what they are saying and how they are saying it. We want to quantify the effect and influence Greta had on the debate, in hopes of better understanding the phenomenon she has become. We want to tell the story of ‘the Greta effect’ in a different way, showing just how big her impact was on the debate in the media.

### 2. Research Questions :

- Which speakers are quoted on climate change, what do they have in common and what are their differences?
  - In terms of age, gender, nationality and political affiliation
- How are different groups speaking about climate change? Are there any differneces between the US and Europe?
  - How long are the quotes?
  - Positive or negative sentiment?
  - What is the difference in language complexity?
- How has the approach to climate change evolved in recent years?
  - Has debate become more polarized?
  - Has the language complexity changed?
  - Is there any correlation between scientific vulgarization and the growing debate on climate change?
- How do Greta's quotes compare to Donald Trump?
- Did extreme weather events have any impact on how people talk about climate? Do we notice any changes in the sentiment score of the speakers?
- Is there any quantifiable difference in the debate using the aforementioned metrics before and after Greta Thunberg?

### 3. Additional Datasets:

We are using the WikiData and WikiLabels datasets, provided for the project, to gather attributes and information about the speakers.
In order to have a global view on our "climate change" topic, we also needed information about the natural disasters. The different events recorded in the dataset we are using are listed here : https://www.nws.noaa.gov/directives/sym/pd01016005curr.pdf.
The dataset was created and maintained since 1950 by the national centers for environmental information in the USA. You can download the dataset from this link : https://www.ncdc.noaa.gov/stormevents/ftp.jsp.

In order to extract quotes related to climate change, we are using a list of similar words inspired by the the COP21 Glossary of Terms Guiding the Long-term Emissions-Reduction Goal (https://www.wri.org/insights/cop21-glossary-terms-guiding-long-term-emissions-reduction-goal).

### 4. Methods:

Our group is collaborating on a jupyter hub hosted by Infomaniak and we will be using jupyter notebooks for the analysis of the data.
In order to extract data frames from the Quotebank dataset, we’re loading a specific number of rows into memory using read_json with a chunksize of 1’000’000, extracting the quotes about climate change and then saving them to pickle files for later use.
As Greta Thunberg appeared on the public stage in August 2018, but really took off in 2019, we will focus on 2017-18 as ‘pre-Greta’ and 2019-20 as ‘post-Greta’ years.

We use a list of climate related words, to extract quotes related to climate change that we focus on in this project. Once we have the climate related datasets per year, we save them as pickle files, in order to use and reuse them efficiently when needed. Using the WikiData and WikiLabels datasets, we link the Wiki attributes to the corresponding speakers and extract these in separate datasets for each year. We then use the speakers dataset to perform some analyses on their gender, age, nationality and political party. We focus on the possible changes in gender and age distribution over the years, in order to have an idea of a "typical" climate speaker profile. Later on, we will see how Greta Thunberg compares to this speaker profile and if she influenced some major changes, since her apparition on the climate debate stage.

The sentiment analysis of the quotes is performed using a pre-trained model from the Flair library (en-sentiment) that was trained on the IMDB dataset. After each quote has been attributed a sentiment (Positive/Negative [0,1]) we are able to analyse how different groups speak about climate change and if there is any variance between them. To measure polarization, we focus on the average sentiment of certain groups express and additionally focus on the topics that they are quoted on.
For the groups we focus on gender, age and political affiliation, as we believe that since Greta Thunberg has appeared in the public, there is a larger diversity of people being quoted about climate change.

Language complexity is analysed using the textstat library. First, we look into the language complexity of individual people and groups and then we look at how it evolves over time. At the same time, we looked into the number of quotes extracted each year and assumed an increasing number of quotes as an expression of the growing debate on climate change. If the latter correlates with a decrease in complexity of the language used overall in the quotes, we could question the link between the two.

In order to analyse the impact of natural disasters on our previous results, we extracted the relevant data and after some first basic analyses, we focus on its correlation with the sentiment scores of the speakers. In this way, we are able to see if new extreme weather events have an impact on how people talk about climate change and how the climate debate change, in general.

### 5. Jupyter Notebooks:

The code for this project is split between four jupyter notebooks and they should be read in the following order:
- *00 Data exctraction*
- *01 Metrics analysis*
- *02 Text Analysis*
- *03 Natural Disasters*

### 6. Timeline:

- *26.11.21 - 02.12.21*: Extracting climate related dataframes from quotebank; extracting WikiData attributes of speakers
- *03.12.21 - 09.12.21*: Grouping the speakers and analysis of attributes distribution; sentiment analysis; analysing language complexity; plotting results
- *10.12.21 - 17.12.21*: Finishing up analysis and results; exporting the plotly plots; writing the data story

### 7. Organization within the team:

- **Alexandre Reis de Matos**: Data extraction using dictionary, scoring algorithm for quotes (not used in the end), natural disasters analysis, Datastory writing
- **Cezary Januszek**: Extracting WikiData and WikiLabels, aggregating speakers into groups and analysis, creating plotly plots for Datastory
- **Hugo Casademont**: Coordination, troubleshooting, server hosting, setup of webiste, code review, creating plotly plots for Datastory 
- **Hannah Casey**: Sentiment and language complexity analysis, plotting results, Datastory writing, group representative for TA's feedback
