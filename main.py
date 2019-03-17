import pygame
import sys
from sprites import *
from settings import *
from os import path

class Game(Entity):
    def __init__(self):
        Entity.__init__(self)
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.timer = pygame.time.Clock()
        self.running = True
        self.timecount = 0
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)

        # load images
        self.saveblock_image = pygame.image.load('images/saveblock.png')
        self.savedblock_image = pygame.image.load('images/savedblock.png')

        # load highscore
        with open(path.join(self.dir + '/highscores', DEMO_DEATH_FILE), 'r+') as f:
            try:
                self.demo_least_deathcount = int(f.read())
            except:
                self.demo_least_deathcount = "No Data"
        
        with open(path.join(self.dir + '/highscores', DEMO_TIME_FILE), 'r+') as f:
            try:
                self.demo_best_time = float(f.read())
            except:
                self.demo_best_time = "No Data"
        with open(path.join(self.dir + '/highscores', EASY_DEATH_FILE), 'r+') as f:
            try:
                self.easy_least_deathcount = int(f.read())
            except:
                self.easy_least_deathcount = "No Data"
        
        with open(path.join(self.dir + '/highscores', EASY_TIME_FILE), 'r+') as f:
            try:
                self.easy_best_time = float(f.read())
            except:
                self.easy_best_time = "No Data"
        
        with open(path.join(self.dir + '/highscores', NORMAL_DEATH_FILE), 'r+') as f:
            try:
                self.normal_least_deathcount = int(f.read())
            except:
                self.normal_least_deathcount = "No Data"
        
        with open(path.join(self.dir + '/highscores', NORMAL_TIME_FILE), 'r+') as f:
            try:
                self.normal_best_time = float(f.read())
            except:
                self.normal_best_time = "No Data"
        
        with open(path.join(self.dir + '/highscores', HARD_DEATH_FILE), 'r+') as f:
            try:
                self.hard_least_deathcount = int(f.read())
            except:
                self.hard_least_deathcount = "No Data"
        
        with open(path.join(self.dir + '/highscores', HARD_TIME_FILE), 'r+') as f:
            try:
                self.hard_best_time = float(f.read())
            except:
                self.hard_best_time = "No Data"
             
        # load stage data
        with open(path.join(self.dir + '/stage', 'level_select_stage.txt'), 'r+') as f:
            self.level_select_stage = f.readlines()
        with open(path.join(self.dir + '/stage', EASY_STAGE_FILE), 'r+') as f:
            self.easystage = f.readlines()
        with open(path.join(self.dir + '/stage', NORMAL_STAGE_FILE), 'r+') as f:
            self.normalstage = f.readlines()
        with open(path.join(self.dir + '/stage', HARD_STAGE_FILE), 'r+') as f:
            self.hardstage = f.readlines()
        with open(path.join(self.dir + '/stage', DEMO_STAGE_FILE), 'r+') as f:
            self.demostage = f.readlines()
        
        with open(path.join(self.dir + '/stage', EASY_STAGE_FILE2), 'r+') as f:
            self.easystage2 = f.readlines()
        with open(path.join(self.dir + '/stage', NORMAL_STAGE_FILE2), 'r+') as f:
            self.normalstage2 = f.readlines()
        with open(path.join(self.dir + '/stage', HARD_STAGE_FILE2), 'r+') as f:
            self.hardstage2 = f.readlines()
        with open(path.join(self.dir + '/stage', DEMO_STAGE_FILE2), 'r+') as f:
            self.demostage2 = f.readlines()
        
        with open(path.join(self.dir + '/stage', EASY_STAGE_FILE3), 'r+') as f:
            self.easystage3 = f.readlines()
        with open(path.join(self.dir + '/stage', NORMAL_STAGE_FILE3), 'r+') as f:
            self.normalstage3 = f.readlines()
        with open(path.join(self.dir + '/stage', HARD_STAGE_FILE3), 'r+') as f:
            self.hardstage3 = f.readlines()
        with open(path.join(self.dir + '/stage', DEMO_STAGE_FILE3), 'r+') as f:
            self.demostage3 = f.readlines()

        # load sound data
        self.jumpsound = pygame.mixer.Sound('music/jump.wav')
        self.djumpsound = pygame.mixer.Sound('music/djump.wav')
        self.deathsound = pygame.mixer.Sound('music/death.wav')
        self.deathsound.set_volume(0.5)

    def new(self):
        # start a new game
        self.entities = pygame.sprite.Group()
        self.jump = self.jump_cut = self.left = self.right = False
        self.gameover = False
        self.savecollision = False
        self.platforms = []
        self.water = []
        self.cherry = []
        self.cherry_sideways = []
        self.cherry_updown = []
        self.spikeup = []
        self.spikeup_sideways = []
        self.spikeup_updown = []
        self.spikedown = []
        self.spikeleft = []
        self.spikeright = []
        self.saveblock = []
        self.exitportal = []
        self.nothing = []

        # choose which level to build
        if self.levelscreen:
            self.layer1 = self.level_select_stage
            self.layer2 = []
            self.layer3 = []
        if self.easy:
            self.layer1 = self.easystage
            self.layer2 = self.easystage2
            self.layer3 = self.easystage3
        if self.normal:
            self.layer1 = self.normalstage
            self.layer2 = self.normalstage2
            self.layer3 = self.normalstage3
        if self.hard:
            self.layer1 = self.hardstage
            self.layer2 = self.hardstage2
            self.layer3 = self.hardstage3
        if self.demo:
            self.layer1 = self.demostage
            self.layer2 = self.demostage2
            self.layer3 = self.demostage3
        
        x = y = 0

        # build layer1
        for row in self.layer1:
            for col in row:
                if col == "M":
                    m = SpikeupUpdown(x, y)
                    self.spikeup_updown.append(m)
                    self.entities.add(m)
                if col == "P":
                    p = Platform(x, y)
                    self.platforms.append(p)
                    self.entities.add(p)
                if col == "U":
                    u = Spikeup(x, y)
                    self.spikeup.append(u)
                    self.entities.add(u)
                if col == "D":
                    d = Spikedown(x, y)
                    self.spikedown.append(d)
                    self.entities.add(d)
                if col == "L":
                    l = Spikeleft(x, y)
                    self.spikeleft.append(l)
                    self.entities.add(l)
                if col == "R":
                    r = Spikeright(x, y)
                    self.spikeright.append(r)
                    self.entities.add(r)
                if col == "C":
                    c = Cherry(x, y)
                    self.cherry.append(c)
                    self.entities.add(c)
                if col == "S":
                    s = SaveBlock(x, y)
                    self.saveblock.append(s)
                    self.entities.add(s)         
                if col == "E":
                    e = ExitPortal(x, y)
                    self.exitportal.append(e)
                    self.entities.add(e)
                if col == "A":
                    self.easyportal = EasyPortal(x, y)
                    self.entities.add(self.easyportal)
                if col == "N":
                    self.normalportal = NormalPortal(x, y)
                    self.entities.add(self.normalportal)
                if col == "H":
                    self.hardportal = HardPortal(x, y)
                    self.entities.add(self.hardportal)
                if col == "T":
                    self.demoportal = DemoPortal(x, y)
                    self.entities.add(self.demoportal)
                if not self.saved:
                    if col == "K":
                        self.player = Player(self, x, y)
                x += 32
            y += 32
            x = 0
        
        # respawn at savepoint if saved
        if self.saved:
            self.player = Player(self, self.x, self.y)
            
        self.entities.add(self.player)
        
        x = y = 0

        # build layer2
        for row in self.layer2:
            for col in row:
                if col == "W":
                    w = Water(x, y)
                    self.water.append(w)
                    self.entities.add(w)
                if col == "F":
                    f = SpikeupSideways(x, y)
                    self.spikeup_sideways.append(f)
                    self.entities.add(f)
                if col == "B":
                    b = CherrySideways(x, y)
                    self.cherry_sideways.append(b)
                    self.entities.add(b)
                if col == "D":
                    d = CherryUpdown(x, y)
                    self.cherry_updown.append(d)
                    self.entities.add(d)
                if col == 'Z':
                    z = Nothing(x, y)
                    self.nothing.append(z)
                    self.entities.add(z)
                x += 32
            y += 32
            x = 0
        
        x = y = 0
        
        # build layer3
        for row in self.layer3:
            for col in row:
                if col == "W":
                    w = Water(x, y)
                    self.water.append(w)
                    self.entities.add(w)
                x += 32
            y += 32
            x = 0

        self.run()

    def run(self):
        # run the game
        self.playing = True
        while self.playing:
            self.timer.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # update player
        self.player.update(self.jump, self.jump_cut, self.left, self.right, self.platforms, self.water)

        # update traps
        for item in range(0, len(self.spikeup_sideways)):
            self.spikeup_sideways[item].update(self.nothing)
        for item in range(0, len(self.spikeup_updown)):
            self.spikeup_updown[item].update()
        for item in range(0, len(self.cherry)):
            self.cherry[item].update()
        for item in range(0, len(self.cherry_sideways)):
            self.cherry_sideways[item].update(self.nothing)
        for item in range(0, len(self.cherry_updown)):
            self.cherry_updown[item].update(self.nothing)

        # check for collisions
        spikeup_hits = pygame.sprite.spritecollide(self.player, self.spikeup, False, pygame.sprite.collide_mask)
        spikeup_sideways_hits = pygame.sprite.spritecollide(self.player, self.spikeup_sideways, False, pygame.sprite.collide_mask)
        spikeup_updown_hits = pygame.sprite.spritecollide(self.player, self.spikeup_updown, False, pygame.sprite.collide_mask)
        spikedown_hits = pygame.sprite.spritecollide(self.player, self.spikedown, False, pygame.sprite.collide_mask)
        spikeleft_hits = pygame.sprite.spritecollide(self.player, self.spikeleft, False, pygame.sprite.collide_mask)
        spikeright_hits = pygame.sprite.spritecollide(self.player, self.spikeright, False, pygame.sprite.collide_mask)
        cherry_hits = pygame.sprite.spritecollide(self.player, self.cherry, False, pygame.sprite.collide_mask)
        cherry_sideways_hits = pygame.sprite.spritecollide(self.player, self.cherry_sideways, False, pygame.sprite.collide_mask)
        cherry_updown_hits = pygame.sprite.spritecollide(self.player, self.cherry_updown, False, pygame.sprite.collide_mask)
        exitportal_hits = pygame.sprite.spritecollide(self.player, self.exitportal, False, pygame.sprite.collide_mask)
        saveblock_hits = pygame.sprite.spritecollide(self.player, self.saveblock, False, pygame.sprite.collide_circle_ratio(0.4))
        easyportal_hits = pygame.sprite.collide_mask(self.player, self.easyportal)
        normalportal_hits = pygame.sprite.collide_mask(self.player, self.normalportal)
        hardportal_hits = pygame.sprite.collide_mask(self.player, self.hardportal)
        demoportal_hits = pygame.sprite.collide_mask(self.player, self.demoportal)
    
        # level select
        if easyportal_hits and self.levelscreen:
            self.playing = False
            self.levelscreen = False
            self.easy = True
            self.startingtime = pygame.time.get_ticks()
        
        if normalportal_hits and self.levelscreen:
            self.playing = False
            self.levelscreen = False
            self.normal = True
            self.startingtime = pygame.time.get_ticks()
        
        if hardportal_hits and self.levelscreen:
            self.playing = False
            self.levelscreen = False
            self.hard = True
            self.startingtime = pygame.time.get_ticks()
        
        if demoportal_hits and self.levelscreen:
            self.playing = False
            self.levelscreen = False
            self.demo = True
            self.startingtime = pygame.time.get_ticks()

        # stop the program if player hits trap
        if spikeup_hits or spikeup_sideways_hits or spikeup_updown_hits or spikedown_hits or spikeleft_hits or spikeright_hits or cherry_hits or cherry_sideways_hits or cherry_updown_hits:
            self.deathsound.play()
            self.deathcount = self.deathcount + 1
            self.playing = False
            self.gameover = True
            self.wait_for_key()
        
        # save player's position if player hits saveblock
        if saveblock_hits:
            self.x = self.player.rect.left
            self.y = self.player.rect.top
            self.saved = True
            self.savecollision = True
            for item in range(0, len(saveblock_hits)):
                self.colliding_saveblock =  saveblock_hits[item]
                self.colliding_saveblock.image = self.savedblock_image

        if not saveblock_hits and self.savecollision:
            self.timecount = self.timecount + 1
            if self.timecount > 50:
                self.savecollision = False
                self.colliding_saveblock.image = self.saveblock_image
                self.timecount = 0
        
        # show stage clear screen if player hits exitportal
        if exitportal_hits:
            self.playing = False
            self.stageclear = True

        # stop the program if player goes off screen
        if self.player.rect.top > WIN_HEIGHT + 64:
            self.deathsound.play()
            self.deathcount = self.deathcount + 1
            self.playing = False
            self.gameover = True
            self.wait_for_key()

    def events(self):
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # check if key pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.jump = True
                self.jump_cut = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.right = True

            # check if key released
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.jump = False
                self.jump_cut = True
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                self.left = False
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                self.right = False
            
            # go back to startscreen if escape key pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.playing = False
                self.restartgame = True

    def draw(self):
        # draw game screen
        self.screen.blit(bg[1], (0,0))
        if self.levelscreen:
            self.entities.draw(self.screen)
            self.draw_text("Select Level", 48, WHITE, WIN_WIDTH / 2, WIN_HEIGHT / 4)
            self.draw_text("Easy", 16, WHITE, WIN_WIDTH / 3 - 23, WIN_HEIGHT - 90)
            self.draw_text("Normal", 16, WHITE, WIN_WIDTH / 2 + 68, WIN_HEIGHT - 90)
            self.draw_text("Hard", 16, WHITE, WIN_WIDTH - 110, WIN_HEIGHT - 90)
        else:
            self.entities.draw(self.screen)
            self.draw_text("Death Count : " + str(self.deathcount), 16, WHITE, WIN_WIDTH - 80, 10)
        pygame.display.update()

    def show_start_screen(self):
        self.startscreen = True
        self.gameover = False
        self.saved = False
        self.stageclear = False
        self.restartgame = False
        self.easy = False
        self.normal = False
        self.hard = False
        self.demo = False
        self.deathcount = 0
        # play background music
        pygame.mixer.music.load(BGM)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)
        # game splash/start screen
        self.screen.blit(bg[0], (0,0))
        self.draw_text(TITLE, 48, BLACK, WIN_WIDTH / 2, WIN_HEIGHT / 4)
        self.draw_text("Press R key to play", 22, BLACK, WIN_WIDTH / 2, WIN_HEIGHT / 2)
        self.draw_text("Best Clear Time : ", 16, WHITE, 100, WIN_HEIGHT * 8 / 10 + 40)
        self.draw_text("Least Death Count : ", 16, WHITE, 100, WIN_HEIGHT * 8 / 10)
        self.draw_text("Easy", 16, LIGHTBLUE, 250, WIN_HEIGHT * 8 / 10 - 40)
        self.draw_text("Normal", 16, GREEN, 400, WIN_HEIGHT * 8 / 10 - 40)
        self.draw_text("Hard", 16, RED, 550, WIN_HEIGHT * 8 / 10 - 40)  
        self.draw_text("Demo", 16, YELLOW, 700, WIN_HEIGHT * 8 / 10 - 40)

        # draw highscores
        self.draw_text(str(self.easy_least_deathcount), 16, WHITE, 250, WIN_HEIGHT * 8 / 10)
        if self.easy_best_time == "No Data":
            self.draw_text(str(self.easy_best_time), 16, WHITE, 250, WIN_HEIGHT * 8 / 10 + 40)
        else:
            self.draw_text(str(self.easy_best_time) + " sec", 16, WHITE, 250, WIN_HEIGHT * 8 / 10 + 40)
        
        self.draw_text(str(self.normal_least_deathcount), 16, WHITE, 400, WIN_HEIGHT * 8 / 10)
        if self.normal_best_time == "No Data":
            self.draw_text(str(self.normal_best_time), 16, WHITE, 400, WIN_HEIGHT * 8 / 10 + 40)
        else:
            self.draw_text(str(self.normal_best_time) + " sec", 16, WHITE, 400, WIN_HEIGHT * 8 / 10 + 40)
        
        self.draw_text(str(self.hard_least_deathcount), 16, WHITE, 550, WIN_HEIGHT * 8 / 10)
        if self.hard_best_time == "No Data":
            self.draw_text(str(self.hard_best_time), 16, WHITE, 550, WIN_HEIGHT * 8 / 10 + 40)
        else:
            self.draw_text(str(self.hard_best_time) + " sec", 16, WHITE, 550, WIN_HEIGHT * 8 / 10 + 40)
        
        self.draw_text(str(self.demo_least_deathcount), 16, WHITE, 700, WIN_HEIGHT * 8 / 10)
        if self.demo_best_time == "No Data":
            self.draw_text(str(self.demo_best_time), 16, WHITE, 700, WIN_HEIGHT * 8 / 10 + 40)
        else:
            self.draw_text(str(self.demo_best_time) + " sec", 16, WHITE, 700, WIN_HEIGHT * 8 / 10 + 40)
        
        pygame.display.update()
        self.wait_for_key()

    def show_stage_clear_screen(self):
        self.restartgame = True
        # calculate clear time:
        self.cleartime = pygame.time.get_ticks()
        self.cleartime = self.cleartime - self.startingtime 
        self.cleartime = self.cleartime/1000
        self.cleartime = round(self.cleartime, 2)
        # game clear screen
        self.screen.blit(bg[2], (0,0))
        self.draw_text("Thank You for Playing!!", 48, WHITE, WIN_WIDTH / 2, WIN_HEIGHT / 4)
        self.draw_text("Press R key to play again", 22, WHITE, WIN_WIDTH / 2, WIN_HEIGHT / 2)
        self.draw_text("Death Count : " + str(self.deathcount), 22, WHITE, WIN_WIDTH / 2, WIN_HEIGHT * 4 / 6)
        self.draw_text("Clear Time : " + str(self.cleartime) + " sec", 22, WHITE, WIN_WIDTH / 2, WIN_HEIGHT * 5 / 6)

        # demo highscore
        if self.demo:
            if self.demo_least_deathcount == "No Data":
                self.demo_least_deathcount = self.deathcount
                self.draw_text("New Record!!!", 22, WHITE, WIN_WIDTH / 2, WIN_HEIGHT * 4 / 6 + 40)
                with open(path.join(self.dir + '/highscores', DEMO_DEATH_FILE), 'w') as f:
                    f.write(str(self.deathcount))

            if self.deathcount < self.demo_least_deathcount:
                self.demo_least_deathcount = self.deathcount
                self.draw_text("New Record!!!", 22, WHITE, WIN_WIDTH / 2, WIN_HEIGHT * 4 / 6 + 40)
                with open(path.join(self.dir + '/highscores', DEMO_DEATH_FILE), 'w') as f:
                    f.write(str(self.deathcount))
        
            if self.demo_best_time == "No Data":
                self.demo_best_time = self.cleartime
                self.draw_text("New Record!!!", 22, WHITE, WIN_WIDTH / 2, WIN_HEIGHT * 5 / 6 + 40)
                with open(path.join(self.dir + '/highscores', DEMO_TIME_FILE), 'w') as f:
                    f.write(str(self.cleartime))

            if self.cleartime < self.demo_best_time:
                self.demo_best_time = self.cleartime
                self.draw_text("New Record!!!", 22, (255,255,255), WIN_WIDTH / 2, WIN_HEIGHT * 5 / 6 + 40)
                with open(path.join(self.dir + '/highscores', DEMO_TIME_FILE), 'w') as f:
                    f.write(str(self.cleartime))

        # easy highscore    
        if self.easy:
            if self.easy_least_deathcount == "No Data":
                self.easy_least_deathcount = self.deathcount
                self.draw_text("New Record!!!", 22, WHITE, WIN_WIDTH / 2, WIN_HEIGHT * 4 / 6 + 40)
                with open(path.join(self.dir + '/highscores', EASY_DEATH_FILE), 'w') as f:
                    f.write(str(self.deathcount))

            if self.deathcount < self.easy_least_deathcount:
                self.easy_least_deathcount = self.deathcount
                self.draw_text("New Record!!!", 22, WHITE, WIN_WIDTH / 2, WIN_HEIGHT * 4 / 6 + 40)
                with open(path.join(self.dir + '/highscores', EASY_DEATH_FILE), 'w') as f:
                    f.write(str(self.deathcount))
        
            if self.easy_best_time == "No Data":
                self.easy_best_time = self.cleartime
                self.draw_text("New Record!!!", 22, WHITE, WIN_WIDTH / 2, WIN_HEIGHT * 5 / 6 + 40)
                with open(path.join(self.dir + '/highscores', EASY_TIME_FILE), 'w') as f:
                    f.write(str(self.cleartime))

            if self.cleartime < self.easy_best_time:
                self.easy_best_time = self.cleartime
                self.draw_text("New Record!!!", 22, (255,255,255), WIN_WIDTH / 2, WIN_HEIGHT * 5 / 6 + 40)
                with open(path.join(self.dir + '/highscores', EASY_TIME_FILE), 'w') as f:
                    f.write(str(self.cleartime))
        
        # normal highscore
        if self.normal:
            if self.normal_least_deathcount == "No Data":
                self.normal_least_deathcount = self.deathcount
                self.draw_text("New Record!!!", 22, WHITE, WIN_WIDTH / 2, WIN_HEIGHT * 4 / 6 + 40)
                with open(path.join(self.dir + '/highscores', NORMAL_DEATH_FILE), 'w') as f:
                    f.write(str(self.deathcount))

            if self.deathcount < self.normal_least_deathcount:
                self.normal_least_deathcount = self.deathcount
                self.draw_text("New Record!!!", 22, WHITE, WIN_WIDTH / 2, WIN_HEIGHT * 4 / 6 + 40)
                with open(path.join(self.dir + '/highscores', NORMAL_DEATH_FILE), 'w') as f:
                    f.write(str(self.deathcount))
        
            if self.normal_best_time == "No Data":
                self.normal_best_time = self.cleartime
                self.draw_text("New Record!!!", 22, WHITE, WIN_WIDTH / 2, WIN_HEIGHT * 5 / 6 + 40)
                with open(path.join(self.dir + '/highscores', NORMAL_TIME_FILE), 'w') as f:
                    f.write(str(self.cleartime))

            if self.cleartime < self.normal_best_time:
                self.normal_best_time = self.cleartime
                self.draw_text("New Record!!!", 22, (255,255,255), WIN_WIDTH / 2, WIN_HEIGHT * 5 / 6 + 40)
                with open(path.join(self.dir + '/highscores', NORMAL_TIME_FILE), 'w') as f:
                    f.write(str(self.cleartime))
        
        # hard highscore
        if self.hard:
            if self.hard_least_deathcount == "No Data":
                self.hard_least_deathcount = self.deathcount
                self.draw_text("New Record!!!", 22, WHITE, WIN_WIDTH / 2, WIN_HEIGHT * 4 / 6 + 40)
                with open(path.join(self.dir + '/highscores', HARD_DEATH_FILE), 'w') as f:
                    f.write(str(self.deathcount))

            if self.deathcount < self.hard_least_deathcount:
                self.hard_least_deathcount = self.deathcount
                self.draw_text("New Record!!!", 22, WHITE, WIN_WIDTH / 2, WIN_HEIGHT * 4 / 6 + 40)
                with open(path.join(self.dir + '/highscores', HARD_DEATH_FILE), 'w') as f:
                    f.write(str(self.deathcount))
        
            if self.hard_best_time == "No Data":
                self.hard_best_time = self.cleartime
                self.draw_text("New Record!!!", 22, WHITE, WIN_WIDTH / 2, WIN_HEIGHT * 5 / 6 + 40)
                with open(path.join(self.dir + '/highscores', HARD_TIME_FILE), 'w') as f:
                    f.write(str(self.cleartime))

            if self.cleartime < self.hard_best_time:
                self.hard_best_time = self.cleartime
                self.draw_text("New Record!!!", 22, (255,255,255), WIN_WIDTH / 2, WIN_HEIGHT * 5 / 6 + 40)
                with open(path.join(self.dir + '/highscores', HARD_TIME_FILE), 'w') as f:
                    f.write(str(self.cleartime))
            
        pygame.display.update()
        self.wait_for_key()

    def wait_for_key(self):
        # show gameover screen if gameover
        if self.gameover:
            self.gameoversprite = pygame.sprite.Group()
            self.game_over_screen = GameOver(0, 150)
            self.gameoversprite.add(self.game_over_screen)
            self.gameoversprite.draw(self.screen)
            pygame.display.update()
        # stop the program
        waiting = True
        while waiting:
            self.timer.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # close the window to exit
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP and event.key == pygame.K_r:
                    # start the program if r key is pressed
                    if self.startscreen:
                        self.startscreen = False
                        self.levelscreen = True
                    waiting = False
    
    def draw_text(self, text, size, color, x, y):
        # text drawing template
        font = pygame.font.Font(FONT_NAME, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()

while g.running:
    if g.restartgame:
        g.show_start_screen()
    
    if not g.startscreen:
        g.new()

    if g.stageclear:
        g.show_stage_clear_screen()

pygame.quit()
sys.exit()