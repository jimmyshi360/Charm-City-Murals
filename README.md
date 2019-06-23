https://jimmyshi360.github.io/charmcity/

Charm City Murals is an Augmented Reality application that allows users to
discover the Baltimore mural landscape from their phones through a webapp. This
project incorporates machine learning techniques, computer vision, and a smooth
front-end experience.

![](https://media.giphy.com/media/cRNbBPOAmLdkdbnXhB/giphy.gif) ![alt
text](https://i.imgur.com/KltToVr.png) ## How does it work?

Users can explore a virtual map of Baltimore. The map displays designated
markers of murals, all of which were documented by STAE and the Baltimore City
Government. A simple touch of the screen (or the click of a button on laptops)
displays the location, creators, and image of the selected mural. Scrolling
further down, users can use their camera to identify a mural while out in the
city of Baltimore. Pointing the camera to any given mural will display relevant
details about the artwork in Augmented Reality.

## Why does this matter?

Baltimore is a city of creatives. Local artists use their work as a way to
connect people and communities, and to express the city's unique history and
personality so central to its identity. This application showcases the much
lauded artistic scene in Baltimore City, yet also reveals a deeply rich past,
and a dynamic, complex present permeating throughout the nation. Most
importantly, however, murals express the current social and political climate,
sometimes strongly enough to become a form of activism and bring to light the
community's struggles. Overall, this application encourages our residents to
explore the city and is an important step forward in celebrating and
acknowledging public art as a voice of charm city.

For example-- Freddie Gray murals, Baltimore Love Project

## Technical stack.

Our application uses a wide range of tools and frameworks. Many thanks, to Stae
City Data and the Baltimore City Government for their data sources.
1. HTML5 to bring AR to your phone browser, making our
   experience immediately available to everyone.
2. Built on top of the light weight microframework Flask, to help create a
   robust API.
3. Uses custom segmentation code and object detection code for murals, using
   the power of OpenCV.
4. Extensive data exploration in bash to aggregate and expand training data for
   our CNN by using city data images.
5. Implements [Augmentor](https://arxiv.org/abs/1708.04680) to help supplement
   our sparse data set of 170 images into countless new ones.
6. Utilized [transfer
   learning](https://www.cse.ust.hk/~qyang/Docs/2009/tkde_transfer_learning.pdf)
   from [TensorFlow Art](https://github.com/nitroventures/tensorflow-art) as an
   artwork classifier.
7. Wrote custom network for mural categorization. We built our model with NumPy
   and Tensorflow. In particular, we implemented a dual encoder convolutional
   neural network for unsupervised feature comparision. This essentially builds
   a "mural vector space" allowing the model, allowing for any murals to be
   quickly lookup and compared.
8. Used [Tensorboard](http://tensorboard.charmcitymurals.com/) for training
   validation and great visualizations.
9. Augmented Reality using HTML and data derived from OpenCV to provide
   information as overlay on the captured image.
10. Frontend implemented using Bootstrap,
    [particle.js](https://vincentgarreau.com/particles.js), Smooth Parallax
    scrolling, and [MapBox](mapbox.com/studio)
11. Services: Domain name using domain.com and server using Google Cloud
    Compute systems.

### What's next?

- Allow artists to virtually display their ideas onto a wall to see what it
  would look like. Note, [we did prototype
  this.](https://github.com/jshi22/HopHacksDreamTeam/blob/master/scratch/wall.py)
- Upload this "virtual" mural and allow the community to vote on it- represents
  community's values
- Aggregate data so all markers have images
- Virtual tour of Baltimore by mural hopping

Thanks!
