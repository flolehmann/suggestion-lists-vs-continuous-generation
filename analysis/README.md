# Data Evaluation
Python scripts for evaluating the data stored from the study. <br>
The `constants.py` file provides some constants and common function used by the other files. The other files offer functions for getting different informations out of the stored csv-Files.

### Actions
`actions.py` provides functions which give informations about the amount of actions used. Every interaction with the user interface is counted as an action. That means every press on the keyboard is counted as an action, as well as the click on a button to start the generation or to select a suggestion.

### Backspaces
`backs.py` provides functions which give informations about the use of backspaces and backspace-sequences. Backspace-sequences are sequences of actions which only contain Backspace-Actions. So deleting a seven-character-long word causes a backspace-sequence with the length seven.

### Generation
`generationeval.py` provides functions which give informations about the amount of how often the generation is started and how often the new options button on Writing with suggestions got used.

### Questions
`questioneval.py` provides functions which give informations about the results from the Likert Questions. The Likert Questions are the questions which were asked directly after writing a text during the study. They all had to be answerd with a five-point-agreement-scale from "strongly agree" to "strongly disagree".

### Table plots
`tblplots.py` provides a function for displaying special csv-files as divering bar charts.

### Words per minute
`wpm.py` provides functions which give informations about the length of the texts writting during the study and the speed (words per minute) with which they are written.




