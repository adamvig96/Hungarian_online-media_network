rm(list=ls())

library(readr)
library(dplyr)
library(tidyr)
library(ggplot2)
require(forcats)

# set data directory

data_dir = "/Users/vigadam/Dropbox/My Mac (MacBook-Air.local)/Documents/github/media_network/media_data/analysis_covid/data"

# read country mentions in TAGS

country_mentions_in_tags <- read_csv(paste(data_dir,"country_mentions_in_covid_tags.csv",sep="/")) %>% select(-1)

# read country mentions in TEXT

country_mentions_in_text <- read_csv(paste(data_dir,"country_mentions_in_covid_text.csv",sep="/")) %>% select(-1)
# read weekly covid data

covid_by_week <- read_csv(paste(data_dir,"covid_data_week.csv",sep="/")) %>% select(-1)



# left merge on tags:
left_on_tags <- merge(x = country_mentions_in_tags, y = country_mentions_in_text, 
                      by = c("week","page","iso3","month","country_hun"), all.x = TRUE) %>% 
                      arrange(iso3,page,week)

# merge left_on_tags with covid week data

left_on_tags <- merge(x = left_on_tags, y = covid_by_week %>% 
           select(weekly_new_cases_permillion,weekly_new_deaths_permillion,reproduction_rate,week,iso3), 
           by = c("week","iso3"), all.x = TRUE) %>% 
           replace_na(list(weekly_new_cases_permillion = 0, weekly_new_deaths_permillion = 0,reproduction_rate = 0))

left_on_tags <- merge(x = left_on_tags, y = covid_by_week %>% select(iso3,continent) %>% distinct(), by = "iso3", all.x = TRUE)


# Save file
write.csv(left_on_tags,paste(data_dir,"data_for_regression_leftmerge_on_tags.csv",sep="/"))




# left merge on text:
left_on_text <- merge(x = country_mentions_in_text, y = country_mentions_in_tags, 
                      by = c("week","page","iso3","month","country_hun"), all.x = TRUE) %>% 
  arrange(iso3,page,week)

# fill NA-s with 0, because text df is longer than tags df

left_on_text <- left_on_text %>% replace_na(list(mentions_tags = 0))


# merge left_on_text with covid week data

left_on_text <- merge(x = left_on_text, y = covid_by_week %>% 
                      select(weekly_new_cases_permillion,weekly_new_deaths_permillion,reproduction_rate,week,iso3), 
                      by = c("week","iso3"), all.x = TRUE) %>% 
                      replace_na(list(weekly_new_cases_permillion = 0, weekly_new_deaths_permillion = 0,reproduction_rate = 0))

left_on_text <- merge(x = left_on_text, y = covid_by_week %>% select(iso3,continent) %>% distinct(), by = "iso3", all.x = TRUE)


# Save file
write.csv(left_on_tags,paste(data_dir,"data_for_regression_leftmerge_on_text.csv",sep="/"))






