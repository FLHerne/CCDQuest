import pygame, sys
from pygame.locals import *
pygame.init()
def ToolTip(window, event, X, Y, Width, Height, Font, Size, InColour, FontColour, Message):
    if event.type == MOUSEMOTION:
        if event.pos[0] in range(X,X+Width) and event.pos[1] in range(Y,Y+Height):
            basicFont = pygame.font.SysFont(Font, Size)
            if InColour != None:
                text = basicFont.render(Message,True,FontColour,InColour)
            else:
                text = basicFont.render(Message,True,FontColour)
            textrect = text.get_rect()
            textrect.topleft = (event.pos)
            return (text,textrect)
    return None
def ToolTipPrint(window,Text):
    if Text != None:
        window.blit(Text[0],Text[1])
def Button(window,event,X,Y,Width,Height):
    if event.type == MOUSEBUTTONDOWN:
        if event.pos[0] in range(X,X+Width) and event.pos[1] in range(Y,Y+Height):
            return True
def Print(window,Password = False, X = 500, Y = 200, Length = 200, InColour = (255,255,255),FontColour = (0,0,0), Font = None, Size = 48, Message = '', Centre = False, YCentre = [False,200], PrintLength = False):
    basicFont = pygame.font.SysFont(Font, Size)
    ExtraChr = ''
    if Password == False:
        while basicFont.render(Message,True,FontColour).get_rect().width > Length:
            if Message[::-1][0] == '|':
                ExtraChr += Message[::-1][1]
                Message = Message[:-2] + '|'
                
            else:
                ExtraChr += Message[::-1][0]
                Message = Message[:-1]
        if InColour != None:
            text = basicFont.render(Message,True,FontColour,InColour)
        else:
            text = basicFont.render(Message,True,FontColour)
    else:
        counter = 0
        tempMessage = ''
        for i in Message:
            counter += 1
            if i != '|':
                tempMessage += '*'
            else:
                tempMessage += '|'
        Message = tempMessage
        while basicFont.render(Message,True,FontColour).get_rect().width > Length:
            if Message[::-1][0] == '|':
                Message = Message[:-2] + '|'
            else:
                Message = Message[:-1]
        if InColour != None:
            text = basicFont.render(Message,True,FontColour,InColour)
        else:
            text = basicFont.render(Message,True,FontColour)


            
    textrect = text.get_rect()
    textrect.topleft = (X,Y)
    if PrintLength == True:
        print(textrect.width)
        print(textrect.height)
    textrect.width = Length
    if YCentre[0] == True:
        textrect.height = YCentre[1]
    textpos = text.get_rect()
    textpos.topleft = (X,Y)
    if Centre == True:
        textpos.left = (textrect.left + ((textrect.width - textpos.width)/2))
    if YCentre[0] == True:
        textpos.top = (textrect.top + ((textrect.height - textpos.height)/2))
    if Centre == False and YCentre[0] == False:
        textpos = textrect
    if InColour != None and window != None:
        pygame.draw.rect(window,InColour,textrect)
    if window != None:
        window.blit(text,textpos)
    return Message, ExtraChr[::-1]
def List(window,X,Y,Width,Message,Messages,Length,Iterate = 'Down'):
    basicFont = pygame.font.SysFont('Arial', 20) 
    if Message != None:
        while basicFont.render(Message,True,(0,0,0)).get_rect().width > Width:
            Message = Message[:-1]
        Messages.insert(0,[Message,-15])
        counter = -1
        for i in Messages:
            counter += 1
            Messages[counter][1] += 15
            if i[1] == 15*(Length):
                Messages.pop(counter)   
    for i in Messages:
        text = basicFont.render(i[0], True, (0,0,0), (255,255,255))
        textrect = text.get_rect()
        if Iterate == 'Down':
            textrect.topleft = (X,Y+i[1])
        else:
            textrect.topleft = (X,Y-i[1])
        textrect.width = Width
        pygame.draw.rect(window,(255,255,255),textrect)
        window.blit(text,textrect)
    return Messages
def Input(window, event, Password = False, X = 500, Y = 200, Length = 200, Font = None, Size = 48,Message = [],EnterEnd = True,Height=[False,100]):
    CHARACTERS = {48:'0',49:'1',50:'2',51:'3',52:'4',53:'5',54:'6',55:'7',56:'8',57:'9',45:'-',61:'=',91:'[',93:']',59:';',39:'\'',92:'#',44:',',46:'.',47:'/',60:'\\'}
    S_CHARACTERS = {48:')',49:'!',50:'"',51:'#',52:'$',53:'%',54:'^',55:'&',56:'*',57:'(',45:'_',61:'+',91:'{',93:'}',59:':',39:'@',92:'~',44:'<',46:'>',47:'?'}
    basicFont = pygame.font.SysFont(Font,Size)
    Message[1] = ''
    if event.type == MOUSEBUTTONDOWN:
        if Height[0] == True:
            if event.pos[0] in range(X,X+Length+1) and event.pos[1] in range(Y,Y+Height[1]+1):
                if Message[2] == False:
                    Message[2] = True
                    Message[0] += '|'
            else:
                Message[2] = False
                if len(Message[0]) != 0:
                    if Message[0][::-1][0] == '|':
                        Message[0] = Message[0][:-1]
        else:
            if event.pos[0] in range(X,X+Length+1) and event.pos[1] in range(Y,Y+basicFont.render(Message[0],True,(0,0,0)).get_rect().height):
                if Message[2] == False:
                    Message[2] = True
                    Message[0] += '|'
            else:
                Message[2] = False
                if len(Message[0]) != 0:
                    if Message[0][::-1][0] == '|':
                        Message[0] = Message[0][:-1]
    if Message[2] == True:
        if event.type == KEYDOWN:
            if len(Message[0]) != 0:
                if Message[0][::-1][0] == '|':
                    Message[0] = Message[0][:-1]
            #LETTERS
            if event.key in range(97,123):
                if event.mod in (8192,1,2,4097,4098,12288):
                    Message[0] += chr(event.key-32)
                else:
                    Message[0] += chr(event.key)
            #CHARACTERS
            if event.key in CHARACTERS:
                if event.mod in (1,2,4097,4098):
                    for i in S_CHARACTERS:
                        if i == event.key:
                            Message[0] += S_CHARACTERS[i]
                else:
                    for i in CHARACTERS:
                        if i == event.key:
                            Message[0] += CHARACTERS[i]
            #BACKSPACE
            if event.key == 8:
                Message[0] = Message[0][:-1]
            #SPACEBAR
            if event.key == 32:
                Message[0] += ' '
            Message[0] += '|'
            while basicFont.render(Message[0],True,(0,0,0)).get_rect().width > Length:
                    Message[0] = Message[0][:-2] + '|'
            #RETURN
            if event.key == 13 and EnterEnd == True:
                Message[2] = False
                Message[1] = Message[0][:-1]
                Message[0] = ''
    else:
        if event.type == KEYDOWN:
            if event.key == 13 and EnterEnd == True:
                Message[0] += '|'
                while basicFont.render(Message[0],True,(0,0,0)).get_rect().width > Length:
                    Message[0] = Message[:-2] + '|'
                Message[2] = False
                Message[1] = Message[0][:-1]
                Message[0] = ''
    return Message
