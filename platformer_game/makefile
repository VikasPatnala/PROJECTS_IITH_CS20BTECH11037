SFMLDIR=/home/harsha/packages/SFML-2.5.1
INCLUDEDIR=$(SFMLDIR)/include
LIBDIR=$(SFMLDIR)/lib
CC =g++
LIBFLAGS=-lsfml-graphics -lsfml-window -lsfml-audio -lsfml-network -lsfml-system
TESTFLAGS= -lgtest -lgtest_main -lpthread $(LIBFLAGS)
SRCS = State.cpp GameState.cpp MainMenuState.cpp Button.cpp Game.cpp\
	 animation.cpp Player.cpp Bound_Rect.cpp InterfaceState.cpp Tilemap.cpp Tile.cpp\
	  TextureSelector.cpp QuitState.cpp GameInfo.cpp PlayerInfo.cpp collider.cpp \
	  PlayerAttributes.cpp PauseMenu.cpp Enemytile.cpp Enemy.cpp Floortile.cpp Shield.cpp\
	  Collisionvisitor.cpp Coin.cpp SoundEffects.cpp Settings.cpp Water.cpp LevelInfo.cpp\
	  HowToPlay.cpp Finishtile.cpp Powerup1.cpp Levelup.cpp Backgroundtile.cpp Poison.cpp\
	  Icytile.cpp Floormovement.cpp Icymovement.cpp Crate.cpp Powerup2.cpp
GAMESRCS = Main.cpp
TESTSRCS= test.cpp Animationtest.cpp Boundtest.cpp Playertest.cpp Collisiontest.cpp\
	Playercollisiontest.cpp


GAMEOBJS =$(addsuffix .o,$(basename $(GAMESRCS)))
TESTOBJS = $(addsuffix .o,$(basename $(TESTSRCS)))

OBJS = $(addsuffix .o,$(basename $(SRCS)))

GAMEEXE = Game
TESTEXE = test


.PHONY = clean all
all = $(GAMEEXE) $(TESTEXE)

$(GAMEEXE) : $(OBJS) $(GAMEOBJS)
	$(CC) -o $@ -L $(LIBDIR) $(OBJS) $(GAMEOBJS) $(LIBFLAGS)

$(OBJS) :%.o :%.cpp
	$(CC) -c -I $(INCLUDEDIR) $<
	
$(GAMEOBJS) :%.o :%.cpp
	$(CC) -c -I $(INCLUDEDIR) $<

$(TESTOBJS) :%.o :%.cpp
	$(CC) -c -I $(INCLUDEDIR) $<

$(TESTEXE) : $(OBJS) $(TESTOBJS)
	$(CC) -o $@ -L $(LIBDIR) $(OBJS) $(TESTOBJS) $(TESTFLAGS)
	
clean:
	rm $(OBJS) $(GAMEEXE) $(TESTEXE) $(GAMEOBJS) $(TESTOBJS)