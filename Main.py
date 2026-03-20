
""" 
 This program is a sorting algorithm visualizer that uses the tkinter library for the user interface and the matplotlib library for graphing. 
 The user can select from three different sorting algorithms (Bubble Sort, Bubble SortEff, and Insertion Sort) and adjust the number of bars to be sorted, the duration of each frame, 
 and the number of operations per frame using sliders. The user can also choose to generate a gif of the sorting process. SortingVisualizer sets up the UI and handles the user interactions, 
 GraphMaker is responsible for creating the graphs and animations for each sorting algorithm, and Graph contains the implementation of the sorting algorithms and the graphing logic. 
 The program is designed to be easily extendable to include more sorting algorithms in the future, simply add a case in SortingVisualiser and GraphMaker.
 Author: Edgar Scott Snellgrove Jr.
 """
from SortingVisualizer import SortingVisualizer

def main():        
    visualizer = SortingVisualizer()
    visualizer.setupUI()

if __name__ == "__main__":    main()