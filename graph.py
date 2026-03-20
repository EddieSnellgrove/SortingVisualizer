import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np
import math
import pygame

# Parent class for all sort types, sets up graph and frame generator for animation
class Graph:
    # Initate graph using Graphs setup and establish non sort spicific varables.
    def __init__(self, numBars, volume):
        # Set up graph with numGraphs subplots for avg case, best case, semi sorted case, and worst case, ex and set up text for number of totalSwaps, operations, bigO notation, and predicted operations
        self.numBars = numBars
        self.volume = volume
        self.fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        self.axes = axes.flatten() 
        self.x = np.arange(self.numBars)

        #Initate pygame mixer for sound effects, set volume
        pygame.mixer.init(frequency=44100, size=-16, channels=1)
        self.duration = 0.05  

        # Create 4 separate datasets and 4 bar lists
        self.allBars = []
        self.swapText = []
        self.operationsText = [] 
        self.bigOText = []
        self.perdictionText = []
        self.allSwaps = [0] * 4
        self.allOps = [0] * 4
        self.allPos = [0] * 4
        self.allIsSorted = [False] * 4
        self.allPostSorted = [False] * 4
        self.allTotalSwaps = [0] * 4
        self.numGraphs = 4
        heights = [np.random.rand(self.numBars), np.linspace(0.1, 1, self.numBars), np.linspace(0.1, 0.8, self.numBars) + np.random.rand(self.numBars) * 0.2, np.linspace(1, 0.1, self.numBars)]

        for i in range(self.numGraphs):
            bars = self.axes[i].bar(self.x, heights[i], width=1, align='edge', color=f'C{i}')
            self.swapText.append(self.axes[i].text(0.02, 0.95, '', transform=self.axes[i].transAxes))
            self.operationsText.append(self.axes[i].text(0.02, 0.90, '', transform=self.axes[i].transAxes))
            self.bigOText.append(self.axes[i].text(0.02, 0.85, '', transform=self.axes[i].transAxes))
            self.perdictionText.append(self.axes[i].text(0.02, 0.80, '', transform=self.axes[i].transAxes))
            self.allBars.append(list(bars))
            self.axes[i].set_ylim(0, 1.1)

        self.axes[0].set_title(f"Avg Case")
        self.axes[1].set_title(f"Best Case")
        self.axes[2].set_title(f"Semi Sorted Case")
        self.axes[3].set_title(f"Worst Case")

    # Frame generator for animation, yields True until the graph is sorted, then stops yielding to end the animation
    def generator(self):
        while not all(self.allPostSorted):
            yield True

    # Check if we are at the end of the list
    def isEnd(self, i):
        if self.allPos[i] == len(self.allBars[i]) - 2:
            return True
        return False
    
    # Check if we are at the beginning of the list
    def atStart(self, i):
        if self.allPos[i] == 0:
            return True
        return False
    
    # Swap the positions of two bars on the graph and in the list of bars
    def swapPosition(self, pos1, pos2, i):
        self.allBars[i][pos1].set_x(pos2)
        self.allBars[i][pos2].set_x(pos1) 
        self.allBars[i][pos1], self.allBars[i][pos2] = self.allBars[i][pos2], self.allBars[i][pos1]

    # Check if the height of the bar at pos1 is greater than the height of the bar at pos2
    def isGreater(self, pos1, pos2, i):
        if self.allBars[i][pos1].get_height() > self.allBars[i][pos2].get_height():
            return True
        return False
    
    # Update the text for number of totalSwaps and operations
    def updateText(self, i):
        self.swapText[i].set_text(f'Total swaps: {self.allTotalSwaps[i]}')
        self.operationsText[i].set_text(f'Operations: {self.allOps[i]}')

    # Play a sound based on the height of the bar being compared, with the frequency of the sound increasing as the height of the bar increases
    def playSound(self, i, pos1):
        freq = 200 + self.allBars[i][pos1].get_height() * 800
        sample_rate = 44100
        n_samples = int(sample_rate * self.duration)
        t = np.linspace(0, self.duration, n_samples, False)
        tone = np.sin(freq * t * 2 * np.pi)
                
        audio = (tone * 32767).astype(np.int16)
        audio_stereo = np.repeat(audio.reshape(-1, 1), 2, axis=1)

        sound = pygame.sndarray.make_sound(audio_stereo)
        sound.set_volume(self.volume * 0.0005)
        sound.play()

# Bubble sort graph that inherits from MyGraph and animates the bubble sort algorithm, counting the number of totalSwaps and operations and displaying them on the graph
class BubbleSort(Graph):
    # Set up sorting spicific variables and set title for graph
    def __init__(self, numBars, volume):
        super().__init__(numBars, volume)
        self.fig.suptitle("Bubble Sort Comparison", fontsize=16)

    # Updates Colors handling for current frame, Colors bars red if they are being compared, and blue if they are not being compared
    def updateColors(self, i):
        if not self.allIsSorted[i]:
            for j in range(len(self.allBars[i])):
                self.allBars[i][j].set_color('C0')

            self.allBars[i][self.allPos[i]].set_color('red')
            self.allBars[i][self.allPos[i]+1].set_color('red')
    # Updates text for number of totalSwaps, operations, and bigO notation and predicted operations based on the current case we are in
    def updateText(self, i):
        super().updateText(i)
        if i == 0:
            self.bigOText[i].set_text(f'Bubble Sort Avg Case: O(n^2)')
            self.perdictionText[i].set_text(f'Predicted operations: {self.numBars**2} Current operations: {self.allOps[i]}')
        elif i == 1:
                self.bigOText[i].set_text(f'Bubble Sort Best Case: O(n)')
                self.perdictionText[i].set_text(f'Predicted operations: {self.numBars} Current operations: {self.allOps[i]}')
        elif i == 2:
            self.bigOText[i].set_text(f'Bubble Sort Semi-Sorted Case: O(kn)')
            self.perdictionText[i].set_text(f'Predicted operations: k x {self.numBars}, k = {math.ceil(self.allOps[i] / self.numBars)} Current operations: {self.allOps[i]}')
        elif i == 3:
            self.bigOText[i].set_text(f'Bubble Sort Worst Case: O(n^2)')
            self.perdictionText[i].set_text(f'Predicted operations: {self.numBars**2} Current operations: {self.allOps[i]}')

    # Updates colors turning all bars green after sorting is complete
    def updateColorsGreen(self, i):
        if self.atStart(i):
            for j in range(len(self.allBars[i])):
                self.allBars[i][j].set_color('C0') 
        self.allBars[i][self.allPos[i]].set_color('green')
        self.allBars[i][self.allPos[i]+1].set_color('green')
        if not self.isEnd(i):
            self.allPos[i] += 1
        if self.isEnd(i):
            self.allBars[i][self.allPos[i]+1].set_color('green')


    # Update function for animation, compares adjacent bars and swaps them if they are out of order, also updates text for number of totalSwaps and operations, and Colors bars red if they are being compared
    def update(self, frame, numComPerFrame):  
        for i in range(self.numGraphs):
            if not self.allIsSorted[i]:      
                for _ in range(int(self.numBars // 1.2) if self.numBars < numComPerFrame else numComPerFrame):
                    # Iterate number of operations if we are not sorted yet
                    self.allOps[i] += 1

                    # Swap bars if out of order, iterate number of totalSwaps
                    if self.isGreater(self.allPos[i], self.allPos[i]+1, i):
                        self.allTotalSwaps[i] += 1
                        self.allSwaps[i] += 1

                        self.swapPosition(self.allPos[i], self.allPos[i]+1, i)
                        self.playSound(i, self.allPos[i])

                    # End the sorting if we have gone through the entire list and made no totalSwaps, otherwise reset swaps for next pass through the list
                    if self.isEnd(i) and self.allSwaps[i] == 0:
                        self.allIsSorted[i] = True
                        self.allPos[i] = 0
                        break
                    elif self.isEnd(i):
                        self.allSwaps[i] = 0

                    # Loop back to beginning of list after reaching end
                    self.allPos[i] += 1
                    if self.allPos[i] == len(self.allBars[i]) - 1:
                        self.allPos[i] = 0            
            else:
                # After sorting, loop through the list and update colors to green for sorted bars
                for _ in range((self.numBars // 10) + 1 if self.numBars < numComPerFrame else (numComPerFrame // 10) + 1):
                    self.updateColorsGreen(i)
                    self.playSound(i, self.allPos[i])


            # Ends the animation if we have reached the end of the list and have sorted the entire list
            if self.isEnd(i) and self.allIsSorted[i]:
                self.allPostSorted[i] = True

            self.updateColors(i)
            self.updateText(i)
        # Compress all bars and text into a single list to return for animation
        finalBars = [bar for sublist in self.allBars for bar in sublist]
        return finalBars + self.swapText + self.operationsText + self.bigOText + self.perdictionText


#Bubble sort with efficiency update graph that inherits from BubbleSort and animates the bubble sort algorithm, counting the number of totalSwaps and operations and displaying them on the graph
class BubbleSortEff(BubbleSort):
    #Set up sorting spicific variables, sorted is the number of bars that are in their final position at the end of the list
    def __init__(self, numBars, volume):
        super().__init__(numBars, volume)
        self.allSorted = [0] * 4
        self.fig.suptitle('Bubble Sort with Efficiency "Upgrade" Comparison', fontsize=16)

    #Check if we are at the end of the unsorted portion of the list
    def isEnd(self, i):
        if self.allPos[i] == (len(self.allBars[i]) - self.allSorted[i] - 1):
            return True
        return False
    
    # Updates text for number of totalSwaps, operations, and bigO notation and predicted operations based on the current case we are in
    def updateText(self, i):
        super().updateText(i)
        if i == 0:
            self.bigOText[i].set_text(f'Bubble SortEff Avg Case: O((n^2)/2)')
            self.perdictionText[i].set_text(f'Predicted operations: {(self.numBars**2)//2} Current operations: {self.allOps[i]}')
        elif i == 1:
                self.bigOText[i].set_text(f'Bubble SortEff Best Case: O((n^2)/2)')
                self.perdictionText[i].set_text(f'Predicted operations: {(self.numBars**2)//2} Current operations: {self.allOps[i]}')
        elif i == 2:
            self.bigOText[i].set_text(f'Bubble SortEff Semi-Sorted Case: O((n^2)/2)')
            self.perdictionText[i].set_text(f'Predicted operations: {(self.numBars**2)//2} Current operations: {self.allOps[i]}')
        elif i == 3:
            self.bigOText[i].set_text(f'Bubble SortEff Worst Case: O((n^2)/2)')
            self.perdictionText[i].set_text(f'Predicted operations: {(self.numBars**2)//2} Current operations: {self.allOps[i]}')

    #Set colors for green sort and handle end of list when we have reached the end of the unsorted portion of the list
    def atEnd(self, i):
        self.allBars[i][self.allPos[i]].set_color('green')
        self.allBars[i][self.allPos[i]-1].set_color('green')
        self.allSwaps[i] = 0
        self.allSorted[i] += 1
        self.allPos[i] = 0

    #Handle end of animation when we have sorted the entire list
    def endAnimation(self, i):
        self.allPostSorted[i] = True

    #Clean up Colors from previous frame and set Colors for current frame
    def updateColors(self, i):
        for j in range(len(self.allBars[i]) - self.allSorted[i]):
            self.allBars[i][j].set_color('C0')
        self.allBars[i][self.allPos[i]].set_color('red')
        self.allBars[i][self.allPos[i]+1].set_color('red')

    #Update function for animation, compares adjacent bars and swaps them if they are out of order, also updates text for number of totalSwaps and operations, and Colors bars red if they are being compared
    def update(self, frame, numComPerFrame):
        for i in range(self.numGraphs):
            for _ in range(int(self.numBars // 1.2) if self.numBars < numComPerFrame else numComPerFrame):
                #Iterate number of operations
                self.allOps[i] += 1

                #Swap bars if out of order, iterate swaps
                if self.isGreater(self.allPos[i], self.allPos[i]+1, i):
                    self.allTotalSwaps[i] += 1
                    self.allSwaps[i] += 1
                    self.swapPosition(self.allPos[i], self.allPos[i]+1, i)
                    self.playSound(i, self.allPos[i])

                
                #End the animation if we have gone through the entire list and made no totalSwaps, otherwise reset swaps for next pass through the list
                self.allPos[i] += 1
                if self.allSorted[i] == len(self.allBars[i]) - 1:
                    self.endAnimation(i)
                    self.atEnd(i)
                    break
                elif self.isEnd(i):
                    self.atEnd(i)
            # Update colors and text for current frame      
            if not self.allPostSorted[i]:
                self.updateColors(i)
            self.updateText(i)
        # Compress all bars and text into a single list to return for animation
        finalBars = [bar for sublist in self.allBars for bar in sublist]
        return finalBars + self.swapText + self.operationsText + self.bigOText + self.perdictionText

    
class InsertionSort(Graph):
    #Set up sorting spicific variables, posTracker tracks the position of the current bar we are trying to insert into the sorted portion of the list
    def __init__(self, numBars, volume):
        super().__init__(numBars, volume)
        self.allPosTracker = [0] * 4

    #Updates Colors handling for current frame, Colors bars red if they are being compared, green if they are in their final position, blue if they are not being compared, and pink if they are the current position
    def updateColors(self, i):
        if not self.allIsSorted[i]:
            for j in range(len(self.allBars[i])):
                self.allBars[i][j].set_color('C0')

            if not self.atStart(i):
                self.allBars[i][self.allPos[i]-1].set_color('red')

            self.allBars[i][self.allPos[i]].set_color('red')
            self.allBars[i][self.allPosTracker[i]].set_color('Yellow')

    # Updates text for number of totalSwaps, operations, and bigO notation and predicted operations based on the current case we are in        
    def updateText(self, i):
        super().updateText(i)
        if i == 0:
            self.bigOText[i].set_text(f'Insertion Sort Avg Case: O((n^2)/4)')
            self.perdictionText[i].set_text(f'Predicted operations: {(self.numBars**2)//4} Current operations: {self.allOps[i]}')
        elif i == 1:
                self.bigOText[i].set_text(f'Insertion Sort Best Case: O(n)')
                self.perdictionText[i].set_text(f'Predicted operations: {self.numBars} Current operations: {self.allOps[i]}')
        elif i == 2:
            self.bigOText[i].set_text(f'Insertion Sort Semi-Sorted Case: O(kn)')
            self.perdictionText[i].set_text(f'Predicted operations: k x {self.numBars}, k = {math.ceil(self.allOps[i] / self.numBars)} Current operations: {self.allOps[i]}')
        elif i == 3:
            self.bigOText[i].set_text(f'Insertion Sort Worst Case: O((n^2)/2)')
            self.perdictionText[i].set_text(f'Predicted operations: {(self.numBars**2)//2} Current operations: {self.allOps[i]}')

    # Updates colors for green sorted bars after sorting is complete, and handles end of animation when we have reached the end of the list and have sorted the entire list
    def updateColorsGreen(self, i):    
        if self.atStart(i):
            for j in range(len(self.allBars[i])):
                self.allBars[i][j].set_color('C0') 

        self.allBars[i][self.allPos[i]].set_color('green')
        self.allBars[i][self.allPos[i] + 1].set_color('green')

        self.allPos[i] += 1
        if self.isEnd(i):
            self.allBars[i][-1].set_color('green')
            
    #Update function for animation, compares adjacent bars and swaps them if they are out of order, then goes back to check if in correct order
    def update(self, frame, numComPerFrame):
        for i in range(self.numGraphs):
            for _ in range(int(self.numBars // 1.2) if self.numBars < numComPerFrame else numComPerFrame):

                #Iterate number of operations if we are not sorted yet
                if not self.allIsSorted[i]:
                    self.allOps[i] += 1

                #Swap bars if out of order, iterate number of totalSwaps, and move back to check if we are in the correct position in the sorted portion of the list
                if self.allPos[i] > 0 and self.isGreater(self.allPos[i]-1, self.allPos[i], i) and not self.allIsSorted[i]:
                    self.allTotalSwaps[i] += 1
                    self.swapPosition(self.allPos[i]-1, self.allPos[i], i)
                    self.allPos[i] -= 1
                    self.playSound(i, self.allPos[i])
                else:
                    if self.allPosTracker[i] < len(self.allBars[i]) - 1:
                        self.allPosTracker[i] += 1
                        self.allPos[i] = self.allPosTracker[i]
                    elif not self.allIsSorted[i]:
                        self.allIsSorted[i] = True
                        self.allPos[i] = 0

            if self.allIsSorted[i]:
                for _ in range((self.numBars // 10) + 1 if self.numBars < numComPerFrame else (numComPerFrame // 10) + 1):
                    #Check if we are at the end of the list and have sorted the entire list, if so end the animation
                    if self.isEnd(i):
                        self.allPostSorted[i] = True
                        break
                    self.updateColorsGreen(i)
                    self.playSound(i, self.allPos[i])


            self.updateText(i)
            self.updateColors(i)
        # Compress all bars and text into a single list to return for animation
        finalBars = [bar for sublist in self.allBars for bar in sublist]
        return finalBars + self.swapText + self.operationsText + self.bigOText + self.perdictionText

    