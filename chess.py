"""
Name: Augustine Premkumar
File: chess.py

"""
import re
import pygame
import time
import sys
from pygame import Surface, mouse, sprite
from pygame import color
from pygame.constants import K_SPACE, RESIZABLE
import numpy as np
import tensorflow as tf
from tensorflow import keras


# Create a dictionary that links CHESS Notation to GUI Coordinates
chessnotation = {}
word = "abcdefgh"
square = ""
enpassantable = None
thesquarethatis = None
for ch in word:
    square = ch 
    for i in range(1,9):
        square +=str(i)
        chessnotation[square]=[0,0]
        square = ch 

for key in chessnotation:
    if key[0]=="a":
        chessnotation[key][0]= 0
    if key[0] == "b":
        chessnotation[key][0] = 100
    if key[0]=="c":
        chessnotation[key][0]= 200
    if key[0] == "d":
        chessnotation[key][0] = 300
    if key[0]=="e":
        chessnotation[key][0]= 400
    if key[0] == "f":
        chessnotation[key][0] = 500
    if key[0]=="g":
        chessnotation[key][0]= 600
    if key[0] == "h":
        chessnotation[key][0] = 700
    if key[1]=="1":
        chessnotation[key][1]= 700
    if key[1] == "2":
        chessnotation[key][1] = 600
    if key[1]=="3":
        chessnotation[key][1]= 500
    if key[1] == "4":
        chessnotation[key][1] = 400
    if key[1]=="5":
        chessnotation[key][1]= 300
    if key[1] == "6":
        chessnotation[key][1] = 200
    if key[1]=="7":
        chessnotation[key][1]= 100
    if key[1] == "8":
        chessnotation[key][1] = 0

# Create Pieces class that stores information on each piece
class Pieces(pygame.sprite.Sprite):
    def __init__(self,color,imagefile,square="",movecount=0):
        pygame.sprite.Sprite.__init__(self)
        self.color=color
        self.image=pygame.image.load(imagefile)
        self.square=square
        self.movecount=movecount
    
class pawn(Pieces):
    def move_list(self):
        movelist=[]
        protectedlist =[]
        newlist = []

        if self.color=="white":
                if self.movecount==0 and clicked_piece(self.square[0]+str(int(self.square[1])+1))==None:
                    movelist.append(self.square[0]+str(int(self.square[1])+2))
                movelist.append(self.square[0]+str(int(self.square[1])+1))
                movelist.append(chr(ord(self.square[0])+1)+str(int(self.square[1])+1))
                movelist.append(chr(ord(self.square[0])-1)+str(int(self.square[1])+1))
        elif self.color=="black":
                if self.movecount==0 and clicked_piece(self.square[0]+str(int(self.square[1])-1))==None:
                    movelist.append(self.square[0]+str(int(self.square[1])-2))
                movelist.append(self.square[0]+str(int(self.square[1])-1))
                movelist.append(chr(ord(self.square[0])+1)+str(int(self.square[1])-1))
                movelist.append(chr(ord(self.square[0])-1)+str(int(self.square[1])-1))
        
        if self.color =="white":
            for square in movelist[-2:]:
                if clicked_piece(square) == 0:
                    continue
                elif clicked_piece(square)==None or clicked_piece(square).color == self.color:
                    protectedlist.append(square)
                elif clicked_piece(square).color != self.color:
                    newlist.append(square)
        
            for square in sorted(movelist[:-2]):
                if clicked_piece(square) != None or clicked_piece(square) == 0:
                    break
                else:
                    newlist.append(square)
            if thesquarethatis == None:
                pass
            elif int(self.square[1]) == 5 and (chr(ord(self.square[0])+1)==thesquarethatis[0] or chr(ord(self.square[0])-1)==thesquarethatis[0]):
                newlist.append(thesquarethatis)


        elif self.color =="black":
            for square in movelist[-2:]:
                if clicked_piece(square) == 0:
                    continue
                elif clicked_piece(square)==None or clicked_piece(square).color == self.color:
                    protectedlist.append(square)
                elif clicked_piece(square).color != self.color:
                    newlist.append(square)
        
            for square in reversed(sorted(movelist[:-2])):
                if clicked_piece(square) != None or clicked_piece(square) == 0:
                    break
                else:
                    newlist.append(square)
            if thesquarethatis == None:
                pass
            elif int(self.square[1]) == 4 and (chr(ord(self.square[0])+1)==thesquarethatis[0] or chr(ord(self.square[0])-1)==thesquarethatis[0]):
                newlist.append(thesquarethatis)

        return newlist,movelist[-2:]

    def legal_moves(self):
        newlist = self.move_list()[0]
        newerlist = []
        for move in newlist:
            if checkmovecheck(self,move,self.square):
                newerlist.append(move)

        return newerlist

class knight(Pieces):
    def move_list(self):
        movelist = []
        newlist = []
        protectedlist =[]
        movelist.append(chr(ord(self.square[0])+2)+str(int(self.square[1])+1))
        movelist.append(chr(ord(self.square[0])+2)+str(int(self.square[1])-1))
        movelist.append(chr(ord(self.square[0])-2)+str(int(self.square[1])+1))
        movelist.append(chr(ord(self.square[0])-2)+str(int(self.square[1])-1))
        movelist.append(chr(ord(self.square[0])+1)+str(int(self.square[1])+2))
        movelist.append(chr(ord(self.square[0])-1)+str(int(self.square[1])+2))
        movelist.append(chr(ord(self.square[0])+1)+str(int(self.square[1])-2))
        movelist.append(chr(ord(self.square[0])-1)+str(int(self.square[1])-2))
        for i in movelist:
            k = clicked_piece(i)
            if k == 0:
                continue
            elif k == None:
                newlist.append(i)
            elif k.color!=self.color:
                    newlist.append(i)
            elif k.color == self.color:
                    protectedlist.append(i)
        
        return newlist,protectedlist

    def legal_moves(self):
        newlist = self.move_list()[0]
        newerlist = []
        for move in newlist:
            if checkmovecheck(self,move,self.square):
                newerlist.append(move)

        return newerlist

class rook(Pieces):  
    def move_list(self):
        a,d = Horizontal(self.square,self.color)
        b,e = Vertical(self.square,self.color)
        movelist = a+b
        protectedlist = d+e
        return movelist,protectedlist

    def legal_moves(self):
        newlist = self.move_list()[0]
        newerlist = []
        for move in newlist:
            if checkmovecheck(self,move,self.square):
                newerlist.append(move)
        return newerlist

class bishop(Pieces):
    def move_list(self):
        a,b = Diagonal(self.square,self.color)               
        return a,b

    def legal_moves(self):
        newlist = self.move_list()[0]
        newerlist = []
        for move in newlist:
            if checkmovecheck(self,move,self.square):
                newerlist.append(move)
        return newerlist

class queen(Pieces):
    def move_list(self):
        a,d = Horizontal(self.square,self.color)
        b,e = Vertical(self.square,self.color)
        c,f = Diagonal(self.square,self.color)
        movelist = a+b+c
        protectedlist = d+e+f
        return movelist,protectedlist

    def legal_moves(self):
        newlist = self.move_list()[0]
        newerlist = []
        for move in newlist:
            if checkmovecheck(self,move,self.square):
                newerlist.append(move)
        return newerlist

class king(Pieces):
    def move_list(self):
        movelist = []
        newlist = []
        protectedlist =[]
        movelist.append(chr(ord(self.square[0])+1)+str(int(self.square[1])))
        movelist.append(chr(ord(self.square[0])-1)+str(int(self.square[1])))
        movelist.append(chr(ord(self.square[0])+1)+str(int(self.square[1])+1))
        movelist.append(chr(ord(self.square[0])+1)+str(int(self.square[1])-1))
        movelist.append(chr(ord(self.square[0])-1)+str(int(self.square[1])+1))
        movelist.append(chr(ord(self.square[0])-1)+str(int(self.square[1])-1))
        movelist.append(chr(ord(self.square[0]))+str(int(self.square[1])+1))
        movelist.append(chr(ord(self.square[0]))+str(int(self.square[1])-1))
        
        for i in movelist:
            k = clicked_piece(i)
            if k == 0:
                continue
            elif k == None:
                newlist.append(i)
            elif k.color!=self.color:
                    newlist.append(i)
            elif k.color==self.color:
                    protectedlist.append(i)



        # Appending moves for castling 
        if self.color == "white" and self.movecount==0 and  clicked_piece("b1")==None and clicked_piece("c1")==None and clicked_piece("d1")==None and type(clicked_piece("a1"))==rook and clicked_piece("a1").movecount==0:
            newlist.append("a1")
        if self.color == "white" and self.movecount==0 and clicked_piece("f1")==None and clicked_piece("g1")==None and type(clicked_piece("h1"))==rook and clicked_piece("h1").movecount==0:
            newlist.append("h1")
        if self.color == "black" and self.movecount==0  and  clicked_piece("b8")==None and clicked_piece("c8")==None and clicked_piece("d8")==None and type(clicked_piece("a8"))==rook and clicked_piece("a8").movecount==0:
            newlist.append("a8")
        if self.color == "black" and self.movecount==0  and  clicked_piece("f8")==None and clicked_piece("g8")==None and type(clicked_piece("h8"))==rook and clicked_piece("h8").movecount==0:
            newlist.append("h8")


        return newlist,protectedlist
        
    def legal_moves(self):
        newlist = self.move_list()[0]
        killlablelist = killable_squares(self.color)
        legallist = []
        castlelist = ["a1","h1","a8","h8"]
        for move in newlist:
            if move not in killlablelist and move not in castlelist:
                legallist.append(move)
        
        if "a1" in newlist and castlecheck(self.color,"a1") and "a1" not in killlablelist:
                legallist.append("a1")
        elif self.movecount!=0 and "a1" in newlist and "a1" not in killlablelist:
                legallist.append("a1")
        if "h1" in newlist and castlecheck(self.color,"h1")and "h1" not in killlablelist:
                legallist.append("h1")
        elif self.movecount!=0 and "h1" in newlist and "h1" not in killlablelist:
                legallist.append("h1")
        if "a8" in newlist and castlecheck(self.color,"a8")and "a8" not in killlablelist:
                legallist.append("a8")
        elif self.movecount!=0 and "a8" in newlist and "a8" not in killlablelist:
                legallist.append("a8")
        if "h8" in newlist and castlecheck(self.color,"h8")and "h8" not in killlablelist:
                legallist.append("h8")
        elif self.movecount!=0 and "h8" in newlist and "h8" not in killlablelist:
                legallist.append("h8")

        return list(set(legallist))

def Horizontal(square,color):
    movelist =[]
    occupiedfriendly = []
    occupiedenemy= []
    occupiedking =[]
    horzlist =[]
    protectedlist=[]
    alpha = "abcdefgh"
    for k in pieces_list:
        if k.color == color:
            occupiedfriendly.append(k.square)
        if k.color != color:
            occupiedenemy.append(k.square)
            if isinstance(k,king):
                occupiedking.append(k.square)


    for ch in alpha:
        horzlist.append(ch+square[1])
    a = horzlist.index(square)
    for i in horzlist[a+1:]:
        if i in occupiedfriendly:
            protectedlist.append(i)
            break
        if i in occupiedenemy:
            movelist.append(i)
            if i in occupiedking:
                protectedlist.append(chr(ord(i[0])+1)+i[1])
            break
        else:
            movelist.append(i)
    for i in reversed(horzlist[:a]):
        if i in occupiedfriendly:
            protectedlist.append(i)
            break
        if i in occupiedenemy:
            movelist.append(i)
            if i in occupiedking:
                protectedlist.append(chr(ord(i[0])-1)+i[1])
            break
        else:
            movelist.append(i)
        
    return movelist,protectedlist

def Vertical(square,color):
    movelist =[]
    occupiedfriendly = []
    occupiedenemy= []
    occupiedking =[]
    vertlist=[]
    protectedlist =[]
    for k in pieces_list:
        if k.color == color:
            occupiedfriendly.append(k.square)
        if k.color != color:
            occupiedenemy.append(k.square)
            if isinstance(k,king):
                occupiedking.append(k.square)

    for i in range(1,9):
        vertlist.append(square[0]+str(i))
    b = vertlist.index(square)
    for i in vertlist[b+1:]:
        if i in occupiedfriendly:
            protectedlist.append(i)
            break
        if i in occupiedenemy:
            movelist.append(i)
            if i in occupiedking:
                protectedlist.append(i[0]+str(int(i[1])+1))
            break
        else:
            movelist.append(i)
    for i in reversed(vertlist[:b]):
        if i in occupiedfriendly:
            protectedlist.append(i)
            break
        if i in occupiedenemy:
            movelist.append(i)
            if i in occupiedking:
                protectedlist.append(i[0]+str(int(i[1])-1))
            break
        else:
            movelist.append(i)

    return movelist,protectedlist

def Diagonal(square,color):
    movelist =[]
    occupiedfriendly = []
    occupiedking =[]
    occupiedenemy= []
    diagonalistru=[]
    diagonalistlu = []
    diagonalistld = []
    diagonalistrd=[]
    protectedlist =[]

    for k in pieces_list:
        if k.color == color:
            occupiedfriendly.append(k.square)
        if k.color != color:
            occupiedenemy.append(k.square)
            if isinstance(k,king):
                occupiedking.append(k.square)
    newsquare = square 
    while 1:
        newsquare = chr(ord(newsquare[0])+1)+str(int(newsquare[1])+1)
        if newsquare in chessnotation.keys():
            diagonalistru.append(newsquare)
        else:
            break
    newsquare = square 
    while 1:
        newsquare = chr(ord(newsquare[0])+1)+str(int(newsquare[1])-1)
        if newsquare in chessnotation.keys():
            diagonalistrd.append(newsquare)
        else:
            break
    newsquare = square 
    while 1:
        newsquare = chr(ord(newsquare[0])-1)+str(int(newsquare[1])-1)
        if newsquare in chessnotation.keys():
            diagonalistld.append(newsquare)
        else:
            break
    newsquare = square 
    while 1:
        newsquare = chr(ord(newsquare[0])-1)+str(int(newsquare[1])+1)
        if newsquare in chessnotation.keys():
            diagonalistlu.append(newsquare)
        else:
            break

    for i in diagonalistru:
        if i in occupiedfriendly:
            protectedlist.append(i)
            break
        if i in occupiedenemy:
            movelist.append(i)
            if i in occupiedking:
                protectedlist.append(chr(ord(i[0])+1)+str(int(i[1])+1))
            break
        else:
            movelist.append(i)
    for i in diagonalistrd:
        if i in occupiedfriendly:
            protectedlist.append(i)
            break
        if i in occupiedenemy:
            movelist.append(i)
            if i in occupiedking:
                protectedlist.append(chr(ord(i[0])+1)+str(int(i[1])-1))
            break
        else:
            movelist.append(i)
    for i in diagonalistlu:
        if i in occupiedfriendly:
            protectedlist.append(i)
            break
        if i in occupiedenemy:
            movelist.append(i)
            if i in occupiedking:
                protectedlist.append(chr(ord(i[0])-1)+str(int(i[1])+1))
            break
        else:
            movelist.append(i)
    for i in diagonalistld:
        if i in occupiedfriendly:
            protectedlist.append(i)
            break
        if i in occupiedenemy:
            movelist.append(i)
            if i in occupiedking:
                protectedlist.append(chr(ord(i[0])-1)+str(int(i[1])-1))
            break
        else:
            movelist.append(i)
    
    return movelist,protectedlist
model = keras.models.load_model("99.97%_model.h5")

def image_preprocessor(filename):
  import PIL 
#   from IPython.display import Image, display
#   from matplotlib import pyplot as plt
  from PIL import Image as im
  img = PIL.Image.open(filename)
#   img = img.resize((400,400),resample=PIL.Image.Resampling.BOX)
  left = 0 
  top = 0 
  right = 50
  bottom = 50
  count = 0

  train_data =np.zeros((64,50,50,3),dtype="float32")

  for i in range(64):   
    #(left,top,right,bottom)
    img = img.crop([left,top,right,bottom])
    left += 50
    right += 50
    count += 1
    if count% 8 == 0: 
      bottom += 50
      top += 50
      left = 0 
      right = 50
    # img.save(f"{str(count)}.png")
    train_data[count-1] = np.asarray(img)
    # display(Image(f"{str(count)}.png"))
    img = PIL.Image.open(filename)
    # img = img.resize((400,400),resample=PIL.Image.Resampling.BOX)
  #greyscale
  train_data = np.dot(train_data[...,:3],[0.2989, 0.5870, 0.1140])
  #normalize
  train_data /= 255
  return train_data

def predict_board(file_name):
  board = np.argmax(model.predict(image_preprocessor(file_name)),axis=-1)
  print(np.reshape(board,(8,8)))
  return np.reshape(board,(8,8))

def arrayofint_to_arrayofclasses(array):
  new_list = list()
  initial_column = "a"
  row_idx = 8
  column_idx = 0
  for row in array:
    for column in row:
      if column!=0:
        if column == 1:
            new_list.append(rook("black","brook.png",initial_column+str(row_idx)))
        elif column == 2:
            new_list.append(knight("black","bknight.png",initial_column+str(row_idx)))
        elif column == 3:
            new_list.append(bishop("black","bbishop.png",initial_column+str(row_idx)))
        elif column == 4:
            new_list.append(queen("black","bqueen.png",initial_column+str(row_idx)))
        elif column == 5:
            new_list.append(king("black","bking.png",initial_column+str(row_idx)))
        elif column == 6:
            new_list.append(pawn("black","bpawn.png",initial_column+str(row_idx)))
        elif column == 7:
            new_list.append(rook("white","wrook.png",initial_column+str(row_idx)))
        elif column == 8:
            new_list.append(knight("white","wknight.png",initial_column+str(row_idx)))
        elif column == 9:
            new_list.append(bishop("white","wbishop.png",initial_column+str(row_idx)))
        elif column == 10:
            new_list.append(queen("white","wqueen.png",initial_column+str(row_idx)))
        elif column == 11:
            new_list.append(king("white","wking.png",initial_column+str(row_idx)))
        elif column == 12:
            new_list.append(pawn("white","wpawn.png",initial_column+str(row_idx)))
      column_idx +=1
      initial_column = chr(ord(initial_column)+1)
    column_idx = 0
    initial_column = "a"
    row_idx -=1
  return new_list

def check_square(mousepos):
    y, x = mousepos
    rows = y // 100
    columns = x // 100
    return rows*100, columns*100

# Convert a GUI cordinate that has passed the check_square function into ChessNotation 
# Input:tuple Returns:string
def convert_cord_toChessNot(tuple):
    tuple = list(tuple)
    for key in chessnotation:
        if chessnotation[key]==tuple:
            return key

# Checks if a square has a piece on it, if it does it returns the piece object, if it does not it returns None
# Input:String Returns:Object that is on that Square/ None
def clicked_piece(square):
    if square not in chessnotation.keys():
        return 0
    for piece in pieces_list:
        if piece.square==square:
            return piece
    return None

# Updates the positions of pieces on the Board
# Inputs: Piece Object, String Returns:None
def move_piece(piece,square,movecounter):
    global enpassantable
    global thesquarethatis

    if move_legal(piece,square,piece.square):

        # ENPASSANT 
        if isinstance(piece,pawn) and square == thesquarethatis:
            piece.square = thesquarethatis
            if piece.color == "white":
                kambachi = clicked_piece(thesquarethatis[0]+str(int(thesquarethatis[1])-1))
            elif piece.color == "black":
                kambachi = clicked_piece(thesquarethatis[0]+str(int(thesquarethatis[1])+1))
            pieces_list.remove(kambachi)
            piece.movecount+=1
            movecounter+=1
            pygame.mixer.music.load("captures.mp3")
            pygame.mixer.music.play()
            thesquarethatis = None
            enpassantable = False
            return movecounter


        # Captures
        for k in pieces_list:
            if k.color!=piece.color and k != piece and k.square == square:
                pieces_list.remove(k)
                pygame.mixer.music.load("captures.mp3")
                pygame.mixer.music.play()
                music = True
        
        enpassantable = False
        thesquarethatis = None

        a = clicked_piece(square)


        #Castling
        try:
            b = a.color
        except:
            pass
        else:
            if b == piece.color:
                if square == "a1":
                    clicked_piece("a1").square = "d1"
                    piece.square = "c1"
                    piece.movecount +=1
                    movecounter+=1
                    pygame.mixer.music.load("castling.mp3")
                    pygame.mixer.music.play()
                    return movecounter
                if square == "h1":
                    clicked_piece("h1").square = "f1"
                    piece.square = "g1"
                    piece.movecount +=1
                    movecounter+=1
                    pygame.mixer.music.load("castling.mp3")
                    pygame.mixer.music.play()
                    return movecounter
                if square == "a8":
                    clicked_piece("a8").square = "d8"
                    piece.square = "c8"
                    piece.movecount +=1
                    movecounter+=1
                    pygame.mixer.music.load("castling.mp3")
                    pygame.mixer.music.play()
                    return movecounter            
                if square == "h8":
                    clicked_piece("h8").square = "f8"
                    piece.square = "g8"
                    piece.movecount +=1
                    movecounter+=1
                    pygame.mixer.music.load("castling.mp3")
                    pygame.mixer.music.play()
                    return movecounter
        


        # ENPASSANT CHECKER 
        if isinstance(piece,pawn) and abs(int(piece.square[1])-int(square[1]))==2 and piece.color=="black":
            enpassantable = True
            thesquarethatis = piece.square[0] + str(int(piece.square[1])-1)
                
        if isinstance(piece,pawn) and abs(int(piece.square[1])-int(square[1]))==2 and piece.color=="white":
            enpassantable = True
            thesquarethatis = piece.square[0] + str(int(piece.square[1])+1)

        piece.square=square

        # Promotion
        if check_promotion():
            if piece.color == "white":
                newqueen = queen("white","wqueen.png",piece.square)
            if piece.color == "black":
                newqueen = queen("black","bqueen.png",piece.square)
            pieces_list.remove(piece)
            pieces_list.append(newqueen)
        

        piece.movecount+=1
        movecounter+=1
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("legalmove.wav")
            pygame.mixer.music.play()
        return movecounter
    else:
        pygame.mixer.music.load("illegalmovebetter.wav")
        pygame.mixer.music.play()
        return movecounter
    


# Need to code checks for if the move is legal or not
# Input: Piece Object, String, String Returns:Bool
def move_legal(piece,squareto,squarefrom):
  if isinstance(piece,king) and squareto not in piece.legal_moves():
      return False
  elif squareto not in piece.legal_moves():
        return False
  else:
      return True



# If the move results in a collision between 2 piece objects, Need to remove the piece that was stationary and update piecesgroup
# Input:None Output:None / Updatespiecesgroup 
def check_promotion():
    for k in pieces_list:
        if isinstance(k,pawn):
            if k.color == "white" and k.square[1] == "8":
                return True
            if k.color == "black" and k.square[1] == "1":
                return True
    else:
        return False
# Need to code if the King is in danger or not
# Input: Don't know yet, Output:bool
def check_if_undercheck(color):
    a = killable_squares(color)
    for piece in pieces_list:
        if isinstance(piece,king) and piece.color==color:
            kingsquare = piece.square
    if kingsquare in a:
        return True

# Checks if a particular move results in a check 
# Returns False if move results in Check 
def checkmovecheck(piece,move,squarefrom):
    a = False
    piece.square = move
    count = 0
    for k in list(pieces_list):
        if k.color!=piece.color and k != piece and k.square == move:
            save = k
            pieces_list.remove(k)
            a = True
        count +=1

    if isinstance(piece,pawn) and move == thesquarethatis:
        piece.square = thesquarethatis
        if piece.color == "white":
            kambachi = clicked_piece(thesquarethatis[0]+str(int(thesquarethatis[1])-1))
        elif piece.color == "black":
            kambachi = clicked_piece(thesquarethatis[0]+str(int(thesquarethatis[1])+1))
        save = kambachi
        pieces_list.remove(kambachi) 
        a = True
        
    if check_if_undercheck(piece.color):
        piece.square = squarefrom
        if a == True:
            pieces_list.append(save)
        return False
    else: 
        piece.square = squarefrom
        if a == True:
            pieces_list.append(save)
        return True

# Returns True if color is CHECKMATED
# Input: Dont know yet, Output: boolx
def check_if_checkmate(color):
    for piece in list(pieces_list):
        if piece.color==color and len(piece.legal_moves())>0:
            return False
    return True


# Searches the board for killable squares returns a List 
def killable_squares(color):
    thelist = []
    for piece in pieces_list:
        if piece.color != color:
            if isinstance(piece,pawn):
                thelist.append(piece.move_list()[1])
            else:
                a,b = piece.move_list()
                thelist.append(a+b)
            
    killablelsit = [k for i in thelist for k in i]
    
    return list(sorted(list(set(killablelsit))))


def castlecheck(color,square):
    a = set(killable_squares(color))
    if square == "a1":
        b = set(["c1","d1","e1"])
    if square == "h1":
        b = set(["e1","f1","g1"])
    if square == "a8":
        b = set(["e8","d8","c8"])
    if square == "h8":
        b = set(["e8","f8","g8"])      

    if not a&b:
        return True
    else:
        return False


# Opening Splash Screen
def openingsplash():
    pieces_list = list()
    nah = 800,485
    newscren = pygame.display.set_mode(nah,RESIZABLE)
    pygame.display.set_caption("Chess")
    openingscreen = pygame.image.load("size.jpg")
    openingscreenrect = openingscreen.get_rect()
    myfont = pygame.font.SysFont("Bradley Hand ITC",28)
    b =myfont.render("Press N for a newgame, Press SPACE to load an existing game",True,"white")
    c = 30,0
    titlefont = pygame.font.SysFont("Algerian",100)
    d = titlefont.render("Chess",True,"white")
    e = (250,90)
    pygame.mixer.music.load("openingmusic.wav")
    pygame.mixer.music.play(-1)
    while 1:
        clock.tick(30)
        newscren.blit(openingscreen,openingscreenrect)
        newscren.blit(b,c)
        newscren.blit(d,e)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    from tkinter import Tk,Button
                    from tkinter import filedialog
                    file_path = filedialog.askopenfilename()
                    board = predict_board(file_path)
                    for i in arrayofint_to_arrayofclasses(board):
                        pieces_list.append(i)
                    return pieces_list
                if event.key == pygame.K_n:
                    pieces_list = [queen("white","wqueen.png","d1")
                    ,king("white","wking.png","e1")
                    ,bishop("white","wbishop.png","c1")
                    ,bishop("white","wbishop.png","f1")
                    ,knight("white","wknight.png","b1")
                    ,knight("white","wknight.png","g1")
                    ,rook("white","wrook.png","a1")
                    ,rook("white","wrook.png","h1")
                    ,pawn("white","wpawn.png","a2")
                    ,pawn("white","wpawn.png","b2")
                    ,pawn("white","wpawn.png","c2")
                    ,pawn("white","wpawn.png","d2")
                    ,pawn("white","wpawn.png","e2")
                    ,pawn("white","wpawn.png","f2")
                    ,pawn("white","wpawn.png","g2")
                    ,pawn("white","wpawn.png","h2")
                    ,queen("black","bqueen.png","d8")
                    ,king("black","bking.png","e8")
                    ,bishop("black","bbishop.png","c8")
                    ,bishop("black","bbishop.png","f8")
                    ,knight("black","bknight.png","b8")
                    ,knight("black","bknight.png","g8")
                    ,rook("black","brook.png","a8")
                    ,rook("black","brook.png","h8")
                    ,pawn("black","bpawn.png","a7")
                    ,pawn("black","bpawn.png","b7")
                    ,pawn("black","bpawn.png","c7")
                    ,pawn("black","bpawn.png","d7")
                    ,pawn("black","bpawn.png","e7")
                    ,pawn("black","bpawn.png","f7")
                    ,pawn("black","bpawn.png","g7")
                    ,pawn("black","bpawn.png","h7")]
                    return pieces_list
            if event.type == pygame.QUIT: sys.exit()
    
# Ending Splash Screen
def endingsplash(color):
    global movecounter
    global pieces_list
    spashscreen = pygame.image.load("endingsplash.jpg").convert()
    myfont = pygame.font.SysFont("Broadway",20)
    textfont = pygame.font.SysFont("Times New Roman",10)
    title = myfont.render(f"{color.capitalize()} won!",True, "black")
    text = textfont.render("Press any button to play again", True, "black")
    text2 = textfont.render("Exit window to quit",True,"black")
    place = (370,315)
    place1 =(380,350)
    place2 = (400,370)
    screen.blit(board, boardrect)
    for a in pieces_list:
        screen.blit(a.image,chessnotation[a.square])
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                pieces_list = [queen("white","wqueen.png","d1")
                ,king("white","wking.png","e1")
                ,bishop("white","wbishop.png","c1")
                ,bishop("white","wbishop.png","f1")
                ,knight("white","wknight.png","b1")
                ,knight("white","wknight.png","g1")
                ,rook("white","wrook.png","a1")
                ,rook("white","wrook.png","h1")
                ,pawn("white","wpawn.png","a2")
                ,pawn("white","wpawn.png","b2")
                ,pawn("white","wpawn.png","c2")
                ,pawn("white","wpawn.png","d2")
                ,pawn("white","wpawn.png","e2")
                ,pawn("white","wpawn.png","f2")
                ,pawn("white","wpawn.png","g2")
                ,pawn("white","wpawn.png","h2")
                ,queen("black","bqueen.png","d8")
                ,king("black","bking.png","e8")
                ,bishop("black","bbishop.png","c8")
                ,bishop("black","bbishop.png","f8")
                ,knight("black","bknight.png","b8")
                ,knight("black","bknight.png","g8")
                ,rook("black","brook.png","a8")
                ,rook("black","brook.png","h8")
                ,pawn("black","bpawn.png","a7")
                ,pawn("black","bpawn.png","b7")
                ,pawn("black","bpawn.png","c7")
                ,pawn("black","bpawn.png","d7")
                ,pawn("black","bpawn.png","e7")
                ,pawn("black","bpawn.png","f7")
                ,pawn("black","bpawn.png","g7")
                ,pawn("black","bpawn.png","h7")]
                movecounter = 1
                pygame.mixer.music.load("startingsound.mp3")
                pygame.mixer.music.play()
                return pieces_list
        screen.blit(spashscreen,(275,275))
        screen.blit(title,place)
        screen.blit(text,place1)
        screen.blit(text2,place2)
        pygame.display.flip()
    
    return

# Create the Board and the GUI
pygame.init()
clock = pygame.time.Clock()
pieces_list = openingsplash()
size = hight,width = 800,800
screen=pygame.display.set_mode(size,RESIZABLE)
board =pygame.image.load("board.png").convert()
boardrect= board.get_rect() 
screen.blit(board,boardrect)
spashscreen = pygame.image.load("endingsplash.jpg").convert()
pygame.mixer.music.load("startingsound.mp3")
pygame.mixer.music.play()

pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
pygame.event.set_allowed(pygame.MOUSEMOTION)
                            
movecounter = 1
# Primary Loop for the Game, loops many times per second 
while 1:
    # Checks events to identify when a player has clicked on a square
    # If the square has a piece, it is stored and moved when the mouse is released
    # If there was no piece that was selected nothing gets updated and the board remains the same
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            a = check_square(mouse.get_pos())
            clickedsquare = convert_cord_toChessNot(a)
            clickedpiece = clicked_piece(clickedsquare)
            # try:
            #     print(clickedpiece.legal_moves(),len(clickedpiece.legal_moves()),clickedpiece.movecount)
            # except:
            #     pass
        if event.type == pygame.MOUSEBUTTONUP:
            b = check_square(mouse.get_pos())
            droppedsquare=convert_cord_toChessNot(b)
            try:
                if movecounter % 2 !=0 and clickedpiece.color=='white':
                    movecounter = move_piece(clickedpiece,droppedsquare,movecounter)
                    if check_if_undercheck("black"):
                        pygame.mixer.music.load("check.mp3")
                        pygame.mixer.music.play()
                if movecounter % 2 == 0 and clickedpiece.color == "black":
                    movecounter = move_piece(clickedpiece,droppedsquare,movecounter)
                    if check_if_undercheck("white"):
                        pygame.mixer.music.load("check.mp3")
                        pygame.mixer.music.play()
            except:
                continue
        
        # Quits game when the window is closed
        if event.type == pygame.QUIT: sys.exit()
    
    # Draws the board
    screen.blit(board, boardrect)
    # Draws the pieces 
    for a in pieces_list:
        screen.blit(a.image,chessnotation[a.square])
    
    # If checkmate enters splash screen
    if check_if_checkmate("white"):
        pygame.mixer.music.load("checkmatereal.mp3")
        pygame.mixer.music.play()
        pieces_list = endingsplash("black")
        continue
    if check_if_checkmate("black"):
        pygame.mixer.music.load("checkmatereal.mp3")
        pygame.mixer.music.play()
        pieces_list = endingsplash("white")
        continue
    pygame.display.flip()
    