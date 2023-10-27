.PHONY: hook clean
all: driver

driver:
	gcc -c -fPIC -fno-stack-protector -fcf-protection=none aflpp_rewrite_driver.c
	ar rcs libAFLRewriteDriver.a aflpp_rewrite_driver.o
clean:
	rm *.a *.o
