## Feature 1

The marketing team have decided that they want to update the website. They want to have a part of the website that shows how many urls they have shortened. So for example if John made a request to shorten `www.google.com`, Alice also made a request to shorten `www.google.com` and Bob made a request to shorten `www.amazon.com`, then the website should say __Number of shortened urls: 3__.

To provide this feature you need to provide an api endpoint `/shortened_urls_count` that returns an integer.

Bonus features:
- If Bob makes 20 requests from the same ip then the number of shortened urls count should only increase by one.

## Feature 2
The marketing team have decided to update the website. They want to include a list of the 10 most shortened urls. So for example if John made a request to shorten `www.google.com`, Alice also made a request to shorten `www.google.com` and Bob made a request to shorten `www.amazon.com`, then the website should say __Most popular urls: www.google.com, www.amazon.com__
