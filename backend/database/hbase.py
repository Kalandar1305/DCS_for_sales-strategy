import happybase
from mongodb import db
# Connect to HBase
connection = happybase.Connection('localhost', port=9090)
table = connection.table('reviews')

def getReviews(product_id):
    # Establish connection to HBase

    # Select table and column family
    col_family = 'review_data'

    # Scan table for all rows with matching product_id
    rows = table.scan(row_prefix=product_id.encode())

    # Create list of all reviews for the matching product_id
    reviews = []
    for row in rows:
        review = {}
        for column, value in row[1].items():
            # Decode column and value from bytes to string
            column = column.decode('utf-8')
            value = value.decode('utf-8')

            # Add column and value to review dictionary
            review[column] = value

        # Add review to list of reviews
        reviews.append(review)

    # Return list of reviews for the matching product_id
    return reviews

def putReviews(data):
    # Connect to HBase

    
    # Define the column family and column names
    col_family = b'review_data'
    col_names = [b'review_title', b'content', b'rating', b'likes', b'time', b'product_title', b'average_rating', b'source', b'price', b'sentiment']
    
    # Put each review in the HBase table
    for review in data:
        # Define the row key as the product_id and review_title
        row_key = f"{review['product_id']}::{review['review_title']}"
        
        # Create a dictionary of the review data with column names as keys and values as values
        review_data = {col_names[i]: str(review[col_names[i].decode()]).encode() for i in range(len(col_names))}
        
        # Put the data in the HBase table
        table.put(row_key.encode(), review_data)