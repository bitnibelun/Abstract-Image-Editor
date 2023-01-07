## Editor

![editor](https://user-images.githubusercontent.com/86565212/201485768-70e98846-4187-4bb9-95bd-9e9ef026865f.jpg)

## Sample

![sample](https://user-images.githubusercontent.com/86565212/201484188-b0629da3-f7a3-40b3-a6b0-e88479566168.jpg)

## About
This program is an abstract image editor written in Python using PyQt5.
This is a first draft, and it's an ongoing project that still needs a lot of work.
The program is slow as it is right now with larger images but can be more efficient with Cython or using other techniques.
## Vision

This program was created for learning, to experiment, play around with images, and
as a base on which more advanced effects can be created.

## Dependencies

1. Python <= 3.10
2. PyQt5

## Running the code

**Make sure that both python 3.10 and PyQt5 are installed.**

There are various ways of running the code:

* IDE:
  1. Use a python IDE such as PyCharm or VS code.
  2. Using the IDE open the folder containing the project.
  2. Select and run the abstract_image_editor.py file.

* Terminal/Command line:
  1. Navigate to the folder containing the project.
  2. Run the program with: 
    ~~~~
    python abstract_image_editor.py
    ~~~~
  
 * Create an executable
   1. Install auto-py-to-exe
   2. Run auto-py-to-exe with:
   ~~~~
   auto-py-to-exe
   ~~~~
   3. When the GUI pops up:
      - Select abstract_image_editor.py for Script Location
      - Choose the One Directory option for OneFile
      - Select abstract_image_editor.ui for the Additional Files option
      - Click on the CONVERT PY. TO EXE. button

      There should be a new folder in the script location. Inside the folder
      there should be an application file from which you can run the program.
      
