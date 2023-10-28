def return_sentiment(review): 
    if isinstance(review, str):
        from textblob import TextBlob
        blob = TextBlob(review)
        polarity = blob.sentiment.polarity
        if polarity <= -0.2:
            return 0
        elif polarity >= 0.2:
            return 2
        else:
            return 1
    else:
        return 1