import pandas as pd

# http://jmcauley.ucsd.edu/data/amazon/
# http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Cell_Phones_and_Accessories_5.json.gz

df = pd.read_json('[%s]' % ','.join(open('../reviews_Amazon_Instant_Video_5.json').readlines()))

print df.describe()

# reviewerID - ID of the reviewer, e.g. A2SUAM1J3GNN3B
# asin - ID of the product, e.g. 0000013714
# reviewerName - name of the reviewer
# helpful - helpfulness rating of the review, e.g. 2/3
# reviewText - text of the review
# overall - rating of the product
# summary - summary of the review
# unixReviewTime - time of the review (unix time)
# reviewTime - time of the review (raw)
print df.columns

# print df.overall.value_counts()
# print df.reviewText.str.len()
print df.reviewerID.value_counts()
print df[df.reviewerID == 'A36SL1P1YOIXL5']

df['sl'] = df.summary.str.len()
df['rl'] = df.reviewText.str.len()

print df.corr('pearson')

print df.asin.value_counts()

print df[df.asin == 'B00I3MPDP4'].overall.mean()

print df.shape
