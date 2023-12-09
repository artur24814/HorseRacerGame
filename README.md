# HorseRacerGame

<img src="https://camo.githubusercontent.com/1971c0a4f776fb5351c765c37e59630c83cabd52/68747470733a2f2f7777772e707967616d652e6f72672f696d616765732f6c6f676f2e706e67">
<ul>
<h2>Contents</h2>
<li><a href="https://github.com/artur24814/HorseRacerGame?tab=readme-ov-file#releases"><h3>releases</h3></a>A list of all our future and existing releases</li>
<li><a href="https://github.com/artur24814/HorseRacerGame?tab=readme-ov-file#clone_project"><h3>clone and run this project on your local machine</h3></a>how run projects in your computer</li>
</ul>
<hr>
<h1 id="releases">Releases</h1>
<h3>Version 1.1.0. 10.12.2023</h3>
<ul>
<li>After each race, each horse receives points that will be important in calculating `start_pos` for the next race (User can see this changes only in terminal);</li>
<li>Implementation of the standard python sqlite3 database;</li>
<li>ORM for game models (CRUD for Horse);</li>
</ul>
<h3>Version 1.2.0. 16.12.2023</h3>
<ul>
<li>Adding new screens: Home screen when loading the game and the betting screen;</li>
<li>Depending on the horse's `start_pos`, the player can see how much money they can receive if he bet on a specific horse (Implementation of the win rate);</li>
<li>Creating automated tests in pytest;</li>
<li>ORM for game models (CRUD for Player);</li>
</ul>
<h3>Version 1.2.0. 30.12.2023</h3>
<ul>
<li>The player can see a table with the winning rate of each horse on the betting screen. And he can change the horse's name and put money on it;</li>
<li>After the race, players' money is recalculated;</li>
<li>If the Player has no money, the game ends;</li>
</ul>


<hr>

<h3 id="clone_project">Clone and Run a Game</h3>

Before diving let’s look at the things we are required to install in our system.

<a href='https://www.python.org/downloads/'>python -> </a>

Install virtual environment

`pip install virtualenv`


Now, we need to clone project from Github:-
<p>Above the list of files, click Code.</p>
<img src="https://docs.github.com/assets/cb-20363/images/help/repository/code-button.png">

Copy the URL for the repository.
<ul>
<li>To clone the repository using HTTPS, under "HTTPS", click</li>
<li>To clone the repository using an SSH key, including a certificate issued by your organization's SSH certificate authority, click SSH, then click</li>
<li>To clone a repository using GitHub CLI, click GitHub CLI, then click</li>
</ul>
<img src="https://docs.github.com/assets/cb-33207/images/help/repository/https-url-clone-cli.png">

Open Terminal.

Change the current working directory to the location where you want the cloned directory.

Type git clone, and then paste the URL you copied earlier.

`$ git clone „paste your copied link”`

Press Enter to create your local clone.

```
$ git clone „your copied link”
> Cloning into `Spoon-Knife`...<br>
> remote: Counting objects: 10, done.
> remote: Compressing objects: 100% (8/8), done.
> remove: Total 10 (delta 1), reused 10 (delta 1)
> Unpacking objects: 100% (10/10), done.
```

Making and Activating the Virtual Environment:-

`python -m venv env`

*If the `python` command doesn't work, try `python3`

`env\Scripts\activate`

Install the project dependencies:

`pip install -r requirements.txt`

Write this code
<code>python start.py<code>

*If the `python` command doesn't work, try `python3`

<p style="font-size:20px">Have fun &#129409;</p>