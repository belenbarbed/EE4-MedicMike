CPP += g++
CPPFLAGS += -ggdb -std=c++11 -W -Wall `pkg-config --cflags --libs tesseract opencv`
CPPFLAGS += -I /home/alexluisi/opencv_contrib/modules/text/include/

pipeline :
	mkdir -p pbin
	$(CPP) $(CPPFLAGS)  /Pipeline1.cpp -o pbin/pipeline $^

clean :
	rm pbin/*