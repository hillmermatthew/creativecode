# RANDOMLY GENERATED CHRISTMAS MOVIE SCRIPTS

I created code that randomly generates Christmas movie scripts when given an input text file containing a bunch of pre-existing Christmas movie scripts, songs, and novels.  You can try it out in a Google Colab python notebook [here](https://colab.research.google.com/drive/1vlSFQIlRDXxaOJbdhnjb9FOXrDqQx4X-), or download [the source code](christmasbook.py) and try to run it directly. 
Alternatively, you can view either of these example pdfs that I already generated: [1](christmas_novel1.pdf) or [2](christmas_novel2.pdf)

## How Does it Work?
So I start by running a really big [source text file](christmas.txt) through [TensorFlow's character-based RNN code](https://www.tensorflow.org/tutorials/text/text_generation), then append a bunch of output text from that to a copy of the original input text, then run all of that through a Markov chain using [Markovify](https://github.com/jsvine/markovify).  That way, the Markov chain input is a mix of the original source text and some goofy nonsense words/sentences generated by the neural network.  After that I format the sentence output to look like lines in a movie script.  The character names are just taken from a big list of names I wrote in.  The title of the story itself is just a little template with a few random words chosen from lists I wrote, and the titles of each chapter are just singular random words taken from the source text.

Anyway, so once we have a bunch of random sentences, I formated them into some HTML and converted it into a PDF file using weasyprint.
