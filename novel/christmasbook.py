"""ChristmasBook.py

Original file is located at
    https://colab.research.google.com/drive/1vlSFQIlRDXxaOJbdhnjb9FOXrDqQx4X-
"""

import random

#Options

inputText = "christmas.txt"

names = ["Santa Claus","Santa","The Grinch", "Grinch", "Tim Allen", "Jimmy", "Turbo Man", "Rudolph the Red Nosed Reindeer", "Rudolph", "Santa Claus", "Santa Claus", "Santa", "Santa", "Jim Carrey", "Buddy the Elf", "Buddy", "Dad", "Ted", "Jamie", "Johnny", "Scott", "Calvin", "Susan", "Perry", "Charlie", "Comet", "Cupid", "Bernard", "Mrs. Claus", "John McClane", "Jesus", "Jesus Christ", "Jesus", "Jesus Christ", "Jesus", "Jesus Christ", "Jesus", "Jesus Christ", "Jesus", "Jesus Christ", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "Santa", "The elf", "The elf", "The elf", "The elf", "The elf", "The elf", "The Grinch", "The Grinch", "The Grinch", "The Grinch", "The Grinch", "The Grinch", "Hulk Hogan", "Alan Rickman", "A Jolly Penguin", "Mr. Narwhal", "Kramer from Seinfeld", "Michael Jordan", "Barry", "Kanye West", "God", "Shaq", "The Ghost of Christmas Past", "The Ghost of Christmas Present", "The Ghost of Christmas Future", "Snoop", "Charlie Brown", "Batman", "The Joker"]

times = ["the night before Christmas", "Christmas eve", "Christmas morning", "one somber and snowy night", "a dreary midnight in the midst of the Christmas season", "a snowy winter morning", "a cold and relaxing winter afternoon"]

speech = ["said to", "told", "exclaimed toward", "whispered to"]
recentNames = [random.choice(names), random.choice(names)]
intro = "Once upon a time, on " + random.choice(times) + ", " + recentNames[0] + " " + random.choice(speech) +" " + recentNames[1] + ", "

# Commented out IPython magic to ensure Python compatibility.
#Setup Block 1


from __future__ import absolute_import, division, print_function, unicode_literals

try:
  # %tensorflow_version only exists in Colab.
#   %tensorflow_version 2.x
except Exception:
  pass
import tensorflow as tf

import numpy as np
import os
import time

# Read, then decode for py2 compat.
text = open(inputText, 'rb').read().decode(encoding='utf-8')
# length of text is the number of characters in it
#print ('Length of text: {} characters'.format(len(text)))

# Take a look at the first 250 characters in text
#print(text[:250])

# The unique characters in the file
vocab = sorted(set(text))
#print ('{} unique characters'.format(len(vocab)))

# Creating a mapping from unique characters to indices
char2idx = {u:i for i, u in enumerate(vocab)}
idx2char = np.array(vocab)

text_as_int = np.array([char2idx[c] for c in text])

#print('{')
#for char,_ in zip(char2idx, range(20)):
#    print('  {:4s}: {:3d},'.format(repr(char), char2idx[char]))
#print('  ...\n}')

# Show how the first 13 characters from the text are mapped to integers
#print ('{} ---- characters mapped to int ---- > {}'.format(repr(text[:13]), text_as_int[:13]))

# The maximum length sentence we want for a single input in characters
seq_length = 25  #25? 100?
examples_per_epoch = len(text)//(seq_length+1)

# Create training examples / targets
char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)

#for i in char_dataset.take(5):
#  print(idx2char[i.numpy()])


sequences = char_dataset.batch(seq_length+1, drop_remainder=True)

#for item in sequences.take(5):
#  print(repr(''.join(idx2char[item.numpy()])))

def split_input_target(chunk):
    input_text = chunk[:-1]
    target_text = chunk[1:]
    return input_text, target_text

dataset = sequences.map(split_input_target)


#for input_example, target_example in  dataset.take(1):
#  print ('Input data: ', repr(''.join(idx2char[input_example.numpy()])))
#  print ('Target data:', repr(''.join(idx2char[target_example.numpy()])))

#for i, (input_idx, target_idx) in enumerate(zip(input_example[:5], target_example[:5])):
#    print("Step {:4d}".format(i))
#    print("  input: {} ({:s})".format(input_idx, repr(idx2char[input_idx])))
#    print("  expected output: {} ({:s})".format(target_idx, repr(idx2char[target_idx])))


# Batch size
BATCH_SIZE = 64

# Buffer size to shuffle the dataset
# (TF data is designed to work with possibly infinite sequences,
# so it doesn't attempt to shuffle the entire sequence in memory. Instead,
# it maintains a buffer in which it shuffles elements).
BUFFER_SIZE = 10000

dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)

#dataset

# Length of the vocabulary in chars
vocab_size = len(vocab)

# The embedding dimension
embedding_dim = 256

# Number of RNN units
rnn_units = 1024

def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
  model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim,
                              batch_input_shape=[batch_size, None]),
    tf.keras.layers.GRU(rnn_units,
                        return_sequences=True,
                        stateful=True,
                        recurrent_initializer='glorot_uniform'),
    tf.keras.layers.Dense(vocab_size)
  ])
  return model

model = build_model(
  vocab_size = len(vocab),
  embedding_dim=embedding_dim,
  rnn_units=rnn_units,
  batch_size=BATCH_SIZE)

for input_example_batch, target_example_batch in dataset.take(1):
  example_batch_predictions = model(input_example_batch)
  #print(example_batch_predictions.shape, "# (batch_size, sequence_length, vocab_size)")

#model.summary()

#sampled_indices = tf.random.categorical(example_batch_predictions[0], num_samples=1)
#sampled_indices = tf.squeeze(sampled_indices,axis=-1).numpy()

#sampled_indices

#print("Input: \n", repr("".join(idx2char[input_example_batch[0]])))
#print()
#print("Next Char Predictions: \n", repr("".join(idx2char[sampled_indices ])))

def loss(labels, logits):
  return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)

example_batch_loss  = loss(target_example_batch, example_batch_predictions)
#print("Prediction shape: ", example_batch_predictions.shape, " # (batch_size, sequence_length, vocab_size)")
#print("scalar_loss:      ", example_batch_loss.numpy().mean())

model.compile(optimizer='adam', loss=loss)

# Directory where the checkpoints will be saved
checkpoint_dir = './training_checkpoints'
# Name of the checkpoint files
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")

checkpoint_callback=tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_prefix,
    save_weights_only=True)

EPOCHS=100

history = model.fit(dataset, epochs=EPOCHS, callbacks=[checkpoint_callback])

tf.train.latest_checkpoint(checkpoint_dir)

model = build_model(vocab_size, embedding_dim, rnn_units, batch_size=1)

model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))

model.build(tf.TensorShape([1, None]))

#model.summary()

def generate_text(model, start_string):
  # Evaluation step (generating text using the learned model)

  # Number of characters to generate
  num_generate = 1000

  # Converting our start string to numbers (vectorizing)
  input_eval = [char2idx[s] for s in start_string]
  input_eval = tf.expand_dims(input_eval, 0)

  # Empty string to store our results
  text_generated = []

  # Low temperatures results in more predictable text.
  # Higher temperatures results in more surprising text.
  # Experiment to find the best setting.
  temperature = 0.4

  # Here batch size == 1
  model.reset_states()
  for i in range(num_generate):
      predictions = model(input_eval)
      # remove the batch dimension
      predictions = tf.squeeze(predictions, 0)

      # using a categorical distribution to predict the word returned by the model
      predictions = predictions / temperature
      predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

      # We pass the predicted word as the next input to the model
      # along with the previous hidden state
      input_eval = tf.expand_dims([predicted_id], 0)

      text_generated.append(idx2char[predicted_id])

  return (start_string + ''.join(text_generated))

print(generate_text(model, start_string=u"C"))

output1 = open(inputText, 'rb').read().decode(encoding='utf-8') 

for i in range(50):
  print(i, "/ 50")
  output1 += generate_text(model, start_string=u"Christmas")

!pip install markovify
!pip install weasyprint
import markovify
import random
from weasyprint import HTML

text_model = markovify.Text(output1)
verbs1 = ["SAVED", "EXPERIENCED", "ALMOST FORGOT", "LEFT", "RUINED", "NEARLY DESTROYED", "FOUND", "DISCOVERED THE MEANING OF", "INHERITED"]

novel = "<h1>THE DAY THAT " + random.choice(recentNames).upper() + " " + random.choice(verbs1) + " CHRISTMAS</h1><br><p>"

thing = text_model.make_sentence()
word1 = random.choice(thing.split())
novel += f"</p><h2>INTRO: " + word1.upper() + "</h2><p><br>"

numChampters = random.randint(10,50)
chLength = (60 - numChampters) * 10

novel += intro + text_model.make_sentence()

for i in range(1, numChampters):
  thing = text_model.make_sentence()
  if(thing != None):
    word1 = random.choice(thing.split())
  else:
    word1 = "Christmas"
  novel += "</p><br><br><h2>Chapter " + str(i) + ": " + word1.upper() + "</h2><p>"
  nameThing1 = random.choice(recentNames)
  nameThing2 = random.choice(recentNames)
  recentNames = [nameThing1, nameThing2, random.choice(names)]
  lastName = ""
  for k in range(chLength):
    #nameNum = random.randrange(len(recentNames) - 1)
    #currentName = recentNames[nameNum]
    #recentNames.pop(nameNum)
    currentName = random.choice(recentNames)
    theSentence = text_model.make_sentence()
    if(theSentence != None):
      if(currentName == lastName):
        novel += "     " + theSentence + "<br>"
      else:
        novel += "<br>" + currentName + ": " + theSentence + "<br>"
    #recentNames.append(currentName)
    if(random.randint(0,50) > 48):
      recentNames.append(random.choice(names))
    lastName = currentName


html_template = f"""
<html>
  <head>
  <title>MERRY CHRISTMAS</title>
  <style>
    body {{
      font-family: "Times New Roman";
      color: white;
      background-color: red;
    }}
  </style>
  </head>
  <body>
  {novel}
  </body>
</html>
"""

# Finally, this line saves that template as a PDF using the HTML module of WeasyPrint
HTML(string=html_template).write_pdf("christmas_novel.pdf")