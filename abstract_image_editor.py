#--------------------------------------------------------------------------------------
Copyright (c) 2022 Alvaro Angel
    This program is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by 
    the Free Software Foundation, either version 3 of the License, 
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful, 
    but WITHOUT ANY WARRANTY; without even the implied warranty 
    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
    See the GNU General Public License for more details.

    You should have received a copy of the GNU 
    General Public License along with this program. 
    If not, see <https://www.gnu.org/licenses/>. 
#--------------------------------------------------------------------------------------
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QSlider, QMessageBox
from PyQt5 import uic
from random import Random
import math
import sys

#CONSTANTS: to help in iterations and in conditionals.
MAX_RGB_VALUE = 255
MIN_RGB_VALUE = 0
SLIDER_DEFAULT_VALUE = 49
PIXEL_CONTENTS = 4
R_G_B = 3
MAX_IMAGE_SIZE = 1500 #Larger images slow down the program considerably.
MIN_IMAGE_SIZE = 4

#Arbitrary value for comparing RGB values. Can be changed at will.
SIMILARITY_RANGE = 15

#Keeps the proportions of the confetti shape similar, independent of image dimensions.
CONFETTI_PROPORTION = 14899
        
class UI(QMainWindow):
    
    def __init__(self):
        """ Load everything onto the main window and display it.
        """
        super(UI, self).__init__()
        uic.loadUi("abstract_image_editor.ui", self)
        
        #initialize the global variables
        self.past_slider_value = 0
        self.rand_int = Random()
        #initialize the image label
        self.image_label = self.findChild(QLabel, "imageLabel")
        
        #initialize the buttons
        self.open_button = self.findChild(QPushButton, "openButton")
        self.reset_button = self.findChild(QPushButton, "resetButton")
        self.save_button = self.findChild(QPushButton, "saveButton")
        self.neon_button = self.findChild(QPushButton, "neonButton")
        self.ww_button = self.findChild(QPushButton, "wwButton")
        self.zeus_button = self.findChild(QPushButton, "zeusButton")
        self.mint_button = self.findChild(QPushButton, "mintButton")
        self.diamond_button = self.findChild(QPushButton, "diamondButton")
        self.strie_button = self.findChild(QPushButton, "strieButton")
        self.pattern_button = self.findChild(QPushButton, "patternButton")
        self.zombie_button = self.findChild(QPushButton, "zombieButton")
        self.sketch_button = self.findChild(QPushButton, "sketchButton")
        self.dust_button = self.findChild(QPushButton, "dustButton")
        self.neon_metal_button = self.findChild(QPushButton, "neonMetalButton")
        self.brighter_button = self.findChild(QPushButton, "brighterButton")
        #connect the buttons
        self.open_button.clicked.connect(self.clicked_open_button)
        self.reset_button.clicked.connect(self.clicked_reset_button)
        self.save_button.clicked.connect(self.clicked_save_button)
        self.neon_button.clicked.connect(self.clicked_neon_button)
        self.ww_button.clicked.connect(self.clicked_wild_west_button)
        self.zeus_button.clicked.connect(self.clicked_zeus_button)
        self.mint_button.clicked.connect(self.clicked_mint_button)
        self.diamond_button.clicked.connect(self.clicked_diamond_button)
        self.strie_button.clicked.connect(self.clicked_strie_button)
        self.pattern_button.clicked.connect(self.clicked_pattern_button)
        self.zombie_button.clicked.connect(self.clicked_zombie_button)
        self.sketch_button.clicked.connect(self.clicked_sketch_button)
        self.dust_button.clicked.connect(self.clicked_dust_button)
        self.neon_metal_button.clicked.connect(self.clicked_neon_metal_button)
        self.brighter_button.clicked.connect(self.clicked_brighter_button)
        
        #initialize the sliders
        self.melt_slider = self.findChild(QSlider, "meltSlider")
        self.wash_slider = self.findChild(QSlider, "washSlider")
        self.confetti_slider = self.findChild(QSlider, "confettiSlider")
        #connect the sliders 
        self.melt_slider.valueChanged.connect(self.moved_melt_slider)
        self.wash_slider.valueChanged.connect(self.moved_wash_slider)
        self.confetti_slider.valueChanged.connect(self.moved_confetti_slider)
        
        #display the main window
        self.show()
        
    def clicked_open_button(self):
        """ Called whenever the open image button is clicked.
            Opens up a load image dialog box and then if an image is selected
            it checks if the image size is within the allowed range.
            If the image meets the requirements, it is displayed.
        """
        self.reset_sliders()
        fileName = QFileDialog.getOpenFileName(self, "Open File",'',"JPEG (*.jpg *.jpeg);;PNG (*.png)")
        #if the fileName is not empty
        if fileName[0] != '':
            self.pixmap = QPixmap(fileName[0])
            
            self.backUpImage = self.pixmap.toImage()
            self.image_height = self.backUpImage.height()
            self.image_width = self.backUpImage.width()
            
            #if the image is too large
            if (self.image_height > MAX_IMAGE_SIZE) or (self.image_width > MAX_IMAGE_SIZE):
                message = f"Image can't be greater than {MAX_IMAGE_SIZE} by {MAX_IMAGE_SIZE} pixels!"
                self.display_warning_message_box(message, "Try Again.")
                return
            #if the image is too small
            if (self.image_height < MIN_IMAGE_SIZE) or (self.image_width < MIN_IMAGE_SIZE):
                message = f"Image can't be less than {MIN_IMAGE_SIZE} by {MIN_IMAGE_SIZE} pixels!"
                self.display_warning_message_box(message, "Try Again.")
                return
            
            #display image
            self.image_label.setPixmap(self.pixmap)
            
            #array is the list of RGB pointer values that represent the pixels of the image.
            self.array = []
            
    def display_warning_message_box(self, text, informative):
        """ Helper method to display a warning message box.
        """ 
        pop_up_msg = QMessageBox()
        pop_up_msg.setIcon(QMessageBox.Warning)
        pop_up_msg.setWindowTitle("Error")
        pop_up_msg.setText(text)
        pop_up_msg.setInformativeText(informative)
        pop_up_msg.setStandardButtons(QMessageBox.Ok)
        pop_up_msg.exec_()
                
    def clicked_zeus_button(self):
        """ Called whenever the zeus button is pressed.
            The pixels of the image are shuffled painting
            the image with various colors.
        """        
        if self.has_no_image(''):
            return
        
        qImage = self.get_QImage()
        
        #Arbitrary value that can be changed at will to create different effects.
        zeus_value = 100
        
        for position in range(0, len(self.array), PIXEL_CONTENTS):
            
            for iteration in range(R_G_B):
                    
                value = self.array[position] + zeus_value
                
                #The next integers in the if, elif, 
                #and else statements represent RGB values from 0 to 255.
                #The values can be changed at will as long as they are kept in the 0-255 range.
                if  value >= 0 and value <= 50:
                    self.array[position] = 70
                elif value >= 51 and value <= 100:
                    self.array[position] = 120
                elif value >= 101 and value <= 150:
                    self.array[position] = 170
                elif value >= 151 and value <= 200:
                    self.array[position] = 225
                else:
                    self.array[position] = 45

                #Arbitrary value that can be changed at will to create different effects.
                #May cause index out of bounds errors.
                position += 1 #go forward 1 rgb value
        
        self.pixmap = QPixmap.fromImage(qImage)
        self.image_label.setPixmap(self.pixmap)

        
    def clicked_brighter_button(self):
        """ Called whenever the brighter button is pressed.
            The pixel values are incremented by the arbitrary brighter value,
            increasing the brightness of the image.
        """   
        if self.has_no_image(''):
            return

        #Arbitrary value that can be changed at will to create different effects.     
        brighter_value = 5
        
        qImage = self.get_QImage()
        
        for position in range(0, len(self.array), PIXEL_CONTENTS):
            
            blue_green_red = [self.array[position], self.array[position + 1]  , self.array[position + 2]]
            
            for color in blue_green_red:
                if (color + brighter_value) > MAX_RGB_VALUE:
                        self.array[position] = color - brighter_value 
                else:
                    self.array[position] = color + brighter_value 

                #Arbitrary value that can be changed at will to create different effects.
                #May cause index out of bounds errors.
                position += 1 #go forward 1 rgb value
                     
        self.pixmap = QPixmap.fromImage(qImage)
        self.image_label.setPixmap(self.pixmap)
        
    def clicked_neon_button(self):
        """ Called whenever the neon button is pressed.
            The rgb values are shuffled, painting the image in 
            various neon colors.
        """    
        if self.has_no_image(''):
            return
        
        #Arbitrary values that can be changed at will to create different effects.
        neon_list = [-100, 70] 

        qImage = self.get_QImage()
        
        for value in neon_list:
        
            for position in range(1, len(self.array)-PIXEL_CONTENTS, PIXEL_CONTENTS):
                
                blue_green_red = [self.array[position], self.array[position + 1]  , self.array[position + 2]]
                
                for color in blue_green_red:
                    if (color + value) < MIN_RGB_VALUE:
                            self.array[position] = self.array[position + 1]
                    elif (color + value) > MAX_RGB_VALUE:
                            self.array[position] = self.array[position - 1]
                    else:
                        self.array[position] = color + value 

                    #Arbitrary value that can be changed at will to create different effects.
                    #May cause index out of bounds errors.    
                    position += 1 #go forward 1 grb value
                     
        self.pixmap = QPixmap.fromImage(qImage)
        self.image_label.setPixmap(self.pixmap)
    
    def clicked_wild_west_button(self):
        """ Called whenever the wild west button is pressed.
            Creates a contrast of colors on the image.
        """  
        if self.has_no_image(''):
            return

        #Arbitrary value that can be changed at will to create different effects.
        ww_value = 100

        qImage = self.get_QImage()
        
        for position in range(0, len(self.array)-PIXEL_CONTENTS, PIXEL_CONTENTS):
            
            blue_green_red = [self.array[position], self.array[position+2], self.array[position+1]]
            
            for color in blue_green_red:
                if (color + ww_value) < MIN_RGB_VALUE:
                        self.array[position] = MAX_RGB_VALUE + color + ww_value
                elif (color + ww_value) > MAX_RGB_VALUE:
                        self.array[position] = color + ww_value - MAX_RGB_VALUE 
                else:
                    self.array[position] = color + ww_value 

                #Arbitrary value that can be changed at will to create different effects.
                #May cause index out of bounds errors.
                position += 2 #go forward 2 rgb values
                    
        self.pixmap = QPixmap.fromImage(qImage)
        self.image_label.setPixmap(self.pixmap) 
    
    def clicked_mint_button(self):
        """ Called whenever the mint button is pressed.
            Creates a contrast of colors on the image.
        """        
        if self.has_no_image(''):
            return
        
        #Arbitrary value that can be changed at will to create different effects.
        mint_value = 1 
        
        qImage = self.get_QImage()
        
        for position in range(0, len(self.array), PIXEL_CONTENTS):
            
            for iteration in range(R_G_B):
                    
                value = self.array[position] + mint_value
                
                #The next integers in the if, elif,
                #and else statements represent RGB values from 0 to 255.
                #The values can be changed at will to create different effects
                #as long as they are kept in the 0-255 range.
                if  value >= 0 and value <= 50:
                    self.array[position] = 225
                elif value >= 51 and value <= 100:
                    self.array[position] = 170
                elif value >= 101 and value <= 150:
                    self.array[position] = 120
                elif value >= 151 and value <= 200:
                    self.array[position] = 70
                else:
                    self.array[position] = 30

                #Arbitrary value that can be changed at will to create different effects.
                #May cause index out of bounds errors.
                position += 1 #go forward 1 rgb value
        
        self.pixmap = QPixmap.fromImage(qImage)
        self.image_label.setPixmap(self.pixmap)
        
    def clicked_strie_button(self):
        """ Called whenever the strie button is pressed.
            The colors of the image are spread to the sides creating a strie effect. 
        """        
        if self.has_no_image(''):
            return
            
        self.brush_effects('strie', 'cross')
        
    def clicked_diamond_button(self):
        """ Called whenever the diamond button is pressed.
            The image colors are reduced to a few colors and creates a diamond pattern.
        """        
        if self.has_no_image(''):
            return
        
        self.brush_effects('diamond', 'cross')

    def clicked_sketch_button(self):
        """ Called whenever the sketch button is pressed.
            Most of the colors of the image are reduced to a few colors 
            turning the image similar to a sketch.
        """        
        if self.has_no_image(''):
            return
         
        qImage = self.get_QImage()
        
        for position in range(len(self.array) - PIXEL_CONTENTS):
    
            rgb = [self.array[position], self.array[position + 1], self.array[position + 2]]
            
            for color in rgb:
                
                #The next integers in the if, elif, 
                #and else statements represent RGB values from 0 to 255.
                #The values can be changed at will as long as they are kept in the 0-255 range.
                if color > 200:
                    self.array[position] = MIN_RGB_VALUE
                elif color < 50:
                    self.array[position] = MAX_RGB_VALUE

        self.pixmap = QPixmap.fromImage(qImage)
        self.image_label.setPixmap(self.pixmap)
        
    def clicked_dust_button(self):
        """ Called whenever the dust button is pressed.
            The colors of the image are spread, 
            and creates the effect of dust in the wind. 
        """        
        if self.has_no_image(''):
            return
        
        self.brush_effects('dust', 'diagonal')
        
    def clicked_neon_metal_button(self):
        """ Called whenever the neon metal button is pressed.
            The image is painted neon with random lines and gray flakes.
        """        
        if self.has_no_image(''):
            return
        
        self.brush_effects('metal', 'diagonal')
    
    def clicked_pattern_button(self):
        """ Called whenever the pattern button is pressed. 
            Wraps the RGB values around the range of 0-255.
            Creates a pattern on the image and reduces the amount of colors.
        """       
        if self.has_no_image(''):
            return
        
        #Arbitrary value that can be changed at will to create different effects.
        pattern_value = 100

        qImage = self.get_QImage()
        
        for position in range(0, len(self.array) - PIXEL_CONTENTS, PIXEL_CONTENTS):
            
            blue_green_red = [self.array[position - 3], self.array[position - 2]  , self.array[position - 1]]
            
            for color in blue_green_red:
                if (color + pattern_value) < MIN_RGB_VALUE:
                        self.array[position] = MAX_RGB_VALUE + color + pattern_value
                elif (color + pattern_value) > MAX_RGB_VALUE:
                        self.array[position] = color + pattern_value - MAX_RGB_VALUE 
                else:
                    self.array[position] = color + pattern_value 
                    

                #Arbitrary value that can be changed at will to create different effects.
                #May cause index out of bounds errors.
                position += 3 #go forward 3 rgb values
                     
        self.pixmap = QPixmap.fromImage(qImage)
        self.image_label.setPixmap(self.pixmap)
    
    def clicked_zombie_button(self):
        """ Called whenever the zombie button is pressed. 
            The colors of the image turn pale.
        """        
        if self.has_no_image(''):
            return

        self.brush_effects('zombie', 'cross')
        
    def brush_effects(self, effect, pattern):
        """ Called whenever a brush slider or button is interacted with. 
            The brush effects are: Wash, Zombie, Strié, Diamond, Dust, and Metal.
            For every pixel, some of it's encircling pixels are selected. 
            How the pixels are selected depends on the pattern string.
            If the surrounding pixels are withing a range of similarity, 
            either the current pixel or the encircling pixels are painted to a similar color.

        Args:
            effect (str): The name of the effect button pressed.    
            pattern (str): The pattern specifies how the encircling pixels
            of the current spot or pixel are selected.
        """        
        qImage = self.get_QImage()
        
        values_per_row = self.image_width * PIXEL_CONTENTS
        total_rows = self.image_height - 2
        row_start =  values_per_row + PIXEL_CONTENTS
        row_end = (values_per_row * 2) - PIXEL_CONTENTS
        perimeter = []
        
        for row in range(total_rows):
            for column in range(row_start, row_end, PIXEL_CONTENTS):
                #select encircling pixels
                #diagonal pattern
                if pattern == 'diagonal': 
                    perimeter.append(column + values_per_row - PIXEL_CONTENTS) #bottom left pixel
                    perimeter.append(column - values_per_row + PIXEL_CONTENTS) #top right pixel
                #cross pattern 
                else: 
                    perimeter.append(column - values_per_row) #top pixel
                    perimeter.append(column + PIXEL_CONTENTS) #side right pixel
                    perimeter.append(column + values_per_row) #bottom pixel
                    perimeter.append(column - PIXEL_CONTENTS) #side left pixel
                    
                current_red = self.array[column + 2]
                current_green = self.array[column + 1]
                current_blue = self.array[column]
                
                for perimeter_pixel in perimeter:
                    
                    red_diff = self.array[perimeter_pixel + 2] - current_red
                    gre_diff = self.array[perimeter_pixel + 1] - current_green
                    blu_diff = self.array[perimeter_pixel] - current_blue
                    
                    if red_diff <= SIMILARITY_RANGE and red_diff >= (SIMILARITY_RANGE * -1):
                        if gre_diff <= SIMILARITY_RANGE and gre_diff >= (SIMILARITY_RANGE * -1):
                            if blu_diff <= SIMILARITY_RANGE and blu_diff >= (SIMILARITY_RANGE * -1):
                        
                                if effect == 'wash' or effect == 'zombie':
                                    self.array[column] = self.array[perimeter_pixel]
                                    self.array[column+1] = self.array[perimeter_pixel + 1]
                                    self.array[column+2] = self.array[perimeter_pixel + 2]
                                    
                                    if effect == 'zombie':
                                    #Arbitrary position value that can be changed at will 
                                    #to create different effects.
                                    #May cause index out of bounds errors.
                                    #This applies to all of the position variables in this method.
                                        column += 1 #go forward 1 rgb value 
                                        
                                elif effect == 'strie' or effect == 'diamond':
                                    self.array[perimeter_pixel] = self.array[column]
                                    self.array[perimeter_pixel + 1] = self.array[column + 1]
                                    self.array[perimeter_pixel + 2] = self.array[column + 2]
                                    
                                    if effect == 'strie':
                                        column += 8 #go forward 2 pixels
                                    elif effect == 'diamond':
                                        column += 1 #go forward 1 rgb value 
                                    
                                elif effect == 'dust':
                                    self.array[column] = self.array[perimeter_pixel]
                                    self.array[column + 1] = self.array[perimeter_pixel + 1]
                                    self.array[column + 2] = self.array[perimeter_pixel + 2]
                                    column += 4 #go forward 1 pixel 
                                    
                                    self.array[perimeter_pixel] = self.array[column]
                                    self.array[perimeter_pixel + 1] = self.array[column + 1]
                                    self.array[perimeter_pixel + 2] = self.array[column + 2]
                                    column += -20 #go back 5 pixels
                                    
                                    self.array[perimeter_pixel] = self.array[column]
                                    self.array[perimeter_pixel + 1] = self.array[column + 1]
                                    self.array[perimeter_pixel + 2] = self.array[column + 2]
                                    column += 8 #go forward 2 pixels
                                    
                                elif effect == 'metal':
                                    self.array[column] = self.array[perimeter_pixel+1]
                                    self.array[column + 1] = self.array[perimeter_pixel + 2]
                                    self.array[column + 2] = self.array[perimeter_pixel]
                                    column += -5 #go back 5 rgb values 
                                        
                perimeter.clear()
            
            #move row_start and row_end to the next row  
            row_start += values_per_row
            row_end += values_per_row
        
        self.pixmap = QPixmap.fromImage(qImage)
        self.image_label.setPixmap(self.pixmap)
        
    def moved_melt_slider(self, melt_value):
        """ Called whenever the melt slider is moved.
            The pixels of the image form squares and either blend towards 
            the top or the bottom depending on the slider's direction
            creating the effect of a melting image.
            
        Args:
            melt_value (int): The melt effect slider's position.
        """        
        if self.has_no_image('melt'):
            return
        
        qImage = self.get_QImage() 
        direction = self.get_slider_direction(melt_value)
        rows_to_melt = self.get_slider_difference(melt_value)
        rgb_values_per_row = self.image_width * PIXEL_CONTENTS
        
        if direction > 0: #slide up
            pixel_position = (rows_to_melt * rgb_values_per_row) - 1
        else: #slide down
            pixel_position = (len(self.array) - (rows_to_melt * rgb_values_per_row)) - 1
            
        column = 0
        done = False
        
        while not done: 
            row_number = rgb_values_per_row
            #travel up or down the current column for all of the n rows_to_melt
            for pixel in range(rows_to_melt): 
                if direction > 0: #slide up
                    #paint the current pixel equal to the pixel that is row_number rows below
                    self.array[pixel_position - row_number] = self.array[pixel_position]
                    self.array[(pixel_position - 1) - row_number] = self.array[pixel_position - 1]
                    self.array[(pixel_position - 2) - row_number] = self.array[pixel_position - 2]
                    self.array[(pixel_position - 3) - row_number] = self.array[pixel_position - 3]
                else: #slide down
                    #paint the current pixel equal to the pixel that is row_number rows above
                    self.array[pixel_position + row_number] = self.array[pixel_position]
                    self.array[(pixel_position - 1) + row_number] = self.array[pixel_position - 1]
                    self.array[(pixel_position - 2) + row_number] = self.array[pixel_position - 2]
                    self.array[(pixel_position - 3) + row_number] = self.array[pixel_position - 3]
        
                #move on to the next row
                row_number += rgb_values_per_row
            
            #move on to the next column
            column += PIXEL_CONTENTS

            #check if the current row is finished
            if column == rgb_values_per_row:
                column = 0
                #skip n rows_to_melt 
                if direction > 0:#slide up
                    pixel_position += (rows_to_melt * rgb_values_per_row)
                else:#slide down
                    pixel_position -= (rows_to_melt * rgb_values_per_row)
            else:
                #move on to the next pixel
                if direction > 0:#slide up
                    pixel_position += PIXEL_CONTENTS 
                else:#slide down
                    pixel_position -= PIXEL_CONTENTS
                    
            if pixel_position < 0 or pixel_position > len(self.array):
                done = True
                    
        self.pixmap = QPixmap.fromImage(qImage)
        self.image_label.setPixmap(self.pixmap)
        
    def moved_wash_slider(self, wash_value):
        """ Called whenever the wash slider is moved. 
            For every pixel, some of it's surrounding pixels are checked. 
            Which pixels are checked depends on the direction of the slider.
            If the surrounding pixels are withing a range of similarity, 
            the pixels are painted to a similar color creating a brush stroke effect.

        Args:
            wash_value (int): The wash effect slider's position.
        """        
        if self.has_no_image('wash'):
            return
        
        direction = self.get_slider_direction(wash_value)
        
        if direction > 0:
            direction = "diagonal"
        else:
            direction = "cross"
        
        self.brush_effects('wash', direction)
        
    def moved_confetti_slider(self, confetti_value):
        """ Called whenever the confetti slider is moved.
            This method blends random areas of the image creating a confetti effect.

        Args:
            confetti_value (int): The confetti effect slider's position.
        """        
        if self.has_no_image('confetti'):
            return
        
        confetti_quantity = self.get_slider_difference(confetti_value)
        qImage = self.get_QImage()
        total_pixels = self.image_height * self.image_width
        confetti_side = int(math.sqrt(total_pixels / CONFETTI_PROPORTION))
        
        #ensure a minimum length for the side of a confetti shape
        if confetti_side == 0:
            confetti_side = 1
        
        rgb_values_per_row = self.image_width * PIXEL_CONTENTS
        left_side_margin = confetti_side * PIXEL_CONTENTS
        right_side_margin = rgb_values_per_row - left_side_margin
        rows_to_skip = rgb_values_per_row * confetti_side
        range_start =  rows_to_skip + left_side_margin
        range_end = len(self.array) - rows_to_skip - left_side_margin
        perimeter_pixels = []
        
        for confetti in range(confetti_quantity):
            found = False
            random_pixel = 0
            
            while(not found):
                #choose a random R value from the RGB values of a pixel on the image
                random_pixel = self.rand_int.randrange(range_start, range_end, PIXEL_CONTENTS)
                #find the position of the chosen pixel on the row 
                pixel_position = ((random_pixel / rgb_values_per_row) % 1) * rgb_values_per_row
                #check if the random pixel is within the allowed range
                if pixel_position >= left_side_margin and pixel_position < right_side_margin:
                    found = True
            
            #move from the random center pixel to the top left corner pixel of the confetti shape     
            start_pixel = random_pixel - left_side_margin
            start_pixel = start_pixel - rows_to_skip  
            #select the pixels that form a square confetti shape starting from the top left corner
            for row in range(confetti_side):
                current_pixel = start_pixel
                for pixel in range(confetti_side):
                    perimeter_pixels.append(current_pixel)
                    current_pixel += PIXEL_CONTENTS
                start_pixel += rgb_values_per_row
            
            #process the selected pixels
            for perimeter_pixel_position in perimeter_pixels:
                #paint the encircling pixels equal to the color of the center random pixel
                self.array[perimeter_pixel_position] = self.array[random_pixel]
                self.array[perimeter_pixel_position + 1] = self.array[random_pixel + 1]
                self.array[perimeter_pixel_position + 2] = self.array[random_pixel + 2]
            #clean the array for the next confetti shape            
            perimeter_pixels.clear()
        
        self.pixmap = QPixmap.fromImage(qImage)
        self.image_label.setPixmap(self.pixmap)  
        
    def clicked_reset_button(self):
        """ Resets the image and the sliders' positions
            whenever the reset button is pressed.
        """    
        if self.has_no_image(''):
            return

        self.reset_sliders()
        
        self.pixmap = QPixmap.fromImage(self.backUpImage)
        self.image_label.setPixmap(self.pixmap)
        
    def clicked_save_button(self):
        """ Saves the image whenever the save button is pressed.
            Opens up a save image dialog box.
            
        Returns: 
            None (None): If the file path cannot be resolved or 
            there is no image on the UI screen to save.
        """
        filePath = QFileDialog.getSaveFileName(self, "Save Image", "",
                         "JPEG (*.jpg *.jpeg);;PNG (*.png);;All Files (*.*) ")
        
        if filePath[0] == "" or self.has_no_image('save'):
            return
        else:
            self.pixmap.save(filePath[0])

    def get_slider_direction(self, new_slider_value):
        """ Helper method to get the slider's direction (positive or negative) 
            and distance of movement.

        Args:
            new_slider_value (int): The current slider's position. 

        Returns:
            new_slider_value (int): 
                The total distance that the slider moved from it's last position. 
                If the slider moved in the positive direction, a positive integer is returned.
                Otherwise a negative integer is returned.
        """        
        buffer_value = new_slider_value
        new_slider_value = new_slider_value - self.past_slider_value 
        self.past_slider_value = buffer_value
        
        return new_slider_value        
      
    def get_slider_difference(self, new_slider_value):
        """ Helper method to get the slider's absolute distance of movement
            from the SLIDER_DEFAULT_VALUE reference point.

        Args:
            new_slider_value (int): The current slider's position.

        Returns:
            new_slider_value (int): 
                The total absolute distance that the slider moved from the SLIDER_DEFAULT_VALUE. 
        """        
        if new_slider_value < SLIDER_DEFAULT_VALUE:
            new_slider_value = SLIDER_DEFAULT_VALUE - new_slider_value
        else:
            new_slider_value = new_slider_value - SLIDER_DEFAULT_VALUE
            
        return new_slider_value
            
    def has_no_image(self, type):
        """ Helper method that makes sure that there is an open image on the UI screen label
            before any operation on the image is performed.
        """
        if self.image_label.pixmap() == None:
            
            if type == 'save':
                message = "There is no image to save!"
                self.display_warning_message_box(message, "Open an image first.")

            self.reset_sliders()
                  
            return True
        else:
            return False
        
    def reset_sliders(self):
        """ Helper method to reset the sliders.
        """
        self.melt_slider.setValue(SLIDER_DEFAULT_VALUE)
        self.wash_slider.setValue(SLIDER_DEFAULT_VALUE)
        self.confetti_slider.setValue(SLIDER_DEFAULT_VALUE)
            
    def get_QImage(self):
        """ Helper method to initialize the array that points to the image's pixels,
            and to return it's QImage from the UI screen.
        
        Returns:
            qImage (QImage): Object of the current image on the UI screen.
        """
        qImage = self.pixmap.toImage()
        pointer = qImage.bits()
        pointer.setsize(qImage.byteCount())
        self.array = pointer.asarray()
        return qImage
            
if __name__ == '__main__':            
    """ Top Level.
        Runs the QApplication object.
    """
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()
