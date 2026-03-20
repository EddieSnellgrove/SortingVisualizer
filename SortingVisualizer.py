import tkinter as tk
from FunctionGrapher import GraphMaker


# This class is responsible for creating the UI for the sorting visualizer, including the sliders and buttons for each algorithum, and handling the button click events to create the graphs using GraphMaker
class SortingVisualizer:
    #Initializes the UI and sets up the algorithums, sliders, and buttons
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sorting Algorithm Visualizer")
        self.algorithms= ["Bubble Sort", "Bubble SortEff", "Insertion Sort"] #TODO add more algorithums:"Selection Sort", "Merge Sort", "Quick Sort", "Heap Sort", "Radix Sort", "Counting Sort", "Bucket Sort", "Shell Sort"
        self.slidersNBars = []
        self.slidersDur = []
        self.slidersNComps = []
    #Handles the button click event, retrieves the values from the sliders, and calls GraphMaker to create the graph
    def on_button_click(self, i, isGif):
        gChoice = self.algorithms[i]
        numBars = self.slidersNBars[i].get() 
        numComPerFrame = self.slidersNComps[i].get()
        volume = self.sliderVol.get()
        dur = self.slidersDur[i].get()
        graphMaker = GraphMaker()
        graphMaker.createGraph(gChoice, numBars, numComPerFrame, dur, volume, isGif)

    #Sets up the UI for the program, including the sliders and buttons for each algorithum
    def setupUI(self):
        self.sliderVol = tk.Scale(self.root, from_=1, to=100, orient=tk.HORIZONTAL, label="Volume:", length=200)
        self.sliderVol.grid(row=0, column=7, padx=5, pady=5)

        for i in range(len(self.algorithms)):
            T = tk.Text(self.root, height=5, width=100)
            T.grid(row=i, column=1)
            T.insert(tk.END, f"{self.algorithms[i]} example:")
            match self.algorithms[i]:
                case "Bubble Sort":
                    T.insert(tk.END, '\n\nBubble Sort is a simple sorting algorithm that repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order. ' \
                    'The pass through the list is repeated until the list is sorted. ')
                case "Bubble SortEff":  
                    T.insert(tk.END, '\n\nBubble SortEff is an differentversion of Bubble Sort that reduces the number of comparisons by \ntaking advantage of the fact that after each pass, the largest element "bubbles" to its ' \
                    'correct \nposition. It is hampered here by not accountingfor more being sorted after each pass.')
                case "Insertion Sort":
                    T.insert(tk.END, '\n\nInsertion Sort is a simple sorting algorithm that builds the final sorted array one item at a time. It works by taking elements from the unsorted portion of the list and ' \
                    'inserting them into their\ncorrect position in the sorted portion of the list.')

            slider = tk.Scale(self.root, from_=10, to=250, orient=tk.HORIZONTAL, label="Number of bars to be sorted:", length=200)
            slider.grid(row=i, column=4, padx=5, pady=5)
            self.slidersNBars.append(slider)

            slider = tk.Scale(self.root, from_=10, to=25, orient=tk.HORIZONTAL, label="Duration (ms) of each frame:", length=200)
            slider.grid(row=i, column=5, padx=5, pady=5)
            self.slidersDur.append(slider)

            slider = tk.Scale(self.root, from_=1, to=300, orient=tk.HORIZONTAL, label="Number of operations per frame:", length=200)
            slider.grid(row=i, column=6, padx=5, pady=5)
            self.slidersNComps.append(slider)


            button = tk.Button(self.root, text=f"{self.algorithms[i]}", command=lambda i=i: self.on_button_click(i, isGif = False))
            button.grid(row=i, column=2, padx=5, pady=5)
            button = tk.Button(self.root, text=f"Generate {self.algorithms[i]} gif", command=lambda i=i: self.on_button_click(i, isGif = True))
            button.grid(row=i, column=3, padx=5, pady=5)

        self.root.mainloop()

