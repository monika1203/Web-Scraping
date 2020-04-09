

from requests.exceptions import HTTPError
import requests
from bs4 import BeautifulSoup
import re
import csv

def simple_get(url, params=None):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        resp = requests.get(url, timeout=5, params=params)
        # If the response was successful, no Exception will be raised
        resp.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        # sanity check
        # is this HTML?
        content_type = resp.headers['Content-Type'].lower()
        # True if the response seems to be HTML, False otherwise.
        # Followed by 'death'
        assert content_type.find('html') >= 0

    return resp

def who_category(url):

    resp = simple_get(url)
    # get the decoded payload.  the text() method uses metadata to devine encoding.
    html = resp.content
    soup = BeautifulSoup(html, 'html.parser')

    # to be returned
    books_category_list = []
    books_category_link_list = []
    
    # After inpspection of the HTML, I found that img elements
    # that have a title attribute that begin with the text 'Slide'
    # will give me the actor names I after (mostly anyway)
    for link in soup.find_all('a', href=re.compile(r'^catalogue/category/books/.*')):
        books=link.text
        print(books)
        books_category_list.append(books.strip())
        books_category_link_list.append(link['href'])
    return books_category_list,books_category_link_list



def main():
    
    EW_URL = 'http://books.toscrape.com/'
    books_category_list,books_category_link_list = who_category(EW_URL)
    
#    print(books_category_list)
#    print(books_category_link_list)
#    Books_dict = {}
    rating_dict = {'One':1 ,'Two':2,'Three':3,'Four':4,'Five':5}
    Books_dict = []
    for links,books_category in zip(books_category_link_list,books_category_list):
#        print(links)
        Subcategory='http://books.toscrape.com/' + links
#        print(Subcategory)
        resp=simple_get(Subcategory)   
        html = resp.content
        soup = BeautifulSoup(html, 'html.parser')  
        
        
        for attributes in soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
            Bookname_ob=attributes.find('img',class_='thumbnail')
            Bookname=Bookname_ob['alt']

            Ratings=attributes.find('p',class_=re.compile(r'star-rating.*'))
            Books_Rating=(Ratings['class'][1])
           
            Price=attributes.find('p',class_='price_color')
        
            Books_dict.append({'Title':str(Bookname),'Rating':rating_dict[Books_Rating],'Price':str(Price.text),'Category':str(books_category)})
    print(Books_dict)     

    with open('book_data.csv', mode='w', newline='') as csv_file:
        writer=csv.writer(csv_file,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Book_name','Ratings', 'Price','Category'])
        for row in Books_dict:
            writer.writerow([row['Title'],row['Rating'],row['Price'],row['Category']])


if __name__ == "__main__":
    main()