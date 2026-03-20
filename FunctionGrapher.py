from graph import Graph,BubbleSort,BubbleSortEff, InsertionSort
import matplotlib.animation as animation
import matplotlib.pyplot as plt
# This class is responsible for creating the UI for the sorting visualizer, including the sliders and buttons for each algorithum, and handling the button click events to create the graphs using GraphMaker
class GraphMaker():
    def __init__(self):
        return
    # This function takes in the user's choices for the graph and creates the appropriate graph and animation using the Graph class and its subclasses for each sorting algorithm. 
    # It also handles saving the animation as a gif if the user chooses to do so.
    def createGraph(self, gChoice,numBars=250,numComPerFrame=30, dur=10, volume=0, isGif = False):
        match gChoice:
            case "Bubble Sort": 
                graph = BubbleSort(numBars, volume)
                anim = animation.FuncAnimation(fig=graph.fig, func=graph.update, frames=graph.generator(), interval=dur, blit=True, repeat=False, fargs=(numComPerFrame,), cache_frame_data=False)
                plt.tight_layout()
                if isGif:
                    writer = animation.PillowWriter(fps=30)
                    anim.save(f"{gChoice}Animation.gif", writer=writer)
                    plt.close()
                else:    
                    plt.show()
            case "Bubble SortEff":  
                graph = BubbleSortEff(numBars, volume)
                anim = animation.FuncAnimation(fig=graph.fig, func=graph.update, frames=graph.generator(), interval=dur, blit=True, repeat=False, fargs=(numComPerFrame,), cache_frame_data=False)
                plt.tight_layout()
                if isGif:
                    writer = animation.PillowWriter(fps=30)
                    anim.save(f"{gChoice}Animation.gif", writer=writer) 
                    plt.close()
                else:
                    plt.show()            
            case "Insertion Sort":
                graph = InsertionSort(numBars, volume)
                anim = animation.FuncAnimation(fig=graph.fig, func=graph.update, frames=graph.generator(), interval=dur, blit=True, repeat=False, fargs=(numComPerFrame,), cache_frame_data=False)
                plt.tight_layout()
                if isGif:
                    writer = animation.PillowWriter(fps=30)
                    anim.save(f"{gChoice}Animation.gif", writer=writer)  
                    plt.close()
                else:
                    plt.show()


    
