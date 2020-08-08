import matplotlib.pyplot as plt
import numpy as np
import os 
import cv2  
import PIL.Image
from collections import namedtuple, defaultdict
import time
from tkinter import *
endxmin=0
endxmax=0
endymin=0
endymax=0
generation=0
initialboardlist=[]
Cellbox = namedtuple('Cellbox', ['x', 'y'])
root = Tk()
root.title("Game of Life")
frame = Frame(root, width=300, height=300)
frame.pack()
canvas = Canvas(frame, width=300, height=300)
canvas.pack()


class Cell:
    def __init__(self, x, y, i, j):
        self.isAlive = False
        self.nextStatus = None
        self.pos_screen = (x, y)
        self.pos_matrix = (i, j)

    def __str__(self):
        return str(self.isAlive)

    def __repr__(self):
        return str(self.isAlive)

    def switchStatus(self):
        self.isAlive = not self.isAlive




def displayboard(board):
    # print(board)
    global generation
    global endxmax
    global endxmin
    global endymax
    global endymin
    xs = [x for (x, y) in board]
    ys = [y for (x, y) in board]
    if(len(xs)==0):
        plt.figure()
        plt.scatter(xs,ys)
        plt.title('Generation:'+str(generation))
        plt.axis([endxmin-2,endxmax+2,endymin-2,endymax+2])
        ax=plt.gca()
        ax.grid(True)
        ax.set_ylim(ax.get_ylim()[::-1])
        ax.xaxis.tick_top()   
        ax.yaxis.set_ticks(np.arange(endymin-2, endymax+2, 1))
        ax.xaxis.set_ticks(np.arange(endxmin-2, endxmax+2, 1))
        ax.yaxis.tick_left()    
        generation=generation+1
        plt.savefig('./animation/generation_'+str(generation-1)+'.png')
        plt.show()
        return 1
    else:
        xmax=max(xs)
        if(xmax>endxmax):
            endxmax=xmax
        xmin=min(xs)
        if (xmin<endxmin):
            endxmin=xmin
        ymax=max(ys)
        if(ymax>endymax):
            endymax=ymax
        ymin=min(ys)
        if(ymin<endymin):
            endymin=ymin
        plt.figure()
        plt.scatter(xs,ys)
        plt.title('Generation:'+str(generation))
        plt.axis([endxmin-2,endxmax+2,endymin-2,endymax+2])
        ax=plt.gca()
        ax.grid(True)
        ax.set_ylim(ax.get_ylim()[::-1])
        ax.xaxis.tick_top()   
        ax.yaxis.set_ticks(np.arange(endymin-2, endymax+2, 1))
        ax.xaxis.set_ticks(np.arange(endxmin-2, endxmax+2, 1))
        ax.yaxis.tick_left()    
        generation=generation+1
        plt.savefig('./animation/generation_'+str(generation-1)+'.png')
        plt.show()
        
        return 0

def displayboardonterminal(board, pad=0):
    if not board:
        return "empty"
    board_str = ""
    xs = [x for (x, y) in board]
    ys = [y for (x, y) in board]
    for y in range(min(ys) - pad, max(ys) + 1 + pad):
        for x in range(min(xs) - pad, max(xs) + 1 + pad):
            board_str += 'o' if Cellbox(x, y) in board else '.'
        board_str += '\n'
    return board_str.strip()

def generate_animation():
    #print(os.getcwd())  
  
    os.chdir("D:\projects\game of life\\animation")   
    path = "D:\projects\game of life\\animation"

    mean_height = 0
    mean_width = 0
    
    num_of_images = len(os.listdir('.')) 
    
    for file in os.listdir('.'): 
        im = PIL.Image.open(os.path.join(path, file)) 
        width, height = im.size 
        mean_width += width 
        mean_height += height 
    
    mean_width = int(mean_width / num_of_images) 
    mean_height = int(mean_height / num_of_images) 
      
    for file in os.listdir('.'): 
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"): 
            im = PIL.Image.open(os.path.join(path, file))  
    
            width, height = im.size    
            #print(width, height) 
      
            imResize = im.resize((mean_width, mean_height), PIL.Image.ANTIALIAS)  
            imResize.save( file, 'PNG', quality = 95)  
            #print(im.filename.split('\\')[-1], " is resized") 
    image_folder = '.' 
    video_name = 'mygeneratedvideo.avi'
    os.chdir("D:\projects\game of life\\animation") 
      
    images = [img for img in os.listdir(image_folder) 
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")] 
      
    #print(images)  
  
    frame = cv2.imread(os.path.join(image_folder, images[0])) 
  
    height, width, layers = frame.shape   
  
    video = cv2.VideoWriter(video_name, 0, 1, (width, height))  
  

    for image in images:  
        video.write(cv2.imread(os.path.join(image_folder, image)))  
       
    cv2.destroyAllWindows()  
    video.release() 
    

def getneighbours(cell):
    for x in range(cell.x - 1, cell.x + 2):
        for y in range(cell.y - 1, cell.y + 2):
            if (x, y) != (cell.x, cell.y):
                #print(x,y)
                #print(cell.x, cell.y)
                yield Cellbox(x, y)


def neighbourcount(board):
    neighbour_counts = defaultdict(int)
    #print(neighbour_counts)
    for cell in board:
        for neighbour in getneighbours(cell):
            neighbour_counts[neighbour] += 1
    print(neighbour_counts)
    return neighbour_counts


def nextgeneration(board):
    new_board = set()
    for cell, count in neighbourcount(board).items():
        if count == 3 or (cell in board and count == 2):
            new_board.add(cell)
    print(new_board)
    return new_board


def generateboard(desc):
    board = set()
    for row, line in enumerate(desc.split("\n")):
        for col, elem in enumerate(line):
            if elem == 'o':
                board.add(Cellbox(int(col), int(row)))
    print(board)
    return board

def start_evol():
    root.destroy()


def find_rect_coordinates(x, y):
    return (x- x%10, y - y%10)


def change_colour_on_click(event):
    #print(event.x, event.y)
    global initialboardlist
    x, y = find_rect_coordinates(event.x, event.y)
    try:
        iy = x / 10 - 1
        ix = y / 10 - 1
        if ix == -1 or iy == -1:
            raise IndexError
        flag=0
        for i in range(len(initialboardlist)):
            if(initialboardlist[i][0]==int(ix) and initialboardlist[i][1]==int(iy)):
                initialboardlist.pop(i)
                #print('popping')
                flag=1
        if(flag==0):
            element=[int(ix),int(iy)]
            #print('pushing')
            initialboardlist.append(element)
        #print(initialboardlist)
        if grid[int(ix)][int(iy)].isAlive:
            canvas.itemconfig(rectangles[int(ix)][int(iy)], fill="white")
        else:
            canvas.itemconfig(rectangles[int(ix)][int(iy)], fill="black")
        grid[int(ix)][int(iy)].switchStatus()
    except IndexError:
        return


def initializeboard():
    print('enter initial grid size : ')
    size=int(input())
    x = 10
    y = 10
    global grid
    global rectangles
    rectangles = []
    grid = []
    for i in range(size):
        grid.append([])
        rectangles.append([])
        for j in range(size):
            rect = canvas.create_rectangle(x, y, x+10, y+10, fill="white")
            rectangles[i].append(rect)
            grid[i].append(Cell(x, y, i, j))
            x += 10
        x = 10
        y += 10
    stop = Button(root, text="Start Evolution", command = start_evol)
    stop.pack(side = RIGHT)
    canvas.bind("<Button-1>", change_colour_on_click)
    root.mainloop()

def generateboardcells():
    global initialboardlist
    board=set()
    for i in range(len(initialboardlist)):
        elem=initialboardlist[i]
        board.add(Cellbox(int(elem[1]),int(elem[0])))
    return board
if __name__ == '__main__':
    initializeboard()
    boardcells=generateboardcells()
    print(boardcells)
    displayboard(boardcells)
    while(True):
        boardcells = nextgeneration(boardcells)
        flag=displayboard(boardcells)
        if(flag==1):
            print('ending')
            break
        else:
            time.sleep(0.1)
    
    generate_animation()
    