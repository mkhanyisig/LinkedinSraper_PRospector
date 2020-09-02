## LinkedIn Scraper

*Purpose*

Automates the process of getting scraping Linkedin profile contents for creating an object field and profile template containing this information. 

### Scapers

Use Selenium Chrome webdriver for browsing through the webpages(Linkedin) and BeatifulSoup(bs4 library) to save html DOM of loaded profile pages. Object attributes selected and scraped using imported library functions

*Linkedinscraper.py or scraper_general.py*

Hard-coded "Author Profiles" csv file, which is in the column format *[name , URL]* where each URL link is scraped. Each scraped object is added to the JSON list of profiles in *profiles.json*. Other lists include *authors.json, companies.json, authors_education.json* , which store this info for each author. 

*_Usage_*

<pre><code>
python scrape_general.py
</code></pre>

*scrape profile*

Same as general scraper, but takes in the author profiles csv file as a command line argument. This avoids hardcoding solutions.

*_Usage_*

<pre><code>
// format: scrape_profiles.py <csv filename>
python scrape_profiles.py test_profiles.csv
</code></pre>

## Profile Template

This is a raw HTML template which searches through the profiles script dt variable (dt is the list of JSON profiles in profiles.js) and given the name to look for in search.js, populates the template with the *author profile object attributes*

<img src="https://github.com/mkhanyisig/RandomCodeSamples/blob/master/Screen%20Shot%202020-09-02%20at%201.10.54%20AM.png">





