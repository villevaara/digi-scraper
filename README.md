# digi-scraper
Webscraper for getting raw data from the 'Digi' open Newspaper archives of the National Library of Finland

Usage:

http://digi.kansalliskirjasto.fi/sanomalehti/search?query=&requireAllKeywords=true&fuzzy=false&hasIllustrations=false&startDate=1920-01-01&endDate=1920-02-01&orderBy=DATE&pages=&resultMode=TEXT&page=1

1. get daily csv:s
2. get number of pages / newspaper in csv (selenium) and update csv
3. get each page xml, txt, img. (wget)
    * eg.: http://digi.kansalliskirjasto.fi/sanomalehti/binding/818572/page-1.xml
98. ???
99. profit

todo:
!get also perodicals
iteroi hakemistot läpi, tarkista onko .csv, jos on niin aja rapsuli
