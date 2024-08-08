import pygame
import json
from pygame import mixer 
import asyncio
import random
import tkinter as tk

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

px=screen_width/1260
py=screen_height/720
#loading sound
mixer.init() 

shotSound=pygame.mixer.Sound('audio/shot.wav')
explosionSound=pygame.mixer.Sound('audio/explosion.wav')


#colors
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)

#loading background
bg = pygame.image.load("Assets/Background/bg.png")
bg = pygame.transform.scale(bg, (screen_width,screen_height))
bg2 = pygame.image.load("Assets/Background/bg2.jpg")
bg2 = pygame.transform.scale(bg2, (screen_width,screen_height))
#loading bullet
bullet1 = pygame.image.load("Assets/bullets/BulletE.png")
bullet1 = pygame.transform.scale(bullet1, (30*px,10*py))
bullet1 = pygame.transform.rotate(bullet1, -90)
#loading the ships
ship1 = pygame.image.load("Assets/Ships/Ship1.png")
ship1 = pygame.transform.scale(ship1, (140*px,140*py))

Enemyship1 = pygame.image.load("Assets/Ships/EnemyShip1.png")
Enemyship1 = pygame.transform.scale(Enemyship1, (140*px,140*py))
Enemyship1 = pygame.transform.rotate(Enemyship1,180)

Enemyship2 = pygame.image.load("Assets/Ships/EnemyShip2.png")
Enemyship2 = pygame.transform.scale(Enemyship2, (140*px,140*py))
Enemyship2 = pygame.transform.rotate(Enemyship2,180)
class Button():
	def __init__(self,x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True
				buttonClick.play()

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action
     
class Ui():
    def __init__(self,x, y,w,h,show):
        self.s=show
        
        self.rect=pygame.Rect(x,y,w,h)


        self.clicked = False


    def draw(self, surface):
        action = False
        if self.s==True:
            pygame.draw.rect(surface, red, self.rect)    
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
                buttonClick.play()

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


            

        return action
#creating the screen
pygame.init()
screen = pygame.display.set_mode((1265*px, 720*py), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

#creating font
font = pygame.font.Font('freesansbold.ttf', 64)
text = font.render('Cosmic Clash', True, green)
textRect = text.get_rect()
textRect.center = (620*px,50*py)

font = pygame.font.Font('freesansbold.ttf', 32)
level_text = font.render('Prepare for the ultimate interstellar showdown!', True, red)
level_textRect = level_text.get_rect()
level_textRect.center = (600*px,50*py)

#loading button images
back = pygame.image.load("Assets/Buttons/back.png")
shop = pygame.image.load("Assets/Buttons/shop.png")
start = pygame.image.load("Assets/Buttons/start.png")
start = pygame.transform.scale(start, (start.get_width()*px,start.get_height()*py-(10*py)))
shop = pygame.transform.scale(shop, (shop.get_width()*px,shop.get_height()*py-(10*py)))

#creating the buttons
start_button=Ui(525*px,380*py,210*px,100*py,False)
shop_button=Button(443*px,330*py,shop,0.24)
back_button=Button(50*px,600*py,back,0.24)

#loading level buttons
l1 = pygame.image.load("Assets/level/1.png")
l2 = pygame.image.load("Assets/level/2.png")
l3 = pygame.image.load("Assets/level/3.png")
l4 = pygame.image.load("Assets/level/4.png")
l5 = pygame.image.load("Assets/level/5.png")
l6 = pygame.image.load("Assets/level/6.png")
l7 = pygame.image.load("Assets/level/7.png")
l8 = pygame.image.load("Assets/level/8.png")

#levels
button_l1=Button(150*px,100*py,l1,0.26)
button_l2=Button(400*px,100*py,l2,0.26)
button_l3=Button(650*px,100*py,l3,0.26)
button_l4=Button(900*px,100*py,l4,0.26)
button_l5=Button(150*px,300*py,l5,0.26)
button_l6=Button(400*px,300*py,l6,0.26)
button_l7=Button(650*px,300*py,l7,0.26)
button_l8=Button(900*px,300*py,l8,0.26)

#creating font blueprint
font = pygame.font.SysFont('Futura', 30)
font2 = pygame.font.SysFont('Futura', 70)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

game_state="Home"

#creating player spaceship coordinates
pl_x=650*px
pl_y=600*py
gameovertick=0

#creating groups
bulletGroup=pygame.sprite.Group()        
EnemyGroup=pygame.sprite.Group()
PlayerbulletGroup=pygame.sprite.Group()
explosion_group=pygame.sprite.Group()
buttonClick=pygame.mixer.Sound('audio/bclick.wav')

#create enemy blueprint
class bullet(pygame.sprite.Sprite):
    def __init__(self,image,speed,x,y,dam):
        pygame.sprite.Sprite.__init__(self)
        self.x=x+(55*px)
        self.y=y+(140*py)
        self.img=image
        self.speed=speed
        self.playerx=pl.xpos
        self.playery=pl.ypos
        self.dam=dam
        self.yChange=((self.playery-self.y)/1000)*self.speed
        self.xChange=((self.playerx-self.x)/1000)*self.speed
        self.rect = self.img.get_rect()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect.center = (self.width/2, self.height/2)
        
    def update(self):
        self.rect.x=self.x
        self.rect.y=self.y
        screen.blit(self.img,(self.x,self.y))
       
        self.x+=self.xChange
        self.y+=self.yChange
        if pygame.sprite.spritecollide(pl,bulletGroup, False):
            
            pl.health-=self.dam
            self.kill()
        if self.y>1500:
            self.kill()

#creating player bullets
class Plbullet(pygame.sprite.Sprite):
    def __init__(self,image,speed,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x=x+(50*px)
        self.y=y+(10*py)
        self.img=image
        self.speed=speed
        self.rect = self.img.get_rect()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect.center = (self.width/2, self.height/2)
        
        
        
        
    def update(self):
        self.rect.x=self.x
        self.rect.y=self.y
        screen.blit(self.img,(self.x,self.y))
        
        self.y-=6*self.speed

        
        
        for i in EnemyGroup:
            if pygame.sprite.spritecollide(i,PlayerbulletGroup, False):
                
                i.health-=10
                self.kill()
                
        
        if self.y<0:
            self.kill()
#creating explosion blueprint
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, scale):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f'Assets/explosion/exp{num}.png').convert_alpha()
			img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
			self.images.append(img)
		self.frame_index = 0
		self.image = self.images[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		self.counter = 0
        
        

	def update(self):
		#scroll
		screen.blit(self.images[self.frame_index],(self.rect.x,self.rect.y))

		EXPLOSION_SPEED = 4
		#update explosion amimation
		self.counter += 1

		if self.counter >= EXPLOSION_SPEED:
			self.counter = 0
			self.frame_index += 1
			#if the animation is complete then delete the explosion
			if self.frame_index >= len(self.images):
				self.kill()
			else:
				self.image = self.images[self.frame_index]


#creating player blueprint
class player(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        pygame.sprite.Sprite.__init__(self)
        self.xpos=x
        self.ypos=y
        self.img=image
        self.health=100
        self.isalive=True
        self.rect = self.img.get_rect()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect.center = (self.width/2, self.height/2)
        self.enemyTakedown=0
        self.shootCooldown=0
    def update(self):
        if self.shootCooldown>0:
            self.shootCooldown-=1
        self.rect.x=self.xpos
        self.rect.y=self.ypos
        if self.health<=0:
            self.isalive=False
        if self.isalive==True:
            screen.blit(self.img,(self.xpos,self.ypos))
            
            return "game"
        else:
            
            self.kill()
            return "lost"



#creating enemy blueprint              
class enemy(pygame.sprite.Sprite):
    def __init__(self,health,dam,img):
        pygame.sprite.Sprite.__init__(self)
        self.x_pos=(random.randrange(100,1000))*px
        self.y_pos=(-300)*py
        self.image=img
        self.health=health
        self.damage=dam
        self.direction=random.randrange(-10,10)
        print(self.direction)
        if self.direction>0:
            self.direction=1
        else:
            self.direction=-1

        self.counter=100
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.center = (self.width/2, self.height/2)
    def update(self):
        self.rect.x=self.x_pos
        self.rect.y=self.y_pos
        screen.blit(self.image,self.rect)
        
        
        if self.y_pos<(100*py):
            self.y_pos+=5
            self.counter=0
        else:
            self.shoot()
            self.counter+=1
            self.movement()

        if self.health<=0:
            self.kill()
            pl.enemyTakedown+=1
            explosion = Explosion(self.rect.x, self.rect.y, 2)
            explosion_group.add(explosion)
            explosionSound.play()

    def shoot(self):
        if self.counter==75:
            
            bt=bullet(bullet1,7,self.x_pos,self.y_pos,self.damage)
            bulletGroup.add(bt)
            self.counter=0
    def movement(self):
        if self.x_pos<0:
            self.direction=1
        elif self.x_pos>1000*px:
            self.direction=-1
        self.x_pos+=2*self.direction
    

#home page
def Home():
    
    screen.blit(bg, (0, 0))

    
    stc=start_button.draw(screen)
    shc=False
    if stc==True:
        return "level"
    elif shc==True:
        return "shop"
    return "Home"
    
        
        
        
#level page
def level():
    screen.blit(bg2, (0, 0))
    screen.blit(level_text, level_textRect)
    lv1=False
    lv2=False
    lv3=False
    lv4=False
    lv5=False
    lv6=False
    lv7=False
    lv8=False
    if dataJson['levels completed']>=7:
        lv1=button_l1.draw(screen)
        lv2=button_l2.draw(screen)
        lv3=button_l3.draw(screen)
        lv4=button_l4.draw(screen)
        lv5=button_l5.draw(screen)
        lv6=button_l6.draw(screen)
        lv7=button_l7.draw(screen)
        lv8=button_l8.draw(screen)
    elif dataJson['levels completed']>=6:
        lv1=button_l1.draw(screen)
        lv2=button_l2.draw(screen)
        lv3=button_l3.draw(screen)
        lv4=button_l4.draw(screen)
        lv5=button_l5.draw(screen)
        lv6=button_l6.draw(screen)
        lv7=button_l7.draw(screen)
    elif dataJson['levels completed']>=5:
        lv1=button_l1.draw(screen)
        lv2=button_l2.draw(screen)
        lv3=button_l3.draw(screen)
        lv4=button_l4.draw(screen)              
        lv5=button_l5.draw(screen)
        lv6=button_l6.draw(screen)
    elif dataJson['levels completed']>=4:
        lv1=button_l1.draw(screen)
        lv2=button_l2.draw(screen)
        lv3=button_l3.draw(screen)
        lv4=button_l4.draw(screen)
        lv5=button_l5.draw(screen)    
    elif dataJson['levels completed']>=3:
        lv1=button_l1.draw(screen)
        lv2=button_l2.draw(screen)
        lv3=button_l3.draw(screen)
        lv4=button_l4.draw(screen)
    elif dataJson['levels completed']>=2:
        lv1=button_l1.draw(screen)
        lv2=button_l2.draw(screen)
        lv3=button_l3.draw(screen)
    elif dataJson['levels completed']>=1:
        lv1=button_l1.draw(screen)
        lv2=button_l2.draw(screen)
    elif dataJson['levels completed']>=0:
        lv1=button_l1.draw(screen)
    if lv1==True:
        
        return "game",1,8
    elif lv2==True:
        
        return "game",2,8
    elif lv3==True:
        return "game",3,10
    elif lv4==True:
        return "game",4,12
    elif lv5==True:
        return "game",5,8
    elif lv6==True:
        return "game",6,8
    elif lv7==True:
        return "game",7,10
    elif lv8==True:
        return "game",8,12
    
    return "level",0,0
    


#shop page
def shop():
    screen.blit(bg, (0, 0))
    bc=back_button.draw(screen)
    if bc==True:
        return "Home"
    return "shop"


#game variables
setup=False

pl=player(pl_x,pl_y,ship1)

cnt=0

game_state="game"
ScreenState="Home"

levelsCompleted=0
dataJson={}

#json file open
with open('gameData.json') as gd:
    dataJson=json.load(gd)

levelsCompleted=dataJson["levels completed"]
print(levelsCompleted)

#game page
def Game(counter,enemycount,initEnemyCount,game_state,lvl,gameovertick):
    if game_state=="game":
        screen.fill((0,0,0))
                
        explosion_group.update()
        bulletGroup.update()
        PlayerbulletGroup.update()
        EnemyGroup.update()
        game_state=pl.update()
        if lvl==1:

                if counter%350==0 and enemycount>0:
                    print(counter)
                    enemy1=enemy(10,7,Enemyship1)
                    EnemyGroup.add(enemy1)
                    
                    enemycount-=1
                
        if lvl==2:

                if counter%350==0 and enemycount>0:
                    print(counter)
                    enemy1=enemy(10,8,Enemyship1)
                    EnemyGroup.add(enemy1)
                    
                    enemycount-=1
                
        if lvl==3:
                if counter%400==0 and enemycount>0:
                    print(counter)
                    enemy1=enemy(15,8,Enemyship2)
                    EnemyGroup.add(enemy1)
                    
                    
                    enemycount-=1
                
                
        if lvl==4:
                if counter%400==0 and enemycount>0:
                    print(counter)
                    enemy1=enemy(15,9,Enemyship2)
                    EnemyGroup.add(enemy1)
                    
                    
                    enemycount-=1
                
                
        if lvl==5:
            
                if counter%500==0 and enemycount>0:
                    print(counter)
                    enemy1=enemy(10,5,Enemyship1)
                    EnemyGroup.add(enemy1)
                    print(counter)
                    enemy1=enemy(10,5,Enemyship1)
                    EnemyGroup.add(enemy1)
                    
                    enemycount-=2
                
        if lvl==6:

                if counter%400==0 and enemycount>0:
                    print(counter)
                    enemy1=enemy(10,6,Enemyship1)
                    EnemyGroup.add(enemy1)
                    print(counter)
                    enemy1=enemy(10,6,Enemyship1)
                    EnemyGroup.add(enemy1)
                    
                    enemycount-=2
                
        if lvl==7:

                if counter%700==0 and enemycount>0:
                    print(counter)
                    enemy1=enemy(15,6,Enemyship2)
                    EnemyGroup.add(enemy1)
                    enemy1=enemy(15,6,Enemyship2)
                    EnemyGroup.add(enemy1)
                    
                    
                    enemycount-=2
                
        if lvl==8:

                if counter%500==0 and enemycount>0:
                    print(counter)
                    enemy1=enemy(15,7,Enemyship2)
                    EnemyGroup.add(enemy1)
                    enemy1=enemy(15,7,Enemyship2)
                    EnemyGroup.add(enemy1)
                    
                    
                    enemycount-=2
                
        draw_text("Health:"+str(pl.health),font,white,10*px,10*py)
        draw_text("Enemys left:"+str(initEnemyCount-pl.enemyTakedown),font,white,10*px,40*py)
        if pl.enemyTakedown==initEnemyCount:
            gameovertick-=1
            if gameovertick==0:
                         
                game_state="won"
        else:
            gameovertick=100            
        return enemycount,game_state,ScreenState,gameovertick
    if game_state=="won":
        screen.fill((0,20,0))
        draw_text("You Won The Game!",font2,blue,500*px,20*py)
        draw_text("Score:"+str(pl.enemyTakedown),font,white,500*px,200*py)
        if dataJson["levels completed"]<lvl:
            dataJson["levels completed"]=lvl
        bc=back_button.draw(screen)
        if bc==True:
            pl.health=100
            pl.isalive=True
            pl.enemyTakedown=0
            for i in EnemyGroup:
                i.kill()
            for i in PlayerbulletGroup:
                i.kill()
            for i in bulletGroup:
                i.kill()
            return 0,"game","Home",0
        
        return 0,game_state,ScreenState,gameovertick
    
    else:
        screen.fill((0,20,0))
        draw_text("Game Over",font2,blue,500*px,20*py)
        draw_text("Score:"+str(pl.enemyTakedown),font,white,500*px,200*py)
        if dataJson["levels completed"]<lvl:
            dataJson["levels completed"]=lvl
        bc=back_button.draw(screen)
        if bc==True:
            pl.health=100
            pl.isalive=True
            pl.enemyTakedown=0
            for i in EnemyGroup:
                i.kill()
            for i in PlayerbulletGroup:
                i.kill()
            for i in bulletGroup:
                i.kill()
            return 0,"game","Home",0
        return 0,game_state,ScreenState,gameovertick

    
    
#declaring control variables
left_keyDown=False   
Right_keyDown=False   

shot=False

enemycount=0
async def main():
    global running,ScreenState,levelChoise,enemycount,lvlEnemyCont,gameovertick,dataJson,game_state,left_keyDown,Right_keyDown,cnt
    while running:
        
        if ScreenState=="Home":
            ScreenState=Home()
        elif ScreenState=="level":
            ScreenState,levelChoise,enemycount=level()
            lvlEnemyCont=enemycount
        elif ScreenState=="shop":
            ScreenState=shop()
        elif ScreenState=="game":
            enemycount,game_state,ScreenState,gameovertick=Game(cnt,enemycount,lvlEnemyCont,game_state,levelChoise,gameovertick)
            
        
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                with open('gameData.json','w') as gdw:
                    json.dump(dataJson,gdw)
                running = False
            if game_state=="game":
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        Right_keyDown=True
                        left_keyDown=False
                    if event.key==pygame.K_LEFT:
                        left_keyDown=True
                        Right_keyDown=False
                    if event.key==pygame.K_SPACE:
                        if pl.shootCooldown==0:
                            blt=Plbullet(bullet1,2,pl.xpos,pl.ypos)
                            PlayerbulletGroup.add(blt)
                            pl.shootCooldown=75
                            shotSound.play()
                    if event.key==pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.KEYUP:
                    if event.key==pygame.K_RIGHT:
                        Right_keyDown=False
                        
                    if event.key==pygame.K_LEFT:
                        left_keyDown=False
                        
                        
        if left_keyDown==True and pl.xpos-5>=0:
            pl.xpos-=5*px
        if Right_keyDown==True and (pl.xpos+pl.rect.width)+5<=1260*py:
            pl.xpos+=5*px
        

    
        pygame.display.flip()
        
        clock.tick(100)  
        cnt+=1
    pygame.quit()
    await asyncio.sleep(0)

asyncio.run(main())