# ada-2021-project-hach
## Is the Greta effect fake news?
### An analysis of the public debate on climate change.

### Abstract: 
Climate change has been a topic dominating the public debate in the media for a while now. Since 2018, the Friday for Future movement has taken to the streets in an attempt to be heard by policy makers. In our project on the Quotebank dataset we will analyze how the public debate on climate change has evolved over the recent years, while focusing on Greta Thunberg’s impact on it. We will explore who is quoted on climate change, what they are saying and how they are saying it. We want to quantify the effect and influence Greta had on the debate, in hopes of better understanding the phenomenon she has become. We want to tell the story of ‘the Greta effect’ in a different way, showing just how big her impact was on the debate in the media.
### Research Questions :
* Which speakers are quoted on climate change, what do they have in common and what are their differences?
  * In terms of age, gender and political affiliation
* How are different groups speaking about climate change?
  * How long are the quotes?
  * Positive or negative sentiment?
  * What is the difference in language complexity?
* How has the approach to climate change evolved in recent years?
  * Has debate become more polarized? 
  * Has the language complexity changed? 
  * Is there any correlation between scientific vulgarization and the growing debate on climate change?
* Is there a quantifiable difference in the debate using the aforementioned metrics before and after Greta Thunberg?

### Proposed Datasets: 
We will be using WikiData and WikiLabels to gather attributes and information about the speakers. 
In order to extract quotes related to climate change, we are using a list of similar words obtained through a web request here: https://relatedwords.org/relatedto/climate%20change 
### Methods: 
Our group is collaborating on a jupyter hub hosted by Infomaniak and we will be using jupyter notebooks for the analysis of the data. 
In order to extract data frames from the Quotebank dataset, we’re loading a specific number of rows into memory using read_json with a chunksize of 1’000’000, extracting the quotes about climate change and then saving them to .pkl files for later use.
As Greta Thunberg appeared on the public stage in August 2018, but really took off in 2019, we will focus on 2017-18 as ‘pre-Greta’ and 2019-20 as ‘post-Greta’ years. 

From related words, we get a large list of approximately 750 words from the most similar to least similar one and their respective scores of similarity to “climate change”. For now, we only keep the top 10. We then perform stemming on the 10-word list and transform the list into a regex used to find all quotes with at least one match with the regex. Finally, we score and sort the quotes by the number of words they contain from the list. Further improvements will be to also take into account the score of similarity of each word given by the website and give a score to the quotes based not only on the number of words, but also on the weight of those words. We are aware this will bias the query towards longer quotes, as they contain more words and therefore have a higher probability of getting a bigger score. We are taking this into account but are assuming that longer quotes contain more data which will be important for sentiment analysis and language complexity analysis.

The sentiment analysis is performed using a pre-trained model from the Flair library (en-sentiment) that was trained on the IMDB dataset. After each quote has been attributed a sentiment (Positive/Negative [0,1]) we will be able to analyze how different groups speak about climate change and if there is any variance between them. To measure polarization, we will focus on the average sentiment certain groups express and additionally focus on the topics that they are quoted on. 
For the groups we will focus on gender, age and political affiliation, as we believe that since Greta Thunberg has appeared in the public, there is a larger diversity of people being quoted about climate change. 

Language complexity will be analysed using the textstat library. First, we will look into the language complexity of individual people and groups and then we will see how it evolves over time. At the same time, we will look into the number of quotes extracted each year and assume an increasing number of quotes as an expression of the growing debate on climate change. If the latter correlates with a decrease in complexity of the language used overall in the quotes, we could question the link between the two.

We will not analyze which news outlets quote which speakers. We assume the quotebank dataset to be USA-centric and thus biased in terms of speakers and topics discussed. 
### Proposed Timeline:
26.11.21 - 02.12.21: Extracting data frames from quotebank, scoring the quotes, extracting WikiData attributes on speakers
03.12.21 - 09.12.21: Grouping the speakers, sentiment analysis, analyzing language complexity, plotting results
10.12.21 - 17.12.21: Finishing up analysis and results, writing the data story

### Organization within the team:
Alexandre Reis de Matos: Data extraction using dictionary, scoring algorithm for quotes
Cezary Januszek: Extracting WikiData and Wikilabels, aggregating speakers into groups
Hugo Casademont: Server hosting, troubleshooting, coordination, writing Datastory, plotly
Hannah Casey: Sentiment analysis, language complexity analysis, plotting results, writing ReadMe and Datastory

### Questions for TAs:
