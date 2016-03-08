reed-solomon.so: *.c *.h
	gcc -O3 -Wall -Werror -shared -lm -o reed_solomon.so reed_solomon.c
	cp reed_solomon.so ../rscode/

android:
	arm-linux-androideabi-gcc -O3 -Wall -Werror -mfpu=neon -fpic -shared -lm -o reed_solomon-android.so reed_solomon.c
	cp reed_solomon-android.so ../rscode/

clean:
	rm -f *.so
