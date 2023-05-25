# Glee Power BI Dashboard

This project aims to create a Power BI dashboard that illustrates information regarding the various covers that had been done on the TV series, Glee.

Specifically, this project aims to:
1. Extract data from the show's Wikipedia pages ([songs](https://en.wikipedia.org/wiki/Lists_of_songs_in_Glee_(TV_series)), [episodes](https://en.wikipedia.org/wiki/List_of_Glee_episodes))
2. Transform and normalize data using Power Query 
3. Model the normalized data using a star schema 
4. Create visualizations 

---

## Context

As a Glee fan, I have always been curious how many covers the show has done the various details of these covers, such as which character did the most covers, which artist or band did the show cover the most, etc. 

Since I need to practice my Power Query skills, I decided to do this project to kill two birds with one stone. In doing so, I came across the topic of database normalization, which I implemented in Power Query as well. 

Once I had normalized the data, it was easy to create the necessary visualizations in Power BI.

## Files

```
.gitignore              - list of files/types to exclude in git commits
glee_dashboard.pbix     - Power BI dashboard; main file
glee_data_model.png     - photo of the final datal model 
glee_logo.png           - photo of the Glee logo; used in the dashboard
README.md               - documentation
```