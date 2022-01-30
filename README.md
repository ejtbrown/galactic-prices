# galactic-prices
### Overview
The galactic-prices system is intended to parse Earthbreaker game system data
(in markdown format) and use it to generate prices for various goods in various
places in the galaxy. It was originally intended for the Star Wars subset of
the Earthbreaker rules.

### Architecture
The system is intended to operate from a Lambda function in AWS, read data from
github, and post the results in HTML format to an S3 bucket (from where users
can access it)
