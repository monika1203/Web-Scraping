## Question: Collect some price data about books from the Books to Scrape website. Specifically, to scrape and capture the following book related 
information - book category, book title, star rating and price. Once captured, output the results to a CSV file.

### Input Used: http://books.toscrape.com/

### Output: book_data.csv

### Requirements Overview
1. Examine the HTML returned from the Books to Scrape top-level URL. Your objective is to identify and extract book category and the book category URL information from this page.
2. For each book category URL, follow the URL to the book category page. You may restrict your data scraping to the first page of books returned for the category URL.
3. For each of the books on a category page, capture the book title, star rating and price.
4. Convert the ordinal star rating data to a numeric scale. For example, the string ‘star-rating One’ would be converted to the number 1, ‘star-rating Two’ would be converted to 2, and so on.
5. For each book, output one line containing the book category, title, numeric star rating and price to a CSV file.
