# www.charmcitymurals.com

Charm City Murals is an augmented reality application that allows users to discover the Baltimore mural landscape from their phones. This project incorporates machine learning techniques, computer vision, and extensive front-end technologies.

How does it work?

Using the web domain www.charmcitymurals.com, users can explore a virtual map of Baltimore. The map displays designated markers of murals, all of which were documented by STAE and the Baltimore City Government. A simple touch of the screen (or the click of a button on laptops) displays the location, creators, and image of the selected mural. Scrolling further down, users can use their camera to identify a mural while out in the city of Baltimore. Pointing the camera to any given mural will display relevant details about the artwork through overlayed text. 

Why does this matter?

Baltimore is a city of creatives. Local artists use their work as a way to connect people and communities, and to express the city's unique history and personality so central to the it's identity. This application showcases the much lauded artistic scene in Baltimore City, yet also reveals a deeply rich past, and a dynamic, complex present permeating throughout the nation. Most importantly, however, murals express the current social and political climate, sometimes strongly enough to become a form of activism and bring to light the community's struggles. Overall, this application encourages our residents to explore the city and is an important step forward in celebrating and acknowledging public art as a voice of charm city. 

For example-- Freddie Gray murals, Baltimore Love Project

Describe the technical stack.

Our application uses a wide range of tools and frameworks. First, we collected data from Stae City Data and the Baltimore City Government.
1. Camera integration for users to discover new murals using their phone camera. Implemented with modern WebHTML5 capabilities.
2. Object detection using OpenCV to process captured images, and Flask to send down information to our server.
3. Extensive data exploration to aggregate training data for our CNN by scraping existing data 
- [Augmentor](https://arxiv.org/abs/1708.04680) was used to help supplement our sparse data set of 170 data points into countless accomodations.
- Utilized [transfer learning](https://www.cse.ust.hk/~qyang/Docs/2009/tkde_transfer_learning.pdf) from [TensorFlow Art](https://github.com/nitroventures/tensorflow-art) as an artwork classifier.
4. Image comparison to categorize murals. Our model uses the machine learning principle of convolutional neural networks and is implemented with TensorFlow and NumPy.
- This is a variation of unsupervised learning. Our model uses a dual encoder model to compare unsupervised feature vectors. This essentially builds a "mural vector space" allowing the model to not be constrained by the number of murals that can be compared.
- [Tensorboard](http://tensorboard.charmcitymurals.com/)
5. Augmented reality using OpenCV displays the mural information as overlay on the captured image.
6. Frontend implemented using Bootstrap, [particle.js](https://vincentgarreau.com/particles.js), parallax scrolling, and [MapBox](mapbox.com/studio)
7. Domain name using domain.com and server using Google Cloud computing systems.

What's next?

- Allow artists to virutally display their ideas onto a wall to see what it would look like
- Upload this "virutal" mural and allow the community to vote on it- represents community's values
- Aggregate data so all markers have images
- Virtual tour of Baltimore by mural hopping



The city's murals are one of its most charming assets and showcase a growing city filled with creativity and promise.

Seen throughout Baltimore, Maryland, street art adds vibrancy to neighborhoods once marked by vacant lots and decaying buildings. The hundreds of murals spread throughout the city are as essential to its identity as crabcakes or the Inner Harbor. Baltimore art is a bright reminder that Charm City cares about creativity and knows how street artists can make a positive impact on their community.


