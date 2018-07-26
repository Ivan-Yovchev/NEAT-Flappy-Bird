Neuroevolution of FlappyBird using NEAT
==========================================
A network is evolved to play a bare-bones version of FlappyBird using Neuroevolution of Augmenting Topologies (NEAT).

How-to
--------------

1. Install Python 3.5.x from [here](https://www.python.org/downloads/)

2. Install PyGame 1.9.x from [here](http://www.pygame.org/download.shtml)

3. Install NEAT-Python 0.92 from [here](https://neat-python.readthedocs.io/en/latest/installation.html)

4. Clone this repository: `git clone https://github.com/fricer/NEAT-Flappy-Bird.git` or use `Download ZIP` to download and extract.

5. To play the game:
   - Navigate to the repo directory
   - Run `python3 flappy_bird_play.py`
   - Use the <kbd>&uarr;</kbd> key to play and <kbd>Esc</kbd> to close the game

6. To train a network:
   - Navigate to the repo directory
   - Run `python3 flappy_bird_train.py`
   - Wait for the genetic algorithm to evolve a network. 
   - After the execution of the script a file named `winner` will be created containing the best performing individual of the population.
   - During the execution of the script information about the population (fitness, species etc) is printed in the terminal.
   - Using the <kbd>Esc</kbd> key during execution closes the game and terminates the evolution process i.e. a network is not trained and a `winner` file is not created
   
7. To use a trained network to play the game:
   - Navigate to the repo directory
   - Run `python3 flappy_bird_test.py`
   - The script will load the network from the `winner` file (if the file is missing or not in the same directory the script throws a `FileNotFoundError` exception) and procede to play the game.
   - A visualization of the network loaded from the `winner` file is also generated
   - Using the <kbd>Esc</kbd> key closes the game
  
  Notes
  ------
  The files `flappy_bird_play.py`, `flappy_bird_train.py` and `flappy_bird_test.py` contain a lot of code duplication and need to be refactored in the future. The file `flappy_bird_train.py` is well-commented, the other files are not. Pull requests are welcome both to refactor the code and to improve the now only bare-bones FlappyBird implementation.
