Example of how to use ``study_image`` method


```python

# importing the method in relative form
from misctools.ext import study_image, check_valid_url

# url have to be valid, if u want to know if a url is valid, pls use check_valid_url

if check_valid_url(<url>):
    study = study_image(<url>)
    print(study)
    """
    This will return a matplotlib interface plotting the original image and a matrix of the most colors used in the image
    """
else:
    ...
```